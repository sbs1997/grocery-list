from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base
from models.models import (Item, Pantry_item, List, List_item, Week, Meal_plan, Meal_plan_recipe, Recipe, Ingredient_item, Base)

engine = create_engine('sqlite:///grocery_lister.db')
Item.__table__.drop(engine)
Pantry_item.__table__.drop(engine)
List.__table__.drop(engine)
List_item.__table__.drop(engine)
Week.__table__.drop(engine)
Meal_plan.__table__.drop(engine)
Meal_plan_recipe.__table__.drop(engine)
Recipe.__table__.drop(engine)
Ingredient_item.__table__.drop(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    # items
    cheddar = Item(name = "Cheddar")
    pecorino = Item(name = "Pecorino Romano")
    bread = Item(name = "Bread")
    butter = Item(name = "Butter")
    spaghetti = Item(name = "Spaghetti")
    buchatini = Item(name = "Buchatini")
    pepper = Item(name = "Pepper")
    salt = Item(name = "Salt")
    tomato = Item(name = "Tomato")
    olive_oil = Item(name = "Olive Oil")
    pancetta = Item(name = "Pancetta")
    egg = Item(name = "Egg")
    onion = Item(name = "Onion")
    refried = Item(name ="Refried Beans")
    black_beans = Item(name = "Black Beans")
    zuc_flowers = Item(name = "Zucchini Flowers")
    bread_crumbs = Item(name = "Bread Crumbs")
    flour = Item(name = "Flour")
    lime = Item(name = "Lime")
    cilantro = Item(name = "Cilantro")
    tomatillo = Item(name = "Tomatillo")
    jalepeno = Item(name = "Jalepeno")
    tortilla = Item(name = "Corn Tortillas")

    all_items = [cheddar, pecorino, bread, butter, spaghetti, buchatini, pepper, 
                salt, tomato, olive_oil, pancetta, egg, onion, refried, black_beans, 
                zuc_flowers, bread_crumbs, flour, lime, cilantro, tomatillo, jalepeno,
                tortilla]

    # recipes
    grilled_cheese = Recipe(name = "Grilled Cheese", instructions = "Melt the butter in the pan, put cheese on two slices of bread, fry them in the butter and cover to melt the cheese, then put them together as a sandwich", type = "Entree", cuisine = "American")
    cacio_e_pepe = Recipe(name = "Cacio e Pepe", instructions="No matter what I put here people will have Opinions tm so i'm not gonna do that and we all know that there's weird magic involved in making great cacio e pepe", type = "Entree", cuisine = "Italian")
    carbonara = Recipe(name="Pasta Carbonara", instructions="Boil salted water and cook the pasta 2 minutes less than usual. While thats happening chop the pancetta and grate the pecorino. Fry the pancetta in a cast iron pan or dutch oven till slightly crispy. whisk 2 of the eggs and yolks of the other 2. The pancetta and the pasta should finish at about the same time, turn off the heat on the pancetta, transfer the pasta to the dutch oven using tongs, slowly mix in the egg, and then the cheese and, if needed extra pasta water to get a nice creamy sauce while avoiding scrambled eggs, serve topped with the extra cheese and pepper to taste", type = "Entree", cuisine = "Italian")
    tacos = Recipe(name = "Taco", instructions = "Heat the tortillas in a pan, add the tasty stuff the way you like it.", type = "Entree", cuisine="Mexican")
    salsa = Recipe(name = "Tomatillo Salsa", instructions = "Blacken the tomatillos and jalepenos in a sauce pan, deglaze the pan with water and let reduce some. Put the veggies and the liquid from deglazing in a food processor and blend until the desired consistency. Add lime juice, cilantro, and salt to taste", type = "Sauce", cuisine = "Mexican")
    fried_zuc_flowers = Recipe (name = "Fried Zucchini Flowers", instructions = "Fill the zucchini flowers with bread crumbs. Then dip them in egg and dredge in flour. Fry in in a pan with olive oil until golden brown. Serve while hot", type = "Appetizer", cuisine = "Italian")

    all_recipes = [grilled_cheese, cacio_e_pepe, carbonara, tacos, salsa, fried_zuc_flowers]

    # weeks
    week1 = Week(start_week = "September 17th")
    week2 = Week(start_week = "September 24th")

    all_weeks = [week1, week2]

    # pantry items
    pantry_cheddar = Pantry_item(item_id = 1, quantity = 3)
    pantry_bread = Pantry_item(item_id = 3, quantity = 24)
    pantry_spaghetti = Pantry_item(item_id = 5, quantity = 2)
    pantry_pepper = Pantry_item(item_id = 7, quantity = 100)
    pantry_salt = Pantry_item(item_id = 8, quantity = 100)

    all_pantry_items = [pantry_bread, pantry_cheddar, pantry_spaghetti, pantry_salt, pantry_pepper]

    # ingredient items
    grilled_cheese_cheddar = Ingredient_item(item_id = 1, recipe_id = 1, quantity = 2)
    grilled_cheese_butter = Ingredient_item(item_id = 4, recipe_id = 1, quantity = 1)
    grilled_cheese_bread = Ingredient_item(item_id = 3, recipe_id = 1, quantity = 2)

    cacio_e_pepe_spaghetti = Ingredient_item(item_id = 5, recipe_id = 2, quantity = 1)
    cacio_e_pepe_pepper = Ingredient_item(item_id = 7, recipe_id = 2, quantity = 1)
    cacio_e_pepe_pecorino = Ingredient_item(item_id = 2, recipe_id = 2, quantity = 2)

    carbonara_spaghetti = Ingredient_item(item_id = 5, recipe_id = 3, quantity = 1)
    carbonara_egg = Ingredient_item(item_id = 12, recipe_id = 3, quantity = 4)
    carbonara_pecorino = Ingredient_item(item_id = 2, recipe_id = 3, quantity = 1)
    carbonara_pancetta = Ingredient_item(item_id = 11, recipe_id = 3, quantity = 1)
    carbonara_salt = Ingredient_item(item_id = 8, recipe_id = 3, quantity = 1)
    carbonara_pepper = Ingredient_item(item_id = 7, recipe_id = 3, quantity = 1)

    tacos_tortilla = Ingredient_item(item_id = 23, recipe_id = 4, quantity = 6)
    tacos_tomato = Ingredient_item(item_id = 9, recipe_id = 4, quantity = 1)
    tacos_onion = Ingredient_item(item_id = 13, recipe_id = 4, quantity = 1)
    tacos_refried = Ingredient_item(item_id = 14, recipe_id = 4, quantity = 1)
    tacos_cilantro = Ingredient_item(item_id = 20, recipe_id = 4, quantity = 1)
    tacos_jalepenos = Ingredient_item(item_id = 22, recipe_id = 4, quantity = 2)
    tacos_lime = Ingredient_item(item_id = 19, recipe_id = 4, quantity = 2)

    salsa_tomatillo = Ingredient_item(item_id = 21, recipe_id = 5, quantity = 5)
    salsa_jalepeno = Ingredient_item(item_id = 22, recipe_id = 5, quantity = 3)
    salsa_cilantro = Ingredient_item(item_id = 20, recipe_id = 5, quantity = 1)
    salsa_salt = Ingredient_item(item_id = 8, recipe_id = 5, quantity = 1)
    salsa_lime = Ingredient_item(item_id = 19, recipe_id = 5, quantity = 2)

    fried_zuc_flowers_zuc_flowers = Ingredient_item(item_id = 16, recipe_id = 6, quantity = 8)
    fried_zuc_flowers_flour = Ingredient_item(item_id = 18, recipe_id = 6, quantity = 2)
    fried_zuc_flowers_bread_crumbs = Ingredient_item(item_id = 17, recipe_id = 6, quantity = 1)
    fried_zuc_flowers_olive_oil = Ingredient_item(item_id = 10, recipe_id = 6, quantity = 1)
    fried_zuc_flowers_eggs = Ingredient_item(item_id = 12, recipe_id = 6, quantity = 3)

    all_ingredient_items = [
        grilled_cheese_bread, grilled_cheese_butter, grilled_cheese_cheddar,
        cacio_e_pepe_pecorino, cacio_e_pepe_pepper, cacio_e_pepe_spaghetti,
        carbonara_egg, carbonara_spaghetti, carbonara_pecorino, carbonara_pancetta, carbonara_salt, carbonara_pepper,
        tacos_tortilla, tacos_tomato, tacos_onion, tacos_refried, tacos_cilantro, tacos_jalepenos, tacos_lime,
        salsa_tomatillo, salsa_jalepeno, salsa_cilantro, salsa_salt, salsa_lime,
        fried_zuc_flowers_bread_crumbs, fried_zuc_flowers_eggs, fried_zuc_flowers_flour, fried_zuc_flowers_olive_oil, fried_zuc_flowers_zuc_flowers
    ]

    # lists
    list_1 = List(week_id = 1)
    list_2 = List(week_id = 2)

    all_lists = [list_1, list_2]

    # list items
    list_butter = List_item(list_id = 1, item_id = 4, quantity = 1)
    list_limes = List_item(list_id = 1, item_id = 19, quantity = 1)
    
    all_list_items = [list_butter, list_limes]

    # meal plans
    mon = Meal_plan(day="Monday", week_id = 1)
    tue = Meal_plan(day="Tuesday", week_id = 1)
    wed = Meal_plan(day="Wednesday", week_id = 1)
    thu = Meal_plan(day="Thursday", week_id = 1)
    fri = Meal_plan(day="Friday", week_id = 1)
    sat = Meal_plan(day="Saturday", week_id = 1)
    sun = Meal_plan(day="Sunday", week_id = 1)

    mon_2 = Meal_plan(day="Monday", week_id = 2)
    tue_2 = Meal_plan(day="Tuesday", week_id = 2)
    wed_2 = Meal_plan(day="Wednesday", week_id = 2)
    thu_2 = Meal_plan(day="Thursday", week_id = 2)
    fri_2 = Meal_plan(day="Friday", week_id = 2)
    sat_2 = Meal_plan(day="Saturday", week_id = 2)
    sun_2 = Meal_plan(day="Sunday", week_id = 2)


    all_meal_plans = [mon, tue, wed, thu, fri, sat, sun, mon_2, tue_2, wed_2, thu_2, fri_2, sat_2, sun_2]

    # meal_plan recipe join tables
    mon_grilled = Meal_plan_recipe(meal_plan_id = 1, recipe_id = 1)
    mon_salsa = Meal_plan_recipe(meal_plan_id = 1, recipe_id = 5)
    tue_cacio = Meal_plan_recipe(meal_plan_id = 2, recipe_id = 2)
    wed_cacio = Meal_plan_recipe(meal_plan_id = 3, recipe_id = 2)
    thu_tacos = Meal_plan_recipe(meal_plan_id = 4, recipe_id = 4)
    fri_flowers = Meal_plan_recipe(meal_plan_id = 5, recipe_id = 6)
    fri_carb = Meal_plan_recipe(meal_plan_id = 5, recipe_id = 3)
    sat_grilled = Meal_plan_recipe(meal_plan_id = 6, recipe_id = 1)
    sun_tacos = Meal_plan_recipe(meal_plan_id = 7, recipe_id = 4)

    all_meal_plan_recipes = [mon_grilled, mon_salsa, tue_cacio, wed_cacio, thu_tacos,
                            fri_flowers, fri_carb, sat_grilled, sun_tacos]

    # adding and committing
    session.add_all(all_recipes)
    session.add_all(all_items)
    session.add_all(all_weeks)
    session.add_all(all_pantry_items)
    session.add_all(all_ingredient_items)
    session.add_all(all_lists)
    session.add_all(all_list_items)
    session.add_all(all_meal_plans)
    session.add_all(all_meal_plan_recipes)

    session.commit()