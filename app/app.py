from fastapi import FastAPI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = FastAPI()

USER_NAME = os.getenv("USER_NAME", "Guest")
INVENTORY_FILE = "inventory.txt"

RECIPES_BY_TIME = {
    "Breakfast": {
        "Omelette": ["eggs", "butter", "onion"],
        "Cereal with Milk": ["cereal", "milk"],
        "Toast": ["bread", "butter", "cheese"]
    },
    "Lunch": {
        "Garlic Chicken": ["chicken breast", "garlic", "onion", "olive oil"],
        "Beef Stew": ["beef", "potatoes", "onion", "carrots"]
    },
    "Dinner": {
        "Classic Tomato Pasta": ["pasta", "tomatoes", "garlic", "olive oil"],
        "Cheesy Caprese": ["mozzarella cheese", "tomatoes", "olive oil"]
    },
    "Midnight Snack": {
        "Midnight Popcorn": ["popcorn kernels", "butter", "salt"],
        "Chocolate Milk": ["milk", "chocolate powder"]
    }
}

@app.get("/")
def get_recipe_suggestion():
    ingredients = []
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            ingredients = [line.strip().lower() for line in f.readlines() if line.strip()]

    inventory_set = set(ingredients)
    current_hour = datetime.now().hour

    if 6 <= current_hour < 12:
        time_greeting, meal_type = "Good morning", "Breakfast"
    elif 12 <= current_hour < 17:
        time_greeting, meal_type = "Good afternoon", "Lunch"
    elif 17 <= current_hour < 22:
        time_greeting, meal_type = "Good evening", "Dinner"
    else:
        time_greeting, meal_type = "Late night", "Midnight Snack"

    relevant_recipes = RECIPES_BY_TIME.get(meal_type, {})
    all_suggestions = []

    for name, req_items in relevant_recipes.items():
        req_set = set(req_items)
        missing = req_set - inventory_set

        all_suggestions.append({
            "name": name,
            "ingredients": req_items,
            "missing": list(missing)
        })

    return {
        "greeting": f"{time_greeting}, {USER_NAME}!",
        "meal_type": meal_type,
        "recipes": all_suggestions,
        "inventory": [i.title() for i in ingredients]
    }