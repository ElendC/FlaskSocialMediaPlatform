<template>
  <div class="friend-list-container">
    <h1>Your Friends</h1>
    <div v-if="friends.length">
      <ul class="friend-list">
        <li v-for="friend in friends" :key="friend.id" class="friend-item">
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
    };
  },
  async created() {
    await this.fetchFriends();
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
  },
};
</script>

<style scoped>
.friend-list-container {
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.friend-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.friend-item {
  display: flex;
  align-items: center;
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
</style>
