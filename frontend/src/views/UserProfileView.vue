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
  <div id="reqbutton">
    <send-friend-req :receiver-username="user.username"></send-friend-req>
    <RespondFriendReq v-if="this.isCurrentUser"></RespondFriendReq>
  </div>
</template>

<script>
import SendFriendReq from "../components/SendFriendReq.vue";
import RespondFriendReq from "../components/RespondFriendReq.vue";

export default {
  components: {
    SendFriendReq,
    RespondFriendReq,
  },
  data() {
    return {
      user: null,
      photo: null,
      currentUser: null, //The logged in user
      isCurrentUser: false, //Check if userpage belongs to logged in user
    };
  },
  async created() {
    let username = this.$route.params.username;
    //Fetch currentuser
    try {
      let currentUserResponse = await fetch(`/current_user`, {
        credentials: "include",
      });
      if (currentUserResponse.ok) {
        let currentUserData = await currentUserResponse.json();
        this.currentUser = currentUserData.username;
      } else {
        console.error("Failed to fetch current user data");
      }
    } catch (error) {
      console.error("Error fetching current user data:", error);
    }
    //Fetch userprofile data
    try {
      let response = await fetch(`/api/user/username/${username}`, {
        credentials: "include",
      });
      if (response.ok) {
        this.user = await response.json();
        //If current user viewing own profile
        this.isCurrentUser = this.currentUser === username;
        console.log("isCurrentuser: ", this.isCurrentUser);
        console.log("currentUser:: ", this.currentUser);
        console.log("username: ", username);
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
  max-width: fit-content;
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
#reqbutton {
  position: absolute;
  top: 35%;
  left: 80%;
}
</style>
