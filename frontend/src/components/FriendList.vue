<template>
  <div>
    <h1>Your Friends</h1>
    <div v-if="friends.length">
      <ul>
        <li v-for="friend in friends" :key="friend.id">
          <img
            :src="`/store/uploads/${friend.profileImg}`"
            alt="Profile Image"
            class="profile-img"
          />
          {{ friend.username }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>You have no friends yet.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      friends: [],
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
        this.friends = data;
      } catch (error) {
        console.error("Error fetching friends:", error);
      }
    },
  },
};
</script>

<style scoped>
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
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
</style>
