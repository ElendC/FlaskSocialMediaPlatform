# Project requirements

## Technology allowed
You need to use the technology from the course.
You may only use the frameworks listed below. If you are unsure if something is allowed, please ask on Discord.

#### Backend:
Your web server should be Flask. Data should be stored either in an SQLite database or on files.
You may use the Flask-login plugin, but that is not required. If you do so, note it in your README.md.
If you want to use a Object-Relational-Mapper (ORM), you may use SQLAlchemy.

You cannot use Flask-forms or Flask-WTF or similar.

#### Frontend:
The frontend should be either pure JS or Vue.
You may use plugins like Vuex or Vue-Router in Vue.
You may use the Lodash JS library.
You may use all buildin JS APIs.
You may use use either Vue version 2 or 3.

You are not allowed to use a different JS Framework like React.

You may use additional JS libraries for achieving extra functionality, e.g. showing graphs, or similar. 
Ask on discord, and mention what is used and for what in your README.

You can use Node.js and Webpack or Vite to create your Vue application. 
However, in this case, you need to build your application and include the final js files in you Flask application such that we do not have to run Node.js to run your project.
You still have to include your source code on github.
Also note that I do only have limited ability to help you with these tools.

## Functional requirements
The following are the functional requirements which build the bases for grading your project.
You can omit some features, but this will effect grading.

### AJAX and REST API

You are free to implement a Single page application (SPA) or an application with multiple routes using Flask templates.

However, some part of your application needs to be implemented using AJAX calls.
The naming of routes in your flask application should follow REST API principles.
You can deviate from this is you have good reasons.
If you do not implement an SPA, you need to use AJAX calls a place it makes sense.

For maximum score, your application must be well-organized and separated into components, or base templates, ...


### Data items
Besides users, the database or files should contain at least two types of data objects, e.g. two tables. Thus, with users, you need 3 types of data!
The application should allow to add, delete, and update some of the data stored.

Some of these operations should require specific authorization, e.g., not every user is allowed to delete every item.

### Data collection display
The frontend must contain functionality to display a collection of items.
There should be functionality to **filter**, or **sort**.
*Preferences on sorting or filtering should be stored*, to be present when the user revisits the site. (May be stored in cookies or similar.)

### Validation
Forms for login, registration, adding and updating data items should be validated.
Validation should be done both in JS and on the server side.
If validation fails, a meaningful error message must be displayed.

You should also use appropriate HTTP error codes.

Similar, if AJAX requests fail, due to server side validation, meaningful errors should be displayed.

