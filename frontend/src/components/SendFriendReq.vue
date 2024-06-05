<template>
  <div>
    <button v-if="!isPending && !accepted" @click="SendFriendRequest">
      Befriend This Person
    </button>
    <button v-if="isPending && !accepted">Pending request</button>
    <h2 v-else>Friends :)</h2>
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
    console.log("Initial receiver: ", this.receiverUsername);
    this.checkFriendRequestStatus();
    console.log("After checkFriendReq receiver: ", this.receiverUsername);
  },
  methods: {
    async SendFriendRequest() {
      try {
        let response = await fetch("/api/friend_request/send", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ receiver_username: this.receiverUsername }),
          credentials: "include",
        });
        let data = await response.json();
        alert(data.message);

        // Check the status again after sending the request
        await this.checkFriendRequestStatus();
      } catch (error) {
        console.error("Error sending friend request:", error);
        alert("Error sending friend request");
      }
    },
    async checkFriendRequestStatus() {
      try {
        // console.log("Receiver username prop:", this.receiverUsername);

        let response = await fetch("/api/friend_requests", {
          method: "GET",
          credentials: "include",
        });
        let data = await response.json();

        // console.log("Data fetched: ", data);
        // console.log("Sent friend requests fetched:", data.sent_requests);

        this.isPending = data.sent_requests.some(
          (req) => req.receiver_username === this.receiverUsername
        );
        // console.log("Pending status: ", this.isPending);

        let friendsResponse = await fetch("/api/friends", {
          method: "GET",
          credentials: "include",
        });
        let friendsData = await friendsResponse.json();
        // console.log("Friends data fetched: ", friendsData);

        this.accepted = friendsData.some(
          (friend) => friend.username === this.receiverUsername
        );
        // console.log("Friend status: ", this.accepted);
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
