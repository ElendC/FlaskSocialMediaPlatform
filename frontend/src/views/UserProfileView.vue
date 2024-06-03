<template>
  <div>
    <h1>User Profile</h1>
    <div v-if="user">
      <p>Username: {{ user.username }}</p>
      <div v-if="user.profileImg">
        <img :src="`/store/uploads/${user.profileImg}`" alt="Profile Image" />
      </div>
      <form @submit.prevent="uploadPhoto">
        <input type="file" @change="onFileChange" />
        <button type="submit">Upload</button>
      </form>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      photo: null,
    };
  },
  async created() {
    const userId = this.$route.params.id;
    try {
      const response = await fetch(`/api/user/${userId}`, {
        credentials: "include",
      });
      if (response.ok) {
        this.user = await response.json();
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
}
</style>
