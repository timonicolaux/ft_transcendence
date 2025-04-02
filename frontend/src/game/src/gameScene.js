import * as THREE from "three";
import { init_light } from "./scene/lights.js";
import { init_camera } from "./scene/camera.js";
import Ball from "./game/ball.js";
import Arena from "./game/arena.js";
import Paddle from "./game/paddle.js";
import { GameConfig } from "./config.js";
import TerrainFactory from "./terrain/generation/terrain_factory.js";
import SkyGenerator from "./terrain/sky.js";
import FishFactory from "./terrain/creatures/FishFactory.js";
import Renderer from "./scene/rendering.js";
import state from "../../app.js";
import { updateLoadingTime } from "./performance_utils.js";

export class GameScene {
  constructor() {
    this.loadingTimes = {};
    this.stats = {};
    this.config = new GameConfig();
    this.canvas = document.querySelector("#c");
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      canvas: this.canvas,
    });
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.scene = new THREE.Scene();
    init_light(this.scene);
    this.state = state;
    this.handleStateChange = this.handleStateChange.bind(this);
    this.players = state.players;
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.pauseButton = "Escape";
    this.initializeEventListener();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.handleResize = this.handleResize.bind(this);
    window.addEventListener("resize", this.handleResize);
  }

  resetControls() {
    if (this.state.gameMode === "OnlineRight") {
      this.paddleRight.choosePlayer("player");
      this.paddleLeft.choosePlayer("none");
    } else if (this.state.gameMode === "OnlineLeft") {
      this.paddleLeft.choosePlayer("player");
      this.paddleRight.choosePlayer("none");
    } else {
      this.paddleLeft.choosePlayer(state.players.left);
      this.paddleRight.choosePlayer(state.players.right);
    }
  }

  handleStateChange() {
    if (this.state.state.gameNeedsReset === true) {
      this.resetControls();
      this.state.setGameNeedsReset(false);
      //   this.state.notifyListeners();
    }
  }

  handleResize() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const aspect = width / height;
    const frustumSize = 20;

    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(window.devicePixelRatio);

    if (this.camera?.isOrthographicCamera) {
      this.camera.left = (-frustumSize * aspect) / 2;
      this.camera.right = (frustumSize * aspect) / 2;
      this.camera.top = frustumSize / 2;
      this.camera.bottom = -frustumSize / 2;
      this.camera.updateProjectionMatrix();
    }
  }

  initializeEventListener() {
    window.addEventListener("keydown", this.handleKeyDown);
  }

  handleKeyDown(event) {
    if (!this.state.state.gameHasLoaded || !this.state.state.gameStarted)
      return;
    if (event.key === this.pauseButton) {
      this.state.togglePause();
    }
  }

  async makeArena() {
    this.state.subscribe(this.handleStateChange);
    this.arena = new Arena(this.config.getSize());
    this.paddleLeft = await updateLoadingTime(
      "Paddles",
      "Left Paddle Creation",
      async () =>
        new Paddle(this.arena, "left", this.players.left, this.config),
      10,
    );

    this.paddleRight = await updateLoadingTime(
      "Paddles",
      "Right Paddle Creation",
      async () =>
        new Paddle(this.arena, "right", this.players.right, this.config),
      10,
    );

    this.ball = await updateLoadingTime(
      "Ball",
      "Ball Creation",
      async () => new Ball(this.config.getSize(), this.config.getBallConfig()),
      5,
    );

    await this.arena.initialized;
    await this.paddleLeft.init();
    await this.paddleRight.init();
    await this.ball.init();
  }

  async makeTerrain() {
    this.terrainFactory = new TerrainFactory();
    this.terrain = this.terrainFactory.create(
      this.config.getSize(),
      this.config.getGenerationConfig("corrals"),
    );
    await this.terrain.initialized;
    this.sea = this.terrainFactory.create(
      this.config.getSize(),
      this.config.getGenerationConfig("sea"),
    );
    this.fishFactory = new FishFactory(this.terrain.geometry, this.terrain.obj);
    await this.fishFactory.initialized;
    for (let creature of this.fishFactory.creatures) {
      this.scene.add(creature.obj);
    }
    this.scene.add(this.terrain.obj);
    this.scene.add(this.sea.obj);
  }

  makeSceneGroups() {
    this.sceneToRotateWithCamera = new THREE.Group();
    this.sceneToRotateWithCamera.add(
      this.arena.obj,
      this.ball.obj,
      this.paddleLeft.obj,
      this.paddleRight.obj,
      this.ball.sparks.group,
      this.camera,
    );
    this.sceneToRotateWithCamera.position.set(0, 0, 0);
    this.scene.add(this.sceneToRotateWithCamera);
  }

  async init() {
    await this.makeArena();
    await this.makeTerrain();

    this.camera = init_camera(
      this.renderer,
      this.arena.obj,
      this.config.getCameraConfig(),
    );

    this.makeSceneGroups();

    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.render(this.scene, this.camera);

    const game = {
      ball: this.ball,
      arena: this.arena,
      paddleLeft: this.paddleLeft,
      paddleRight: this.paddleRight,
      terrain: this.terrain,
      sea: this.sea,
      fishFactory: this.fishFactory,
      players: this.players,
      sceneToRotateWithCamera: this.sceneToRotateWithCamera,
    };

    this.rendererInstance = new Renderer(
      this.renderer,
      this.scene,
      this.camera,
      game,
    );

    this.state.setGameHasLoaded();
  }
}
