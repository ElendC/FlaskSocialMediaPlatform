<template>
  <div>
    <button v-if="!isPending && !accepted" @click="SendFriendRequest">
      Befriend This Person
    </button>
    <button v-if="isPending && !accepted">Pending request</button>
    <h2>Friends :)</h2>
    <h2>receiver: {{ receiverUsername }}</h2>
    <h3>{{ this.isPending }}</h3>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isPending: false,
      accepted: false,
    };
  },
  props: {
    receiverUsername: {
      type: String,
      required: true,
    },
  },
  async created() {
    this.checkFriendRequestStatus();
  },

  methods: {
    async SendFriendRequest() {
      try {
        //Sending receiver name to the backend
        let response = await fetch("/api/friend_request/send", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ receiver_username: this.receiverUsername }),
          credentials: "include",
        });
        let data = await response.json();
        alert(data.message);
        console.log("receiverUsername: ", this.receiverUsername);
      } catch (error) {
        console.error("Error sending friend request:", error);
        alert("Error sending friend request");
      }
    },
    async checkFriendRequestStatus() {
      try {
        console.log("Hello this is pending: ", this.isPending);
        let response = await fetch("/api/friend_requests", {
          method: "GET",
          credentials: "include",
        });
        let data = await response.json();

        console.log("Sent friend requests:", data.sent_requests);

        //Checks if friend request already sent. Returns true if one match
        this.isPending = data.sent_requests.some(
          (req) => req.receiver_username === this.receiverUsername
        );
        console.log("Hello this is pending: ", this.isPending);
      } catch (error) {
        console.error("Error checking friend request status:", error);
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

input {
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
}

button {
  padding: 8px;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
