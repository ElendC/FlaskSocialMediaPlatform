<template>
  <div class="explore-container">
    <header>
      <h1>Explore People's Spaces</h1>
    </header>
    <main>
      <div class="search-sort-container">
        <input
          v-model="searchUser"
          placeholder="Search by education"
          @input="searchUsers"
        />
        <button @click="sortByAge">Sort by Age</button>
      </div>
      <ul v-if="listUsers.length">
        <li v-for="user in listUsers" :key="user.username" class="user-item">
          <router-link
            :to="{ name: 'userprofile', params: { username: user.username } }"
          >
            <img
              :src="
                user.profileImg
                  ? `/store/uploads/${user.profileImg}`
                  : defaultImg
              "
              alt="Profile Image"
              class="profile-img"
            />

            <div class="user-details">
              <p><strong>Username:</strong> {{ user.username }}</p>
              <p><strong>Age:</strong> {{ user.age }}</p>
              <p><strong>Education:</strong> {{ user.education }}</p>
            </div>
          </router-link>
        </li>
      </ul>
      <p v-else>No users found</p>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      listUsers: [],
      defaultImg: "../store/uploads/default.jpg", // Default profile image
      searchUser: "", // Search query for education
      sortAsc: true, // Flag for sorting order
    };
  },
  created() {
    this.fetchCurrentUser();
  },
  watch: {
    username(newUsername) {
      this.loadSearchParameter(newUsername);
    },
  },
  methods: {
    async fetchCurrentUser() {
      try {
        let response = await fetch("/current_user", {
          credentials: "include",
        });
        if (response.ok) {
          let data = await response.json();
          this.username = data.username;
        } else {
          console.error("Failed to fetch current user");
        }
      } catch (error) {
        console.error("Error fetching current user:", error);
      }
    },
    async searchUsers() {
      if (this.searchUser.trim() === "") {
        this.listUsers = [];
        sessionStorage.removeItem(`${this.username}_searchUser`);
        return;
      }

      try {
        let response = await fetch("/api/users_by_education", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ education: this.searchUser }),
        });

        if (response.ok) {
          let data = await response.json();
          let userPromises = data.map((user) =>
            this.fetchUserInfo(user.username)
          );
          let usersInfo = await Promise.all(userPromises);
          this.listUsers = usersInfo;
          sessionStorage.setItem(
            `${this.username}_searchUser`,
            this.searchUser
          );
        } else {
          console.error("Failed to fetch users");
          this.listUsers = [];
        }
      } catch (error) {
        console.error("Error fetching users:", error);
        this.listUsers = [];
      }
    },
    async fetchUserInfo(username) {
      try {
        let response = await fetch(`/api/user_info/${username}`, {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          let data = await response.json();
          return data;
        } else {
          console.error("Failed to fetch user info for", username);
          return {
            username: username,
            profileImg: null,
            age: "N/A",
            education: "N/A",
          };
        }
      } catch (error) {
        console.error("Error fetching user info:", error);
        return {
          username: username,
          profileImg: null,
          age: "N/A",
          education: "N/A",
        };
      }
    },
    sortByAge() {
      this.listUsers.sort((a, b) => {
        if (this.sortAsc) {
          return a.age - b.age;
        } else {
          return b.age - a.age;
        }
      });
      this.sortAsc = !this.sortAsc;
    },
    loadSearchParameter(username) {
      const savedSearch = sessionStorage.getItem(`${username}_searchUser`);
      if (savedSearch) {
        this.searchUser = savedSearch;
        this.searchUsers();
      }
    },
  },
};
</script>

<style scoped>
.explore-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-family: "Arial", sans-serif;
}
header {
  text-align: center;
  margin-bottom: 20px;
}
.search-sort-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  margin-right: 10px;
  width: 300px;
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
ul {
  list-style-type: none;
  padding: 0;
}
.user-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}
.user-item:hover {
  background-color: #f1f1f1;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}
.profile-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 20px;
  object-fit: cover;
}
.user-details {
  text-align: left;
}
.user-details p {
  margin: 5px 0;
  font-size: 1.2em;
  color: #34495e;
  font-family: "Roboto", sans-serif;
}
</style>
