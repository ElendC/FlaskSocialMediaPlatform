<template>
  <div>
    <h1>User Profile</h1>
    <p v-if="username">Username: {{ username }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
    };
  },
  created() {
    this.fetchCurrentUser();
  },
  methods: {
    fetchCurrentUser() {
      this.$http
        .get("/current_user")
        .then((response) => {
          this.username = response.data.username;
        })
        .catch(() => {
          console.error("Error fetching current user");
        });
    },
  },
};
</script>
