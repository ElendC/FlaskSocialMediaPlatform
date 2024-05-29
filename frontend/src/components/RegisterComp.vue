<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />
      <button type="submit">Register</button>
    </form>
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
        })
        .catch(() => {
          alert("Registration failed");
        });
    },
  },
};
</script>
