from contextlib import contextmanager
from typing import Iterable, List
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload
from app.db import SessionLocal
from app.models import Recipe, Ingredient, Category


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_or_create_category(session, name: str) -> Category:
    name = name.strip()
    cat = session.execute(
        select(Category).where(Category.name.ilike(name))
    ).scalar_one_or_none()
    if not cat:
        cat = Category(name=name)
        session.add(cat)
        session.flush()
    return cat


def get_or_create_ingredient(session, name: str) -> Ingredient:
    norm = name.strip()
    ing = session.execute(
        select(Ingredient).where(Ingredient.name.ilike(norm))
    ).scalar_one_or_none()
    if not ing:
        ing = Ingredient(name=norm)
        session.add(ing)
        session.flush()
    return ing

def add_recipe(title, instructions, category, ingredients):
    with get_session() as session:
        cat = get_or_create_category(session, category or "Uncategorized")
        recipe = Recipe(
            title=title.strip(),
            instructions=instructions.strip(),
            category=cat
        )
        
        session.add(recipe)
        session.flush()  

    
        for ing_name in ingredients or []:
            if ing_name.strip():
                ingredient = Ingredient(name=ing_name.strip(), recipe=recipe)
                session.add(ingredient)

        session.commit()
        recipe_title = recipe.title  # get value before closing session
        session.close()
        return {"title": recipe_title}


def list_recipes(category: str | None = None) -> List[Recipe]:
    with get_session() as session:
        stmt = select(Recipe).order_by(Recipe.title)
        if category:
            stmt = stmt.join(Recipe.category).where(Category.name.ilike(category.strip()))
        return list(session.execute(stmt).scalars())


def find_by_ingredient(ingredient_name: str) -> List[dict]:
    names = [n.strip() for n in ingredient_name.split(",") if n.strip()]
    if not names:
        return []

    with get_session() as session:
        stmt = select(Recipe).options(joinedload(Recipe.category))
        for name in names:
            stmt = stmt.where(Recipe.ingredients.any(Ingredient.name.ilike(name)))
        stmt = stmt.order_by(Recipe.title)
        recipes = list(session.execute(stmt).unique().scalars())
        return [{'title': r.title, 'id': r.id} for r in recipes]


def remove_recipe(recipe_title: str) -> bool:
    with get_session() as session:
        recipe = session.execute(
            select(Recipe).where(Recipe.title.ilike(recipe_title.strip()))
        ).scalar_one_or_none()
        if not recipe:
            return False
        session.delete(recipe)
        return True
