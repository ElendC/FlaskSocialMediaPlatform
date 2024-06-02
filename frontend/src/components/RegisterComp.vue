<template>
  <div>
    <h2 class="h2Auth">Register</h2>
    <form @submit.prevent="register" class="formAuth">
      <input v-model="username" placeholder="Username" required />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />
      <button type="submit" class="buttonAuth">Register</button>
    </form>
    <h5>
      Already have an account?
      <span class="highlightText" @click="showLoggIn">Login here </span>
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
    register() {
      this.$http
        .post("/register", {
          username: this.username,
          password: this.password,
        })
        .then(() => {
          this.$emit("register-success");
          this.$router.push({ name: "user" });
        })
        .catch(() => {
          alert("Registration failed");
        });
    },
    showLoggIn() {
      this.$emit("show-loggin");
    },
  },
};
</script>
