<template>
  <div>
    <div v-if="friendRequests.length">
      <p>Friend requests</p>
      <ul>
        <li v-for="request in friendRequests" :key="request.id">
          {{ request.sender_username }}
          <button @click="respondToRequest(request.id, 'accept')">
            Accept
          </button>
          <button @click="respondToRequest(request.id, 'decline')">
            Decline
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      friendRequests: [],
    };
  },
  async created() {
    await this.fetchFriendRequests();
  },
  methods: {
    async fetchFriendRequests() {
      try {
        let response = await fetch("/api/friend_requests", {
          credentials: "include",
        });
        let data = await response.json();
        this.friendRequests = data.received_requests;
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      }
    },
    async respondToRequest(requestId, action) {
      try {
        let response = await fetch("/api/friend_request/respond", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ request_id: requestId, action }),
          credentials: "include",
        });
        let data = await response.json();
        alert(data.message);
        await this.fetchFriendRequests(); // Refresh the friend requests list
      } catch (error) {
        console.error(`Error responding to friend request: ${error}`);
        alert("Error responding to friend request");
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
}

button {
  margin-left: 10px;
  padding: 5px;
  font-size: 14px;
  cursor: pointer;
}

button:first-of-type {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
}

button:first-of-type:hover {
  background-color: #45a049;
}

button:last-of-type {
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
}

button:last-of-type:hover {
  background-color: #e53935;
}
</style>
