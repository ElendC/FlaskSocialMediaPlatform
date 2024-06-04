<template>
  <div v-if="user">
    <h1>{{ user.username }}</h1>
    <div v-if="user.profileImg">
      <img :src="`/store/uploads/${user.profileImg}`" alt="Profile Image" />
    </div>
    <form v-if="isCurrentUser" @submit.prevent="uploadPhoto">
      <input type="file" @change="onFileChange" />
      <button type="submit">Upload</button>
    </form>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      photo: null,
      currentUser: null, // To store the current user's username
      isCurrentUser: false, // To track if the current user is viewing their own profile
    };
  },
  async created() {
    const username = this.$route.params.username;

    // Fetch current user info
    try {
      const currentUserResponse = await fetch(`/current_user`, {
        credentials: "include",
      });
      if (currentUserResponse.ok) {
        const currentUserData = await currentUserResponse.json();
        this.currentUser = currentUserData.username;
      } else {
        console.error("Failed to fetch current user data");
      }
    } catch (error) {
      console.error("Error fetching current user data:", error);
    }

    // Fetch the user profile data
    try {
      const response = await fetch(`/api/user/username/${username}`, {
        credentials: "include",
      });
      if (response.ok) {
        this.user = await response.json();
        // Check if the current user is viewing their own profile
        this.isCurrentUser = this.currentUser === username;
      } else {
        console.error("Failed to fetch user data");
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  },
  methods: {
    onFileChange(event) {
      this.photo = event.target.files[0];
    },
    async uploadPhoto() {
      if (!this.photo) {
        alert("Please select a file");
        return;
      }

      let formData = new FormData();
      formData.append("photo", this.photo);

      try {
        let response = await fetch("/upload", {
          method: "POST",
          body: formData,
          credentials: "include",
        });

        if (response.ok) {
          let data = await response.json();
          this.user.profileImg = data.filename;
          alert("File uploaded successfully");
        } else {
          alert("File upload failed");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
        alert("File upload failed");
      }
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
}

input[type="file"] {
  margin-bottom: 10px;
}

button {
  width: 100px;
  padding: 5px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

img {
  margin-top: 10px;
  max-width: 150px;
  border-radius: 50%;
  top: 10%;
}
</style>
