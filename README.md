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
4. Errors are displayed for all register and login errors.

## UserProfileView
### Uploading Image
1. After logging in, visit your user profile  (from nav bar).
2. Can **upload png/jpeg image** with max size of 2MB, both front and backend validation.

### User Information
1. Userinfo can be **edited** only when logged in user is the owner of the profile.
2. Users can visit eachothers profiles, but wont be able to edit anything.
3. When updating information, real time check will tell user if changes are valid.

### Friend logic stuff
1. Friendlist is on the left side of the page.
2. Friends can be deleted by pressing edit.
3. Friends profiles can be visited by clicking on their profile picture or name.
4. A friend request can be: {'sent', 'accepted', 'declined'}
5. Send request: Visit a users profile.
6. Accept requests: Visit your own profile from the navigation bar.
7. If u1 sends request to u2, an entry in the friend_request table will be made with: FriendRequest('id', 'u1.id', 'u2.id').
   u2 will now have three options:
    * Accept -> Becomes friends, entry in Friend('id', 'u1.id', 'u2.id'), and FriendRequest entry is deleted.
    * Decline -> FriendRequest entry is deleted.
    * u2 visit u1 profile and send friend request -> same as Accept.












