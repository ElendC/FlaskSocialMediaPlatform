<template>
  <div class="user-info-cont">
    <h2>UserInfo</h2>
    <button v-if="isEditable" @click="toggleEditMode">
      {{ editMode ? "Save" : "Edit" }}
    </button>
    <div class="user-info-box">
      <div v-if="editMode">
        <p><strong>Username:</strong> {{ userInfo.username }}</p>
        <p><strong>Work:</strong> <input v-model="userInfo.work" /></p>
        <p>
          <strong>Education:</strong> <input v-model="userInfo.education" />
        </p>
        <p><strong>Hobbies:</strong> <input v-model="userInfo.hobbies" /></p>
        <p>
          <strong>Age:</strong> <input v-model="userInfo.age" type="number" />
        </p>
        <p><strong>Location:</strong> <input v-model="userInfo.location" /></p>
        <p>
          <strong>Bio:</strong> <textarea v-model="userInfo.bio"></textarea>
        </p>
      </div>
      <div v-else>
        <p><strong>Username:</strong> {{ userInfo.username }}</p>
        <p><strong>Work:</strong> {{ userInfo.work }}</p>
        <p><strong>Education:</strong> {{ userInfo.education }}</p>
        <p><strong>Hobbies:</strong> {{ userInfo.hobbies }}</p>
        <p><strong>Age:</strong> {{ userInfo.age }}</p>
        <p><strong>Location:</strong> {{ userInfo.location }}</p>
        <p><strong>Bio:</strong> {{ userInfo.bio }}</p>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      userInfo: {
        username: "Loading...",
        work: "Loading...",
        education: "Loading...",
        hobbies: "Loading...",
        age: "Loading...",
        location: "Loading...",
        bio: "Loading...",
      },
      editMode: false,
    };
  },
  props: {
    username: { type: String, required: true }, //Owner of profile
    currentUser: { type: String, required: true }, //Logged in user
  },
  computed: {
    isEditable() {
      return this.username === this.currentUser;
    },
  },
  async created() {
    await this.fetchUserInfo(this.username);
  },
  methods: {
    async fetchUserInfo(username) {
      try {
        let response = await fetch(`/api/user_info/${username}`, {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          let data = await response.json();
          this.userInfo = data;
          console.log("User info:", data);
        } else {
          console.error("Failed to fetch user info");
        }
      } catch (error) {
        console.error("Error fetching user info:", error);
      }
    },
    toggleEditMode() {
      if (this.editMode) {
        this.saveUserInfo();
      }
      this.editMode = !this.editMode;
    },
    async saveUserInfo() {
      try {
        let response = await fetch(`/api/user_info`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify(this.userInfo),
        });

        if (response.ok) {
          console.log("User info saved");
        } else {
          console.error("Failed to save user info");
        }
      } catch (error) {
        console.error("Error saving user info:", error);
      }
    },
  },
};
</script>
<style scoped>
.user-info-cont {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-family: "Arial", sans-serif;
}
h2 {
  font-size: 2.5em;
  margin-bottom: 20px;
  color: #5d6a77;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: bold;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
}
button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.3s;
}
button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}
.user-info-box {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  text-align: left;
}
p {
  font-size: 1.2em;
  color: #34495e;
  margin: 10px 0;
  font-family: "Roboto", sans-serif;
}
</style>
