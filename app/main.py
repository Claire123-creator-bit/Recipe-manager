import sys
from app.services import add_recipe, list_recipes, find_by_ingredient, remove_recipe
from sqlalchemy.orm import joinedload
from .models import Recipe
from app.db import SessionLocal

session = SessionLocal()

def print_menu():
    print("\n🍳 Recipe Manager")
    print("1. Add Recipe")
    print("2. List Recipes")
    print("3. Search by Ingredient")
    print("4. Remove Recipe")
    print("5. Quit")

def handle_add():
    while True:
        title = input("Enter recipe title: ").strip()
        if title:
            break
        print("⚠️ Title cannot be empty. Please enter a valid title.")
    while True:
        instructions = input("Enter instructions: ").strip()
        if instructions:
            break
        print("⚠️ Instructions cannot be empty. Please enter valid instructions.")
    category = input("Enter category:  ").strip()
    ingredients = input("Enter ingredients (comma-separated): ").split(",")

    recipe_info = add_recipe(title, instructions, category, ingredients)
    print(f"✅ Recipe '{recipe_info['title']}' added successfully!")
def handle_list():
    recipes = session.query(Recipe).options(joinedload(Recipe.category)).all()
    if not recipes:
        print("📭 No recipes found.")
        return
    for r in recipes:
        print(f"📌 {r.id}. {r.title} ({r.category.name if r.category else 'Uncategorized'})")

def handle_search():
    while True:
        ing = input("Enter ingredient name: ").strip()
        if ing:
            break
        print("⚠️ Ingredient name cannot be empty. Please enter a valid ingredient name.")
    results = find_by_ingredient(ing)
    if not results:
        print(f"⚠️  No recipes found with ingredient '{ing}'.")
    else:
        print(f"\n🔎 Recipes with '{ing}':")
        for r in results:
            print(f"- {r['title']}")

def handle_remove():
    while True:
        title = input("Enter recipe title to remove: ").strip()
        if title:
            break
        print("⚠️ Title cannot be empty. Please enter a valid title.")
    ok = remove_recipe(title)
    if ok:
        print(f"🗑️  Recipe '{title}' removed.")
    else:
        print(f"⚠️  Recipe '{title}' not found.")

def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_add()
        elif choice == "2":
            handle_list()
        elif choice == "3":
            handle_search()
        elif choice == "4":
            handle_remove()
        elif choice == "5":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("⚠️ Invalid choice, try again.")

if __name__ == "__main__":
    main()