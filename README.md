# Organizing your Big Green Egg


## A web application that will help you plan out your cooks on the BGE

This is a CRUD application that will allow a user to create an account that will store what they have planned to cook on their BGE by keeping track of the temperature they are cooking at and what accessories are used on the egg. The matching feature can even help find recipes to match the temperature you're cooking at and whether you are cooking directly or indirectly.

You can even use your own recipes by replacing the file recipes.txt in the recipe_data folder using the syntax:
Recipe Name | Cook Temps Separated by Whitespace | Is an Entree True/False | Cooking Method direct/indirect/both | Reference to Recipe

Then you can run the program orm_transfer.py to add the new recipes to the recipe_table in eggs.db and you've successfully added you're favorite recipes to the system.
