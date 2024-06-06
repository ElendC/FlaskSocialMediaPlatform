<template>
  <div class="friend-list-container">
    <h1>Your Friends</h1>
    <button class="edit-button" @click="toggleEdit">
      {{ editMode ? "Done" : "Edit" }}
    </button>
    <div v-if="friends.length">
      <ul class="friend-list">
        <li v-for="friend in friends" :key="friend.id" class="friend-item">
          <router-link
            :to="{ name: 'userprofile', params: { username: friend.username } }"
            class="nav-link active"
          >
            <img
              :src="
                friend.profileImg
                  ? `/store/uploads/${friend.profileImg}`
                  : defaultImg
              "
              alt="Profile Image"
              class="profile-img"
            />
            <span>{{ friend.username }}</span>
          </router-link>
          <button
            @click="deleteFriend(friend.username)"
            v-if="editMode"
            class="remove-friend"
          >
            ✖
          </button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>You have no friends yet :/</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      friends: [],
      defaultImg: "../store/uploads/default.jpg",
      editMode: false,
    };
  },
  async created() {
    await this.fetchFriends();
  },
  watch: {
    "$route.params.username": "fetchFriends",
  },
  methods: {
    async fetchFriends() {
      try {
        let response = await fetch("/api/friends", {
          credentials: "include",
        });
        let data = await response.json();
        // console.log(data);
        this.friends = data;
      } catch (error) {
        console.error("Error fetching friends:", error);
      }
    },
    toggleEdit() {
      this.editMode = !this.editMode;
    },
    async deleteFriend(friendId) {
      try {
        let response = await fetch("/api/friends/delete", {
          method: "DELETE",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ friend_username: friendId }),
        });

        if (response.ok) {
          let data = await response.json();
          console.log("Friend deleted", data);
          await this.fetchFriends();
        } else {
          console.error("failed to delete");
        }
      } catch (error) {
        console.error("Error deleting: ", error);
      }
    },
  },
};
</script>

<style scoped>
.friend-list-container {
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}
.friend-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}
.friend-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: white;
  transition: background-color 0.3s, box-shadow 0.3s;
}
.friend-item:hover {
  background-color: #f1f1f1;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
.friend-item span {
  font-size: 16px;
  font-weight: 500;
}
.remove-friend {
  cursor: pointer;
  color: red;
  font-weight: bold;
  background: none;
  border: none;
  font-size: 20px;
  position: relative;
}
.remove-friend::after {
  content: "Delete";
  visibility: hidden;
  opacity: 0;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  padding: 5px;
  position: absolute;
  bottom: 125%; /* Position above the button */
  left: 50%;
  transform: translateX(-50%);
  transition: opacity 0.3s;
  font-size: 12px;
}
.remove-friend:hover::after {
  visibility: visible;
  opacity: 1;
}
.edit-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 16px;
}
.edit-button:hover {
  background-color: #00db0b;
}
</style>
