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
<!-- async fetchAllUsers() {
  try {
    let response = await fetch("/api/users", {
      credentials: "include",
    });
    if (response.ok) {
      let data = await response.json();
      console.log("All users:", data);
      // Update your state or do something with the data
    } else {
      console.error("Failed to fetch users");
    }
  } catch (error) {
    console.error("Error fetching users:", error);
  }
} -->
