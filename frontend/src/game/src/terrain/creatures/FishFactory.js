import Creature from "./creature.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import * as THREE from "three";
import * as SkeletonUtils from "three/examples/jsm/utils/SkeletonUtils";
import { updateLoadingTime } from "../../performance_utils.js";

class FishFactory {
  constructor(terrain_geometry, terrain_obj) {
    this.creatures = [];
    this.initialized = this.initialize(terrain_geometry, terrain_obj);
  }

  async initialize(terrain_geometry, terrain_obj) {
    try {
      await updateLoadingTime(
        "Terrain",
        "Fish1",
        async () => this.loadObjects(),
        7,
      );
      await updateLoadingTime(
        "Terrain",
        "Fish2",
        async () => this.init(terrain_geometry, terrain_obj),
        8,
      );
    } catch (error) {
      console.error("Error initializing FishFactory:", error);
    }
  }

  async loadObjects() {
    try {
      this.fishScene = await this.loadModel("/game/assets/guppy_fish.glb", {
        x: 0.5,
        y: 0.5,
        z: 0.5,
      });
      this.jellyfishScene = await this.loadModel("/game/assets/jellyfish.glb", {
        x: 4,
        y: 4,
        z: 4,
      });
    } catch (error) {
      console.error("Error loading fish objects:", error);
      throw error;
    }
  }

  async init(terrain_geometry, terrain_obj) {
    for (let i = 0; i < 8; i++) {
      let fish = new Fish(
        terrain_geometry,
        terrain_obj,
        this.cloneScene(this.fishScene),
      );
      this.creatures.push(fish);
    }

    for (let i = 0; i < 3; i++) {
      let jellyfish = new JellyFish(
        terrain_geometry,
        terrain_obj,
        this.cloneScene(this.jellyfishScene),
      );
      this.creatures.push(jellyfish);
    }
  }

  cloneScene(scene) {
    let clonedModel = SkeletonUtils.clone(scene.model);
    let mixer = new THREE.AnimationMixer(clonedModel);

    if (scene.animations && scene.animations.length > 0) {
      let animationAction = mixer.clipAction(scene.animations[0]);
      animationAction.setLoop(THREE.LoopRepeat, Infinity);
      animationAction.play();
    }
    return {
      model: clonedModel,
      mixer: mixer,
    };
  }

  loadModel(path, scale) {
    return new Promise((resolve, reject) => {
      const loader = new GLTFLoader();
      loader.load(
        path,
        (gltf) => {
          let scene = {};
          scene.model = gltf.scene;
          scene.mixer = new THREE.AnimationMixer(scene.model);
          scene.animations = gltf.animations;
          if (gltf.animations.length > 0) {
            scene.animationAction = scene.mixer.clipAction(scene.animations[0]);
          }
          scene.model.scale.set(scale.x, scale.y, scale.z);
          resolve(scene);
        },
        undefined,
        (error) => {
          console.error(error);
          reject(error);
        },
      );
    });
  }
}

class JellyFish extends Creature {
  constructor(terrain_geometry, terrain_obj, scene) {
    super(terrain_geometry, terrain_obj, scene);
    this.looks_target = false;
    this.max_speed = 0.1;
    this.min_speed = -0.1;
    this.spawn_y = -5;
    this.max_y = -3;
    this.makeSomeCreatures();
  }
}

class Fish extends Creature {
  constructor(terrain_geometry, terrain_obj, scene) {
    super(terrain_geometry, terrain_obj, scene);
    this.looks_target = true;
    this.max_speed = 0.2;
    this.min_speed = -0.2;
    this.spawn_y = -3;
    this.max_y = -1;
    this.makeSomeCreatures();
  }
}

export default FishFactory;
