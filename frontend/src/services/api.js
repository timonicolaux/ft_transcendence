import axios from "axios";
import state from "../app.js";
import { router } from "../app.js";
// import https from "https";

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;

const API = axios.create({
  // baseURL: API_BASE_URL,
  baseURL: "https://10.13.11.1:8443/api",
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
  // httpsAgent: new https.Agent({
  //   rejectUnauthorized: false,
  // }),
});

async function getNewAccessToken() {
  console.log("Getting new access token");
  try {
    const response = await API.post(`/auth/custom-token/access/`);
    const data = response.data.user;
    state.state.lang = data.lang;
    state.state.userId = data.id.toString();
    state.state.username = data.username;
    state.state.userAlias = data.alias;
    state.saveState();
  } catch (error) {
    state.setIsUserLoggedIn(false);
    console.error(`Error while trying to get new access token : ${error}`);
    throw error;
  }
}

let isRetrying = false;

API.interceptors.response.use(
  (response) => response, // Laisser passer les réponses réussies
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 500) {
      router.navigate("/500");
      return Promise.reject(error);
    }
    if (error.response.status === 401 && window.location.pathname === "/login")
      return Promise.reject(error);
    if (error.response.status === 401) {
      if (isRetrying) {
        setTimeout(() => {
          if (
            window.location.pathname !== "/" &&
            window.location.pathname !== "/login" &&
            window.location.pathname !== "/register" &&
            window.location.pathname !== "/game" &&
            window.location.pathname !== "/local-tournament" &&
            window.location.pathname !== "/rules"
          ) {
            router.navigate("/login");
          }
        }, 100);
        isRetrying = false;
        return Promise.reject(error);
      }
      isRetrying = true;
      console.error("Error 401, will try to get new access token");
      try {
        await getNewAccessToken();
        state.setIsUserLoggedIn(true);
        isRetrying = false;
        return API(originalRequest);
      } catch (tokenError) {
        console.error("Token refresh failed:", tokenError);
        return Promise.reject(tokenError);
      }
    }
    return Promise.reject(error);
  },
);

export default API;
