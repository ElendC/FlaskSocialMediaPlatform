# How the application works


## Starting the application
1. run **app.py** file in the backend folder.
    If frontend needs to be compiled, this is how to do it:
    Step 1: cd into frontend.
    Step 2: Run the command: 'npm run lint' (This might be needed as lint check is enabled when compiling)
    Step 3: Run the command: 'npm run build'
2. If you need dummy users, run the createDummy.py file in the same folder as app.py (backend)

## Authentication
1. Authentication and Friendship logic is all stored in the auth.py file.
2. Flask_login is used.
3. Session is stored in a session cookie on register/login (Line 22 & 35 ) and removed at logout (Line 42).

# Upload profile image (Extra feature)
1. Location: '/frontend/views/UserPorfileView.vue'
2. After logging in, visit your user profile  (from nav bar).
3. Chose a file and upload.
    JS validation: Only jpg/png allowed, and max size of 2MB


WRITE HOW USERS ARE CREATED, PASSWORD REQ ETC: 
If the user tries to register a password with less than 5 characters, an Error is displayed.

## Friend requests (Extra feature)
1. A friend request can be: {'sent', 'accepted', 'declined'}
2. Send request: Visit a users profile.
3. Accept requests: Visit your own profile from the navigation bar.
4. If u1 sends request to u2, an entry in the friend_request table will be made with: FriendRequest('id', 'u1.id', 'u2.id').
   u2 will now have three options:
    * Accept -> Becomes friends, entry in Friend('id', 'u1.id', 'u2.id'), and FriendRequest entry is deleted.
    * Decline -> FriendRequest entry is deleted.
    * u2 visit u1 profile and send friend request -> same as Accept.


JS Form validation



## Database
User information is stored inside user.db
If login, session is stored in a cookie

The Status route checks if there is a active session, frontend can then be refreshed without user having to relog.








