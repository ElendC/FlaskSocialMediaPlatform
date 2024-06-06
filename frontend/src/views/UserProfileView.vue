<template>
  <div class="profile-page">
    <header v-if="this.user">
      <h1>{{ user.username }}</h1>
      <div>
        <img
          :src="
            user.profileImg ? `/store/uploads/${user.profileImg}` : defaultImg
          "
          alt="Profile Image"
          class="profile-img"
        />
      </div>
      <form v-if="isCurrentUser" @submit.prevent="uploadPhoto">
        <input type="file" @change="onFileChange" />
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <button type="submit">Upload</button>
      </form>
    </header>

    <main></main>

    <aside class="sidebar">
      <div id="reqbutton">
        <send-friend-req
          v-if="!this.isCurrentUser && this.user"
          :receiver-username="user.username"
        ></send-friend-req>
        <RespondFriendReq v-if="this.isCurrentUser"></RespondFriendReq>
      </div>
      <div id="friendlist">
        <button @click="toggleFriendList">Show friend list</button>
        <FriendList v-if="showFriendList"></FriendList>
      </div>
    </aside>
  </div>
</template>

<script>
import SendFriendReq from "../components/SendFriendReq.vue";
import RespondFriendReq from "../components/RespondFriendReq.vue";
import FriendList from "../components/FriendList.vue";

export default {
  components: {
    SendFriendReq,
    RespondFriendReq,
    FriendList,
  },
  data() {
    return {
      user: null,
      photo: null,
      currentUser: null, //The logged in user
      isCurrentUser: false, //Check if userpage belongs to logged in user
      isFriend: false,
      showFriendList: false,
      defaultImg: "../store/uploads/default.jpg",
      errorMessage: "",
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
      //Fetch currentuser
      let username = this.$route.params.username;
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
          console.log("line 75: ", this.user.username);
          //If current user viewing own profile
          this.isCurrentUser = this.currentUser === username;
          // console.log("isCurrentuser: ", this.isCurrentUser);
          // console.log("currentUser:: ", this.currentUser);
          // console.log("username: ", username);
          this.checkFriendStatus();
        } else {
          console.error("Failed to fetch user data");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
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
      //VALIDATION START: comment out for backend validation testing
      let validTypes = ["image/jpeg", "image/png"];
      let maxSize = 2097152;
      if (!validTypes.includes(this.photo.type)) {
        this.errorMessage = "Invalid file type. only jpeg or png.";
        console.log("INVALID TYPE");
        return;
      }
      if (this.photo.size > maxSize) {
        this.errorMessage = "Img is to large, max 2MB";
        console.log("INVALID SIZE");
        return;
      }
      //VALIDATION END: comment out for backend validation testing

      let formData = new FormData();
      formData.append("photo", this.photo);

      try {
        console.log("TRYING TO FETCH");
        let response = await fetch("/upload", {
          method: "POST",
          body: formData,
          credentials: "include",
        });

        if (response.ok) {
          console.log("RESPONSE IS OK");
          let data = await response.json();
          this.user.profileImg = data.filename;
          this.errorMessage = "";
        } else {
          console.log("RESPOONSE FAILED");
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
        console.error("Error fetching friend list: ", error);
      }
    },
    toggleFriendList() {
      if (!this.showFriendList) {
        this.showFriendList = true;
      } else {
        this.showFriendList = false;
      }
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
  right: 20px;
  top: 110px;
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
