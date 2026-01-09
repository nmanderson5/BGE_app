# Organizing your Big Green Egg

#### Video Demo: 

## A web application that will help you plan out your cooks on the BGE

This is a CRUD application that will allow a user to create an account that will store what they have planned to cook on their BGE by keeping track of the temperature they are cooking at and what accessories are used on the egg. The matching feature can even help find recipes to match the temperature you're cooking at and whether you are cooking directly or indirectly.

## Adding Recipes to the database

You can even use your own recipes by replacing the file recipes.txt in the recipe_data folder using the syntax: <br>
Recipe Name | Cook Temps Separated by Whitespace | Is an Entree True/False | Cooking Method direct/indirect/both | Reference to Recipe

Then you can run the program orm_transfer.py to add the new recipes to the recipe_table in eggs.db and you've successfully added you're favorite recipes to the system. This program will separate the information about the recipes using | and create an instance of the Recipe class to then add to eggs.db with SQLAlchemy.

## The HTML files

When you first visit the webpage you will be brought to index.html which is the homepage for users not logged in. This will prompt you to login or register with a username and password and will reprompt you with an error message if you try to register a username already in use or register/login while only filling in one of the fields. Once logged in you will be taken to dashboard.html which will display your Egg's current layout of accessories and food. You can change the accessories using dropdown menus at the top and can change the temperature setting in the middle, with a button to reset to the default empty settings. You will also find a button for Match Egg that will find recipes based on your Egg's current temperature, whether it's cooking directly, indirectly or both, and display the results on results.html. You could also follow the link to browse recipes from your dashboard to browse.html where you can enter the temperature, method of cooking (direct, indirect, both), whether or not it's an entree, and optionally a keyword for the name. This will also take you to results.html, and from here you can choose to add any of these recipes to your Egg, it will be updated and send you back to your dashboard. All of these html files are generated over the template of layout.html which just has some basic header information.

## The Python running the show

Most of the heavy lifting for this web app is done by project.py using the different app.route's to handle the requests and render the templates while also communicating with the SQLite databases. They also do error checking to ensure that even adversarial users cannot confuse the app with strange inputs by changing the HTML and SQLAlchemy escapes inputs to the database to prevent injection attacks. There are also some helper functions at the top to transform the inputs from the forms on the web pages into what the database expects.

## The Tests

These are tests of some helper functions in test_units.py to ensure they work as expected and the tests in test_functional.py check several routes to see that they work as expected with some test inputs like creating a user and logging them in as well as the browse route with a test search.
