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

// Make Axios instance available globally
app.config.globalProperties.$http = axiosInstance;

app.use(store).use(router).mount("#app");
