import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import UserView from "../views/UserView.vue";
import { isAuthenticated } from "../main.js";
import UserProfileView from "../views/UserProfileView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: AboutView,
  },
  {
    path: "/user",
    name: "user",
    component: UserView,
    meta: { requiresAuth: true },
  },
  {
    path: "/user/:id",
    name: "userprofile",
    component: UserProfileView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach(async (to) => {
  if (
    //Authentication check
    to.matched.some((record) => record.meta.requiresAuth) &&
    !(await isAuthenticated()) &&
    //To avoid inf loop
    to.name !== "about"
  ) {
    //If trying to access without authentication
    return { name: "about" };
  }
});

export default router;
