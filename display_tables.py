from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from app.models import Recipe, Ingredient, Category

engine = create_engine('sqlite:///recipes.db')
Session = sessionmaker(bind=engine)
session = Session()

# Display Recipes
recipes = session.query(Recipe).options(joinedload(Recipe.category)).all()
print("Recipes Table:")
print(f"{'ID':<5} {'Title':<20} {'Instructions':<50} {'Category':<15}")
print("-" * 90)
for r in recipes:
    instr = r.instructions.replace('add', ', add').replace('stir', ', stir') if r.instructions else ''
    instr = instr[:47] + '...' if len(instr) > 50 else instr
    cat = r.category.name if r.category else 'Uncategorized'
    print(f"{r.id:<5} {r.title:<20} {instr:<50} {cat:<15}")

# Display Ingredients
ingredients = session.query(Ingredient).options(joinedload(Ingredient.recipe)).all()
print("\nIngredients Table:")
print(f"{'ID':<5} {'Name':<15} {'Quantity':<15} {'Recipe':<20}")
print("-" * 55)
for i in ingredients:
    qty = i.quantity or ''
    print(f"{i.id:<5} {i.name:<15} {qty:<15} {i.recipe.title:<20}")

# Display Categories
categories = session.query(Category).all()
print("\nCategories Table:")
print(f"{'ID':<5} {'Name':<15} {'Description':<30}")
print("-" * 50)
for c in categories:
    desc = c.description or ''
    print(f"{c.id:<5} {c.name:<15} {desc:<30}")

session.close()
