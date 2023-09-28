from sqlalchemy import ForeignKey, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship, validates

#initialize with decrative base
Base = declarative_base()


# A grocery item, such as broccili or flour
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    pantry_items = relationship("Pantry_item", back_populates="item")
    list_items = relationship("List_item", back_populates="item")
    ingredient_items = relationship("Ingredient_item", back_populates="item")
    
    def __repr__(self):
        return repr(f"{self.name}")


# an item once it's in your pantry
class Pantry_item(Base):
    __tablename__ = "pantry_items"

    id = Column(Integer, primary_key = True)
    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("Item", back_populates= "pantry_items")
    quantity = Column(Integer)

    def __repr__(self):
        return f"{self.quantity} of {self.item}"

# an item on the list
class List_item(Base):
    __tablename__ = "list_items"

    id = Column(Integer, primary_key = True)
    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("Item", back_populates= "list_items")
    list_id = Column(Integer, ForeignKey('lists.id'))
    list = relationship("List", back_populates="list_items")
    quantity = Column(Integer)

# a grocery list of items to buy
class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key = True)
    week_id = Column(Integer, ForeignKey('weeks.id'))
    week = relationship("Week", back_populates="list")
    list_items = relationship("List_item",  back_populates="list")
# the week for the meal plans to be used
class Week(Base):
    __tablename__ = "weeks"

    id = Column(Integer, primary_key = True)
    start_week = Column(String)
    list = relationship("List", back_populates="week")
    meal_plans = relationship("Meal_plan", back_populates="week")

    def __repr__(self):
        return f"Week beginning on {self.start_week}"

# a meal plan, which may contain multiple recipes for a specific day
class Meal_plan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key = True)
    day = Column(String)
    week_id = Column(Integer, ForeignKey('weeks.id'))
    week = relationship("Week", back_populates="meal_plans")
    meal_plan_recipes = relationship("Meal_plan_recipe", back_populates="meal_plan")

    def grab_date(self):
        if self.day == "Sunday":
            return int(self.week.start_week[-4:-2])
        elif self.day == "Monday":
            return int(self.week.start_week[-4:-2])+1
        elif self.day == "Tuesday":
            return int(self.week.start_week[-4:-2])+2
        elif self.day == "Wednesday":
            return int(self.week.start_week[-4:-2])+3
        elif self.day == "Thursday":
            return int(self.week.start_week[-4:-2])+4
        elif self.day == "Friday":
            return int(self.week.start_week[-4:-2])+5
        elif self.day == "Saturday":
            return int(self.week.start_week[-4:-2])+6
        
    def date(self):
        return f"{self.day} the {self.grab_date()}th"

    def __repr__(self):
        return f"{self.day}: {self.meal_plan_recipes}"

# join table for mealplan and recipe
class Meal_plan_recipe(Base):
    __tablename__ = "meal_plan_recipes"

    id = Column(Integer, primary_key = True)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"))
    meal_plan = relationship("Meal_plan", back_populates="meal_plan_recipes")
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="meal_plan_recipes")

    def __repr__(self):
        return f"{self.recipe.name}"

# the recipe
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    instructions = Column(String)
    type = Column(String)
    cuisine = Column(String)
    meal_plan_recipes = relationship("Meal_plan_recipe", back_populates="recipe")
    ingredient_items = relationship("Ingredient_item", back_populates="recipe")

    def pretty_ingredients(self):
        ingredient_list = ""
        for ingredient in self.ingredient_items:
            ingredient_list+=str(ingredient) + "\n"
        return ingredient_list
    
    def __repr__(self):
        return (f"{self.name}\n---------------------------------------------------\n({self.cuisine} {self.type})\n\n{self.pretty_ingredients()}\n\n{self.instructions}\n")

# an ingredient in a recipe
class Ingredient_item(Base):
    __tablename__ = "ingredient_items"

    id = Column(Integer, primary_key = True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="ingredient_items")
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="ingredient_items")
    quantity = Column(Integer)

    def __repr__(self):
        return f"{self.quantity} of {self.item.name}"