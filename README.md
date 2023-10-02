# Grocery Lister
Grocery Lister is a CLI app to help you plan your meals and make your shopping list. First you have a pantry which represents the food you already have in your house. There is full CRUD any pantry item.

There is also a digital recipe book, which can the user can customize with their own recipes that they like to make (once again with full CRUD).

The majority of the functionality of the app is in the Meal Plans sub-menu. There the user can make meal plans, which can include multiple recipes, for each week. Once they have their meal plans for the week they can automatically generate a grocery list, which will account for what is already in their pantry. Once the grocery list is made, the user can view and edit it at any time, and, whenever they choose they can add the entire list to their pantry. Finally the user has the option to remove all the ingredients a meal plan requires from the pantry with a single action. 

## Running the Program
In order run the program, navigate to the project folder in CLI and run 
```bash
pipenv install
pipenv shell
python3 lib/cli.py
```