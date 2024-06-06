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
      <p v-if="errorMessg" class="error-message">{{ errorMessg }}</p>
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
      errorMessg: "",
    };
  },
  methods: {
    //VALIDATE START: comment out for backend test
    validateRegister() {
      this.errorMessg = "";
      if (this.username.length < 2 || this.username.length > 5) {
        this.errorMessg =
          "Username needs to be between 2 and 5 characters long!";
        return false;
      }
      if (this.password.length < 1 || this.password.length > 10) {
        this.errorMessg = "Password should be between 1-10 characters";
        return false;
      }
      return true;
    },
    //VALIDATE END: comment out for backend test
    async register() {
      let errorValidating = this.validateRegister();
      if (errorValidating) {
        try {
          let response = await this.$http.post("/register", {
            username: this.username,
            password: this.password,
          });
          if (response.status === 200) {
            this.errorMessg = "";
            this.$emit("register-success");
            this.$router.push({ name: "user" });
          } else {
            this.errorMessg = response.data.message || "Registration failed";
          }
        } catch (error) {
          if (
            error.response &&
            error.response.data &&
            error.response.data.message
          ) {
            this.errorMessg = error.response.data.message;
          } else {
            console.error("Registration failed", error);
            this.errorMessg = "Registration failed";
          }
        }
      }
    },
    showLoggIn() {
      this.$emit("show-loggin");
    },
  },
};
</script>
