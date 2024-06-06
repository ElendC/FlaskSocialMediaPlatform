<template>
  <div class="profile-page">
    <header v-if="this.user">
      <h1>{{ user.username }}</h1>
      <div>
        <img :src="profileImgUrl" alt="Profile Image" class="profile-img" />
      </div>
      <form v-if="isCurrentUser" @submit.prevent="uploadPhoto">
        <input type="file" @change="onFileChange" />
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <button type="submit">Upload</button>
      </form>
    </header>

    <main>
      <user-info
        v-if="user && currentUser"
        :username="user.username"
        :currentUser="currentUser"
      ></user-info>
    </main>

    <aside class="sidebar">
      <send-friend-req
        v-if="!this.isCurrentUser && this.user"
        :receiver-username="user.username"
      ></send-friend-req>
      <div id="reqbutton">
        <RespondFriendReq v-if="this.isCurrentUser"></RespondFriendReq>
      </div>
      <div id="friendlist">
        <button @click="toggleFriendList">Friend list</button>
        <FriendList v-if="showFriendList"></FriendList>
      </div>
    </aside>
  </div>
</template>

<script>
import SendFriendReq from "../components/SendFriendReq.vue";
import RespondFriendReq from "../components/RespondFriendReq.vue";
import FriendList from "../components/FriendList.vue";
import UserInfo from "../components/UserInfo.vue";

export default {
  components: {
    SendFriendReq,
    RespondFriendReq,
    FriendList,
    UserInfo,
  },
  data() {
    return {
      user: null,
      photo: null,
      currentUser: null, //The loggedin user
      isCurrentUser: false, //Check if loggedin user owns page
      isFriend: false,
      showFriendList: false,
      defaultImg: "../store/uploads/default.jpg",
      errorMessage: "",
      profileImgUrl: "", //URL for the profile image
    };
  },
  async created() {
    await this.fetchUserData();
  },
  watch: {
    "$route.params.username": "fetchUserData",
  },
  methods: {
    async fetchUserData() {
      // Fetch current user
      let username = this.$route.params.username;
      try {
        let currentUserResponse = await fetch(`/current_user`, {
          credentials: "include",
        });
        if (currentUserResponse.ok) {
          let currentUserData = await currentUserResponse.json();
          this.currentUser = currentUserData.username;
          console.log("Current user is: ", this.currentUser);
        } else {
          console.error("Failed to fetch current user data");
        }
      } catch (error) {
        console.error("Error fetching current user data:", error);
      }

      // Fetch user profile data
      try {
        let response = await fetch(`/api/user/username/${username}`, {
          credentials: "include",
        });
        if (response.ok) {
          this.user = await response.json();
          this.isCurrentUser = this.currentUser === username;
          this.updateProfileImgUrl(); // Update the profile image URL
          this.checkFriendStatus();
        } else {
          console.error("Failed to fetch user data");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    updateProfileImgUrl() {
      //If user has profile img, and uploads a new one. So no need refresh
      if (this.user && this.user.profileImg) {
        this.profileImgUrl = `/store/uploads/${
          this.user.profileImg
        }?t=${new Date().getTime()}`;
      } else {
        this.profileImgUrl = this.defaultImg;
      }
    },
    onFileChange(event) {
      this.photo = event.target.files[0];
    },
    async uploadPhoto() {
      if (!this.photo) {
        this.errorMessage = "Please select a file";
        return;
      }

      let validTypes = ["image/jpeg", "image/png"];
      let maxSize = 2097152;
      if (!validTypes.includes(this.photo.type)) {
        this.errorMessage = "Invalid file type. only jpeg or png.";
        return;
      }
      if (this.photo.size > maxSize) {
        this.errorMessage = "Img is too large, max 2MB";
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
          await this.fetchUserData();
          this.errorMessage = "";
        } else {
          this.errorMessage = "Failed to upload image";
        }
      } catch (error) {
        console.error("Error uploading file:", error);
        this.errorMessage = "File upload failed";
      }
    },
    async checkFriendStatus() {
      try {
        let response = await fetch("/api/friends", {
          method: "GET",
          credentials: "include",
        });
        let friendData = await response.json();
        console.log("friendlist:", friendData);
      } catch (error) {
        console.error("Error fetching friend list:", error);
      }
    },
    toggleFriendList() {
      this.showFriendList = !this.showFriendList;
    },
  },
};
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}
header {
  text-align: center;
  margin-bottom: 20px;
}
.sidebar {
  position: absolute;
  left: 0px;
  top: 60px;
  max-width: 300px;
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
#friendlist {
  margin-top: 20px;
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
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 10px 0;
  display: flex;
  align-items: center;
}
.profile-img {
  width: 160px;
  height: 170px;
  border-radius: 50%;
  margin-right: 10px;
}
.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}
</style>
