<template>
  <nav class="navbar navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="#"
        >YourSpace <span v-if="username">Hello {{ username }} </span
        >{{ isLoggedIn }}</a
      ><!-- REMOVE {{ isLoggedIn }} -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasDarkNavbar"
        aria-controls="offcanvasDarkNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="offcanvas offcanvas-end text-bg-dark"
        tabindex="-1"
        id="offcanvasDarkNavbar"
        aria-labelledby="offcanvasDarkNavbarLabel"
      >
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Menu</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Home</a>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link class="nav-link active" :to="{ name: 'user' }"
                >YourPage</router-link
              >
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link
                class="nav-link active"
                :to="{ name: 'userprofile', params: { username: username } }"
                >Profile
              </router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" v-if="isLoggedIn" @click="logout"
                >Logout</a
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
  <div id="app">
    <div class="form-wrapper">
      <login-component
        v-if="!isLoggedIn && showLoggIn"
        @login-success="handleLoginSuccess"
        @show-register="showLoggIn = false"
      />
      <register-component
        v-if="!isLoggedIn && !showLoggIn"
        @register-success="handleRegisterSuccess"
        @show-loggin="showLoggIn = true"
      />
    </div>
  </div>

  <router-view />
</template>

<script>
import LoginComponent from "./components/LoginComp.vue";
import RegisterComponent from "./components/RegisterComp.vue";

export default {
  name: "App",
  components: {
    LoginComponent,
    RegisterComponent,
  },
  data() {
    return {
      isLoggedIn: false,
      showLoggIn: true,
      username: "",
      userId: null,
    };
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIn = true;
      this.fetchCurrentUser();
    },
    handleRegisterSuccess() {
      this.isLoggedIn = true;
    },
    logout() {
      fetch("/logout", {
        method: "POST",
        credentials: "include",
      })
        .then(() => {
          this.isLoggedIn = false;
          this.username = ""; // Clear username on logout
        })
        .catch((error) => {
          console.error("Error logging out:", error);
        });
    },

    checkLoginStatus() {
      fetch("/status", {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          this.isLoggedIn = data.logged_in;
          if (this.isLoggedIn) {
            this.fetchCurrentUser();
          }
        })
        .catch((error) => {
          console.error("Error checking login status:", error);
        });
    },
    fetchCurrentUser() {
      fetch("/current_user", {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          this.username = data.username;
          this.userId = data.id;
        })
        .catch((error) => {
          console.error("Error fetching current user:", error);
        });
    },
  },
  created() {
    this.checkLoginStatus();
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
