# lib/cli.py
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base, validates
from models.models import (Item, Pantry_item, List, List_item, Week, Meal_plan, Meal_plan_recipe, Recipe, Ingredient_item, Base)
import inquirer


engine = create_engine('sqlite:///grocery_lister.db')
Base.metadata.create_all(engine)


def main():
    with Session(engine) as session:
        #home menu
        def home_menu():
            questions = [
                inquirer.List(
                    "chosen_menu",
                    message = "Welcome to Grocery Lister, what would you like to do",
                    choices = [
                        "View your Meal Plans",
                        "View your Pantry",
                        "View your Recipes",
                        "Exit"
                    ]
                )
            ]
            response = inquirer.prompt(questions)
            if response["chosen_menu"] == "View your Meal Plans":
                view_week_menu()
            elif response["chosen_menu"] == "View your Pantry":
                view_pantry()
            elif response["chosen_menu"] == "View your Recipes":
                view_recipes()
            else:
                exit()
        

################### View and edit a week's menus+ functionality ####################### 
        # select a week to view menu
        def view_week_menu():
            week_list = session.query(Week).all()
            # week_list.append("Return to main menu")
            questions = [
                inquirer.List(
                    "week",
                    message = "Select a week",
                    choices = ["New week"]+week_list+["Return to main menu"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["week"] == "Return to main menu":
                home_menu()
            elif answer["week"] == "New week":
                # make a new week starting on that date, and generates a meal plan for each day of that week
                new_week_date = input("What is the first day (the sunday) of the new week? ")
                new_week = Week(start_week = new_week_date)
                # print(new_week.id)
                session.add(new_week)
                session.commit()
                # print(new_week.id)
                sun = Meal_plan(day = "Sunday", week_id = new_week.id)
                mon = Meal_plan(day = "Monday", week_id = new_week.id)
                tue = Meal_plan(day = "Tuesday", week_id = new_week.id)
                wed = Meal_plan(day = "Wednesday", week_id = new_week.id)
                thu = Meal_plan(day = "Thursday", week_id = new_week.id)
                fri = Meal_plan(day = "Friday", week_id = new_week.id)
                sat = Meal_plan(day = "Saturday", week_id = new_week.id)
                list = List(week_id = new_week.id)
                session.add_all([sun, mon, tue, wed, thu, fri, sat, list])
                session.commit()
                view_week_menu()
                
                
            else:
                week_display(session.query(Week).filter(Week.id == answer["week"].id).first())
        
        # actually view the meal plans for a week
        def week_display(week):
            questions = [
                inquirer.List(
                    "meal_plan",
                    message = "Pick a day to edit it, or choose another option",
                    choices = week.meal_plans + ["Automatically add items to the grocery list", "Edit grocery list", "View grocery list", "Add list to pantry", "Back"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["meal_plan"] == "Back":
                view_week_menu()
            if answer["meal_plan"] == "Automatically add items to the grocery list":
                create_list(week)
            elif answer["meal_plan"] == "Edit grocery list":
                edit_list(week)
            elif answer["meal_plan"] == "View grocery list":
                print(week.list[0].pretty())
                week_display(week)
            elif answer["meal_plan"] == "Add list to pantry":
                update_pantry(week.list[0])
            else:
                meal_plan_menu(answer["meal_plan"])

###############################grocery list stuff##########################################
        # automatically add items to your grocery list for the meals you have planned that week, taking into account your pantry
        def create_list(week):
            week_list = week.list[0]
            print(week.list[0].id)
            print(week)
            for meal_plan in week.meal_plans:
                for meal_plan_recipe in meal_plan.meal_plan_recipes:
                    for ingredient in meal_plan_recipe.recipe.ingredient_items:
                        ing_list_item = session.query(List_item).filter(List_item.item_id == ingredient.item_id).filter(List_item.list_id == week_list.id).first()
                        # make the list item if it doesn't exist yet
                        if ing_list_item is None:
                            ing_list_item = List_item(item_id = ingredient.item_id, list_id = week_list.id, quantity = 0)
                            session.add(ing_list_item)
                            session.commit()
                        # updates the list item quantitiy
                        ing_list_item.quantity += ingredient.quantity
                        session.commit()
            # checks each list item against the pantry
            for list_item in week_list.list_items:
                pantry_item = session.query(Pantry_item).filter(Pantry_item.item_id==list_item.item_id).first()
                if pantry_item is not None:
                    if pantry_item.quantity >= list_item.quantity:
                        session.delete(list_item)
                        session.commit()
                    elif pantry_item.quantity < list_item.quantity:
                        list_item.quantity -= pantry_item.quantity
                        session.commit()
            print(week_list.pretty())
            week_display(week)
        
        # menu for directly editing the list
        def edit_list(week):
            week_list = session.query(List).filter(List.week_id == week.id).first()
            questions = [
                inquirer.List(
                    "option",
                    message = "select an item to delete or change the quantity",
                    choices = week_list.list_items + ["Back", "Add new item","Clear"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Back":
                week_display(week)
            elif answer["option"] == "Clear":
                for list_item in week_list.list_items:
                    session.delete(list_item)
                session.commit()
                print(week.list[0].pretty())
                week_display(week)
            elif answer["option"]== "Add new item":
                new_list_item(week.list[0], week)
            else:
                edit_list_item(answer["option"])

        #add an item to a list 
        def new_list_item(parent_list, week):
            new_name = input("What is the name of the item you want to add to your list? ")
            new_item = session.query(Item).filter(Item.name == new_name.title()).first()
            if new_item is None:
                # if an item does not exist make the item
                new_item = Item(name = new_name.title())
                session.add(new_item)
                session.commit()
            new_quant = input("Enter a quantity ")
            if new_quant.isnumeric():
                new_list_item = List_item(item_id = new_item.id, quantity = int(new_quant), list_id = parent_list.id)
                session.add(new_list_item)
                session.commit()
                edit_list(week)
            else:
                print("Please enter an integer")
                new_list_item()
        # follow up to edit an item
        def edit_list_item(list_item):
            questions = [
                inquirer.List(
                    "option",
                    message = str(list_item),
                    choices = ["Edit quantity", "Delete"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Edit quantity":
                new_quant = input("New Quantity: ")
                list_item.quantity = new_quant
                session.commit()
                edit_list(list_item.list.week)
            elif answer["option"] == "Delete":
                week = list_item.list.week
                session.delete(list_item)
                session.commit()
                edit_list(week)

        # automatically add the items on the list to your pantry
        def update_pantry(list):
            for list_item in list.list_items:
                pantry_item = session.query(Pantry_item).filter(Pantry_item.item_id == list_item.item_id).first()
                if pantry_item is None:
                    pantry_item = Pantry_item(item_id = list_item.item_id, quantity = 0)
                    session.add(pantry_item)
                    session.commit()
                pantry_item.quantity+=list_item.quantity
                session.commit()
            questions = [
                inquirer.List(
                    "option",
                    message = "Go to",
                    choices = ["Pantry", "Week of meal plans"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Week of meal plans":
                week_display(list.week)
            if answer["option"] == "Pantry":
                view_pantry()

####################################### end of list stuff ##########################################

        # view the meal plan for a specific day
        def meal_plan_menu(meal_plan):
            meal_plan_recipes = ""
            for meal_plan_recipe in meal_plan.meal_plan_recipes:
                meal_plan_recipes += str(meal_plan_recipe.recipe)
                meal_plan_recipes += "\n"
            print(f"Meal Plan for {meal_plan.date()} \n" + str(meal_plan_recipes))
            questions = [
                inquirer.List(
                    "option",
                    message = "select an option",
                    choices = ["Edit", "Home Menu", "Week View", "Make the meal and update your pantry"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Week View":
                week_display(meal_plan.week)
            elif answer["option"] == "Home Menu":
                home_menu()
            elif answer["option"] == "Make the meal and update your pantry":
                make_meal(meal_plan)
            elif answer["option"] == "Edit":
                edit_plan(meal_plan)

        # make a meal and update the pantry
        def make_meal(meal_plan):
            for meal_plan_recipe in meal_plan.meal_plan_recipes:
                for ingredient in meal_plan_recipe.recipe.ingredient_items:
                    pantry_item = session.query(Pantry_item).filter(ingredient.item_id == Pantry_item.item_id).first()
                    if pantry_item is None:
                        print(f"{ingredient.item} wasn't in your pantry!")
                    elif pantry_item.quantity > ingredient.quantity:
                        pantry_item.quantity -= ingredient.quantity
                        session.commit()
                        print(f"{pantry_item} left in your pantry")
                    elif pantry_item.quantity == ingredient.quantity:
                        print(f"You've used up all of your {ingredient.item}")
                        session.delete(pantry_item)
                        session.commit()
                    elif pantry_item.quantity < ingredient.quantity:
                        print(f"You didn't have enought {ingredient.item}, so I've removed everything there was from your pantry")
                        session.delete(pantry_item)
                        session.commit()
            questions = [
                inquirer.List(
                    "option",
                    message = "Go to",
                    choices = ["Pantry", "Meal Plan"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Meal Plan":
                meal_plan_menu(meal_plan)
            if answer["option"] == "Pantry":
                view_pantry()

        # menu to edit a meal plan
        def edit_plan(meal_plan):
            questions = [
                inquirer.List(
                    "option",
                    message = meal_plan.date()+": Select a dish to delete it, or add a new dish",
                    choices = meal_plan.meal_plan_recipes+["Add a New Dish", "Back"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Back":
                meal_plan_menu(meal_plan)
            if answer["option"] == "Add a New Dish":
                add_recipe(meal_plan)
            else: 
                recipe_to_delete = session.query(Meal_plan_recipe).filter(Meal_plan_recipe.id == answer["option"].id).first()
                print(f"Deleted: {recipe_to_delete}!")
                session.delete(recipe_to_delete)
                session.commit()
                edit_plan(meal_plan)

        # menu to add a new dish to a meal
        def add_recipe(meal_plan):
            all_recipes = session.query(Recipe).all()
            all_recipe_names = []
            for recipe in all_recipes:
                all_recipe_names.append(recipe.name)
            questions =[
                inquirer.List(
                    "option",
                    message = "Choose a recipe to add",
                    choices = all_recipe_names + ["Back"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Back":
                edit_plan(meal_plan)
            else:
                # print(type(answer["option"]))
                # print(answer["option"].id)
                selected_recipe = session.query(Recipe).filter(Recipe.name == answer["option"]).first()
                # print(selected_recipe)
                # print(type(selected_recipe))
                # print(selected_id)
                # print(type(meal_plan))
                # print(meal_plan.id)
                new_dish = Meal_plan_recipe(meal_plan_id = meal_plan.id, recipe_id = selected_recipe.id)
                session.add(new_dish)
                session.commit()
                edit_plan(meal_plan)

        

###################################### full CRUD on the pantry###################################
        # view the whole pantry
        def view_pantry():
            pantry = session.query(Pantry_item).all()
            questions = [
                inquirer.List(
                    "option",
                    message = "Choose a pantry item to add, or select an item to edit it",
                    choices = pantry + ["Add new pantry item", "Back"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Back":
                home_menu()
            elif answer["option"] == "Add new pantry item":
                new_pantry()
            else:
                edit_pantry(answer["option"])
        
        # update or delete a pantry item
        def edit_pantry(pantry_item):
            questions = [
                inquirer.List(
                    "option",
                    message = str(pantry_item),
                    choices = ["Edit quantity", "Delete", "Back"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Back":
                view_pantry()
            if answer["option"] == "Edit quantity":
                # update quantity
                new_quant = input("Enter the new quantity ")
                if new_quant.isnumeric():
                    pantry_item.quantity = int(new_quant)
                    session.commit()
                    view_pantry()
                else:
                    print("Please enter an integer")
                    edit_pantry(pantry_item)
            if answer["option"] == "Delete":
                # delete the pantry item
                session.delete(pantry_item)
                session.commit()
                view_pantry()

        def new_pantry():
            new_name = input("What is the name of the new pantry item you want to add? ")
            new_item = session.query(Item).filter(Item.name == new_name.title()).first()
            if new_item is None:
                # if an item does not exist make the item
                new_item = Item(name = new_name.title())
                session.add(new_item)
                session.commit()
            new_quant = input("Enter a quantity ")
            if new_quant.isnumeric():
                new_pantry_item = Pantry_item(item_id = new_item.id, quantity = int(new_quant))
                session.add(new_pantry_item)
                session.commit()
                view_pantry()
            else:
                print("Please enter an integer")
                new_pantry()

###################################### Full recipe crud ######################################
        # view all the recipes
        def view_recipes():
            cookbook = session.query(Recipe).all()
            cookbook_names = []
            for recipe in cookbook:
                cookbook_names.append(recipe.name)
            questions = [
                inquirer.List(
                    "option",
                    message = "Choose a recipe to edit it, or add a new one",
                    choices = cookbook_names + ["Add a new recipe", "Back"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Back":
                home_menu()
            elif answer["option"] == "Add a new recipe":
                new_recipe_name = input("New recipe name: ")
                new_recipe_type = input("Type of dish: ")
                new_recipe_cuisine = input("Cuisine: ")
                new_recipe = Recipe(name = new_recipe_name, type=new_recipe_type, cuisine = new_recipe_cuisine)
                session.add(new_recipe)
                session.commit()
                edit_recipe(new_recipe)
            else:
                recipe_to_edit = session.query(Recipe).filter(Recipe.name == answer["option"]).first()
                edit_recipe(recipe_to_edit)

        # edit a recipe
        def edit_recipe(recipe):
            print(recipe)
            questions = [
                inquirer.List(
                    "option",
                    message = "Options",
                    choices = ["Change name", "Edit ingredients", "Edit instructions", "Delete", "Back"]
                )
            ]
            answer = inquirer.prompt(questions)
            if answer["option"] == "Back":
                view_recipes()
            if answer["option"] == "Delete":
                # delete the recipe
                session.delete(recipe)
                session.commit()
                view_recipes()
            elif answer["option"] == "Edit ingredients":
                edit_ingredients(recipe)
            elif answer["option"] == "Change name":
                # Change the name
                new_name = input("New Name ")
                recipe.name = new_name
                session.commit()
                edit_recipe(recipe)
            elif answer["option"] == "Edit instructions":
                # change the instructions
                new_instr = input("New Instructions: ")
                recipe.instructions = new_instr
                session.commit()
                edit_recipe(recipe)
                
        # specifically edit the ingredients in a recipe
        def edit_ingredients(recipe):
            ingredient_list = recipe.ingredient_items
            questions = [
                inquirer.List(
                    "option",
                    message = "Select an ingredient to edit or delete it, or add a new ingredient",
                    choices = ingredient_list + ["Add a new ingredient", "Back"] 
                )
            ]
            answer = inquirer.prompt(questions)
            
            if answer["option"] == "Back":
                edit_recipe(recipe)
            elif answer["option"] == "Add a new ingredient":
                new_name = input("Ingredient Name: ")
                new_item = session.query(Item).filter(Item.name == new_name.title()).first()
                if new_item is None:
                    # if an item does not exist make the item
                    new_item = Item(name = new_name.title())
                    session.add(new_item)
                    session.commit()
                new_quant = input("Enter a quantity ")
                if new_quant.isnumeric():
                    new_ingredient_item = Ingredient_item(item_id = new_item.id, recipe_id = recipe.id, quantity = int(new_quant))
                    session.add(new_ingredient_item)
                    session.commit()
                    edit_recipe(recipe)
                else:
                    print("Please enter an integer")
                    edit_ingredients(recipe)
            else:
                session.delete(answer["option"])
                session.commit()
                edit_recipe(recipe)




##############################Start the whole shebang###################################
        print('''
   _____ _____   ____   _____ ______ _______     __  _      _____  _____ _______ ______ _____  
  / ____|  __ \ / __ \ / ____|  ____|  __ \ \   / / | |    |_   _|/ ____|__   __|  ____|  __ \ 
 | |  __| |__) | |  | | |    | |__  | |__) \ \_/ /  | |      | | | (___    | |  | |__  | |__) |
 | | |_ |  _  /| |  | | |    |  __| |  _  / \   /   | |      | |  \___ \   | |  |  __| |  _  / 
 | |__| | | \ \| |__| | |____| |____| | \ \  | |    | |____ _| |_ ____) |  | |  | |____| | \ \ 
  \_____|_|  \_\\\____/ \_____|______|_|  \_\ |_|    |______|_____|_____/   |_|  |______|_|  \_\\

                .-----.                                _.----"""""""----._
          _.---//-"""-\\\---._            .------.___  (                   )
         (   (/        `-'   )          (        ___|-|`"""---..___..---""|
        _|`"--._________.--"'|_          `---'"""     |                   |
       (_|                   |_)                      |                   |
       `--)                 (--'          ________    |                   |
         |                   |   _.--"""""        """"----._              |
         |                   |  (_                         _)--.----------------.
         |                   |   \`""---...________...----'/__/___             ||
         `-.__           __.-'    \___                  __/ ""-----"""""""-----`'
             `""-----""'              ""`-----------'""
              ''')
        home_menu()


if __name__ == "__main__":
    main()
