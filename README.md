# How the application works

## Authentication
Check backend->auth.py
User information is stored inside user.db
If login, session is stored in a cookie

The Status route checks if there is a active session, frontend can then be refreshed without user having to relog.










  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav>