# Recipe-manager
# 🍳 Recipe Manager CLI

A command-line application for managing recipes with categories and ingredients using SQLAlchemy ORM and Alembic migrations.

## Features

- ✅ Add new recipes with ingredients and categories
- ✅ List all recipes with their categories
- ✅ Search recipes by ingredient name
- ✅ Remove recipes by title
- ✅ Automatic category creation
- ✅ SQLite database with proper relationships
- ✅ Input validation and error handling
- ✅ Alembic database migrations

## Installation

### Prerequisites
- Python 3.12+
- pipenv

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd recipe-manager-cli

# Install dependencies
pipenv install

# Set up the database
pipenv run alembic upgrade head

# Run the application
pipenv run python -m app.main
```

## Usage

### Running the Application
```bash
pipenv run python -m app.main
```

### Menu Options

1. **Add Recipe**
   - Enter recipe title (required)
   - Enter cooking instructions (required)
   - Enter category name (optional, defaults to "Uncategorized")
   - Enter ingredients as comma-separated list (optional)

2. **List Recipes**
   - Displays all recipes with their categories
   - Shows recipe ID, title, and category

3. **Search by Ingredient**
   - Enter ingredient name to find matching recipes
   - Supports partial matching (case-insensitive)

4. **Remove Recipe**
   - Enter recipe title to delete
   - Confirms successful removal

5. **Quit**
   - Exit the application

## Database Schema

### Categories Table
- `id` (Integer, Primary Key)
- `name` (String, Unique, Not Null)
- `description` (Text)

### Recipes Table
- `id` (Integer, Primary Key)
- `title` (String, Not Null)
- `instructions` (Text)
- `cooking_time` (Integer)
- `category_id` (Integer, Foreign Key to categories.id)

### Ingredients Table
- `id` (Integer, Primary Key)
- `name` (String, Not Null)
- `quantity` (String)
- `recipe_id` (Integer, Foreign Key to recipes.id)

## Sample Database Content

### Recipes Table
```
ID    Title                Instructions                                       Category
------------------------------------------------------------------------------------------
1     ugali                boil water, add flour to the boiling water, stir until it hardens  kenyan
```

### Ingredients Table
```
ID    Name            Quantity        Recipe
-------------------------------------------------------
1     flour                           ugali
2     water                           ugali
```

### Categories Table
```
ID    Name            Description
--------------------------------------------------
1     kenyan
```

## API Functions

### Core Functions (app/services.py)

#### `add_recipe(title, instructions, category, ingredients)`
Adds a new recipe to the database.
- **Parameters:**
  - `title` (str): Recipe title
  - `instructions` (str): Cooking instructions
  - `category` (str): Category name (optional)
  - `ingredients` (list): List of ingredient names
- **Returns:** Dict with recipe title

#### `list_recipes(category=None)`
Retrieves all recipes, optionally filtered by category.
- **Parameters:**
  - `category` (str): Category name to filter by (optional)
- **Returns:** List of Recipe objects

#### `find_by_ingredient(ingredient_name)`
Finds recipes containing specified ingredients.
- **Parameters:**
  - `ingredient_name` (str): Ingredient name(s) separated by commas
- **Returns:** List of dicts with recipe title and ID

#### `remove_recipe(recipe_title)`
Deletes a recipe by title.
- **Parameters:**
  - `recipe_title` (str): Title of recipe to remove
- **Returns:** Boolean indicating success

### Helper Functions

#### `get_or_create_category(session, name)`
Gets existing category or creates new one.
- **Parameters:**
  - `session`: Database session
  - `name` (str): Category name
- **Returns:** Category object

#### `get_or_create_ingredient(session, name)`
Gets existing ingredient or creates new one.
- **Parameters:**
  - `session`: Database session
  - `name` (str): Ingredient name
- **Returns:** Ingredient object

## Dependencies

### Production Dependencies
- **SQLAlchemy**: ORM for database operations
- **Click**: CLI framework (future enhancement)
- **Aiosqlite**: Async SQLite support

### Development Dependencies
- **Alembic**: Database migration tool

## Project Structure

```
recipe-manager-cli/
├── Pipfile                 # Dependency management
├── Pipfile.lock           # Locked dependencies
├── README.md              # This file
├── alembic.ini           # Alembic configuration
├── alembic/               # Migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── app/                   # Main application package
│   ├── __init__.py
│   ├── db.py             # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── services.py       # Business logic functions
│   └── main.py           # CLI interface
├── recipes.db            # SQLite database
└── LICENSE               # MIT License
```

## Database Migrations

The project uses Alembic for database version control:

```bash
# Create new migration
pipenv run alembic revision --autogenerate -m "migration message"

# Apply migrations
pipenv run alembic upgrade head

# Check current migration
pipenv run alembic current
```

## Development

### Running Tests
```bash
# Install development dependencies
pipenv install --dev

# Run tests (when implemented)
pipenv run pytest
```

### Code Style
- Follow PEP 8 conventions
- Use type hints where appropriate
- Keep functions focused and modular

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
