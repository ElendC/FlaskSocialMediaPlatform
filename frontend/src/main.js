import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "./assets/custom.css";

// Create Axios instance
const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5000",
  withCredentials: true,
});

const app = createApp(App);

//Make axios instance available globally
app.config.globalProperties.$http = axiosInstance;

const isAuthenticated = async () => {
  try {
    let response = await fetch("/status", {
      credentials: "include",
    });
    let data = await response.json();
    return data.logged_in;
  } catch (error) {
    console.error("Error checking login stat", error);
    return false;
  }
};

export { isAuthenticated };
app.use(store).use(router).mount("#app");
