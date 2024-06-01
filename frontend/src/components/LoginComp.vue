<template>
  <div>
    <h2 class="h2Auth">Login</h2>
    <form @submit.prevent="login" class="formAuth">
      <input v-model="username" placeholder="Username" required />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />
      <button type="submit" class="buttonAuth">Login</button>
    </form>
    <h5>
      Don't have an account?
      <span class="highlightText" @click="showRegister">register here</span>
    </h5>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    login() {
      this.$http
        .post("/login", {
          username: this.username,
          password: this.password,
        })
        .then(() => {
          this.$emit("login-success");
        })
        .catch(() => {
          alert("Login failed");
        });
    },
    showRegister() {
      this.$emit("show-register");
    },
  },
};
</script>
