<template>
  <nav class="navbar navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">YourSpace</a>
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
          <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">
            Dark offcanvas
          </h5>
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
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#"
                >YourPage</a
              >
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
  <h1>IsloggedIn: {{ isLoggedIn }}</h1>
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
    <button v-if="isLoggedIn" @click="logout">Logout</button>
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
    };
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIn = true;
    },
    handleRegisterSuccess() {
      this.isLoggedIn = true;
    },
    logout() {
      this.$http.post("/logout").then(() => {
        this.isLoggedIn = false;
      });
    },
    checkLoginStatus() {
      this.$http.get("/status").then((response) => {
        this.isLoggedIn = response.data.logged_in;
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
