<template>
  <div id="app">
    <h1>Login/Register</h1>
    <login-component v-if="!isLoggedIn" @login-success="handleLoginSuccess" />
    <register-component
      v-if="!isLoggedIn"
      @register-success="handleRegisterSuccess"
    />
    <button v-if="isLoggedIn" @click="logout">Logout</button>
  </div>
</template>

<script>
import LoginComponent from "../components/LoginComp.vue";
import RegisterComponent from "../components/RegisterComp.vue";

export default {
  name: "App",
  components: {
    LoginComponent,
    RegisterComponent,
  },
  data() {
    return {
      isLoggedIn: false,
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
