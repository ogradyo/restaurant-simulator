from .order_models import MenuItem, ItemCategory

# ACSP (A Chicken Sandwich Place) inspired menu
MENU_ITEMS = [
    # Sandwiches
    MenuItem(
        id="chicken_sandwich",
        name="ACSP Chicken Sandwich",
        description="A boneless breast of chicken seasoned to perfection, hand-breaded, pressure cooked in 100% refined peanut oil and served on a toasted, buttered bun with dill pickle chips.",
        category=ItemCategory.SANDWICHES,
        base_price=4.79,
        calories=440,
        allergens=["wheat", "soy", "milk"],
        preparation_time=6,
        customizations=["no_pickle", "extra_pickle", "no_butter", "grilled_chicken"]
    ),
    MenuItem(
        id="deluxe_sandwich",
        name="ACSP Deluxe Sandwich",
        description="A boneless breast of chicken seasoned to perfection, hand-breaded, pressure cooked in 100% refined peanut oil and served on a toasted, buttered bun with dill pickle chips, green leaf lettuce, tomato and American cheese.",
        category=ItemCategory.SANDWICHES,
        base_price=5.79,
        calories=550,
        allergens=["wheat", "soy", "milk"],
        preparation_time=7,
        customizations=["no_pickle", "extra_pickle", "no_butter", "no_lettuce", "no_tomato", "no_cheese", "grilled_chicken"]
    ),
    MenuItem(
        id="spicy_sandwich",
        name="Spicy Chicken Sandwich",
        description="A boneless breast of chicken seasoned to perfection, hand-breaded, pressure cooked in 100% refined peanut oil and served on a toasted, buttered bun with dill pickle chips.",
        category=ItemCategory.SANDWICHES,
        base_price=4.79,
        calories=450,
        allergens=["wheat", "soy", "milk"],
        preparation_time=6,
        customizations=["no_pickle", "extra_pickle", "no_butter"]
    ),
    MenuItem(
        id="grilled_sandwich",
        name="Grilled Chicken Sandwich",
        description="A boneless breast of chicken marinated in a special blend of herbs and spices, grilled and served on a toasted, buttered bun with green leaf lettuce and tomato.",
        category=ItemCategory.SANDWICHES,
        base_price=5.39,
        calories=320,
        allergens=["wheat", "soy", "milk"],
        preparation_time=5,
        customizations=["no_lettuce", "no_tomato", "no_butter"]
    ),
    
    # Chicken Strips
    MenuItem(
        id="chicken_strips",
        name="ACSP Chicken Strips",
        description="Tender, juicy strips of chicken breast, hand-breaded and pressure cooked in 100% refined peanut oil. Served with your choice of dipping sauce.",
        category=ItemCategory.CHICKEN_STRIPS,
        base_price=6.79,
        calories=360,
        allergens=["wheat", "soy", "milk"],
        preparation_time=8,
        customizations=["extra_strips", "grilled_strips"]
    ),
    MenuItem(
        id="nuggets_8",
        name="ACSP Nuggets (8 count)",
        description="Bite-sized pieces of boneless chicken breast, seasoned to perfection, hand-breaded and pressure cooked in 100% refined peanut oil.",
        category=ItemCategory.CHICKEN_STRIPS,
        base_price=5.79,
        calories=250,
        allergens=["wheat", "soy", "milk"],
        preparation_time=6,
        customizations=["grilled_nuggets"]
    ),
    MenuItem(
        id="nuggets_12",
        name="ACSP Nuggets (12 count)",
        description="Bite-sized pieces of boneless chicken breast, seasoned to perfection, hand-breaded and pressure cooked in 100% refined peanut oil.",
        category=ItemCategory.CHICKEN_STRIPS,
        base_price=7.79,
        calories=380,
        allergens=["wheat", "soy", "milk"],
        preparation_time=7,
        customizations=["grilled_nuggets"]
    ),
    
    # Salads
    MenuItem(
        id="cobb_salad",
        name="Cobb Salad",
        description="A bed of mixed greens topped with chopped grilled chicken breast, crumbled blue cheese, hard-boiled egg, tomatoes, crispy red bell peppers and bacon.",
        category=ItemCategory.SALADS,
        base_price=9.99,
        calories=520,
        allergens=["milk", "eggs"],
        preparation_time=4,
        customizations=["no_cheese", "no_egg", "no_bacon", "grilled_chicken"]
    ),
    MenuItem(
        id="market_salad",
        name="Market Salad",
        description="A bed of mixed greens topped with grilled chicken breast, blue cheese, crumbled blue cheese, strawberries, blueberries, apples and granola.",
        category=ItemCategory.SALADS,
        base_price=9.99,
        calories=470,
        allergens=["milk", "nuts"],
        preparation_time=4,
        customizations=["no_cheese", "no_nuts", "grilled_chicken"]
    ),
    
    # Sides
    MenuItem(
        id="waffle_fries",
        name="Waffle Potato Fries",
        description="Waffle-cut potatoes cooked in canola oil until crispy outside and tender inside.",
        category=ItemCategory.SIDES,
        base_price=2.79,
        calories=360,
        allergens=[],
        preparation_time=3,
        customizations=["well_done", "light_fry"]
    ),
    MenuItem(
        id="mac_cheese",
        name="Mac & Cheese",
        description="Creamy macaroni and cheese made with a blend of cheeses including Cheddar, Parmesan and Romano.",
        category=ItemCategory.SIDES,
        base_price=3.79,
        calories=450,
        allergens=["wheat", "milk"],
        preparation_time=4,
        customizations=["extra_cheese"]
    ),
    MenuItem(
        id="fruit_cup",
        name="Fruit Cup",
        description="A refreshing mix of mandarin oranges, strawberries, blueberries, red and green apples.",
        category=ItemCategory.SIDES,
        base_price=3.79,
        calories=60,
        allergens=[],
        preparation_time=2,
        customizations=["no_apples", "extra_berries"]
    ),
    
    # Beverages
    MenuItem(
        id="lemonade",
        name="ACSP Lemonade",
        description="Freshly squeezed lemonade made from real lemons.",
        category=ItemCategory.BEVERAGES,
        base_price=2.79,
        calories=200,
        allergens=[],
        preparation_time=1,
        customizations=["light_ice", "no_ice", "extra_lemon"]
    ),
    MenuItem(
        id="sweet_tea",
        name="Sweet Tea",
        description="Freshly brewed sweet tea.",
        category=ItemCategory.BEVERAGES,
        base_price=2.79,
        calories=120,
        allergens=[],
        preparation_time=1,
        customizations=["light_ice", "no_ice", "unsweet_tea"]
    ),
    MenuItem(
        id="coke",
        name="Coca-Cola",
        description="Classic Coca-Cola soft drink.",
        category=ItemCategory.BEVERAGES,
        base_price=2.79,
        calories=140,
        allergens=[],
        preparation_time=1,
        customizations=["light_ice", "no_ice", "diet_coke", "coke_zero"]
    ),
    MenuItem(
        id="milkshake_vanilla",
        name="Vanilla Milkshake",
        description="Hand-spun vanilla milkshake made with real ice cream.",
        category=ItemCategory.BEVERAGES,
        base_price=4.79,
        calories=560,
        allergens=["milk"],
        preparation_time=3,
        customizations=["extra_thick", "light_ice_cream"]
    ),
    MenuItem(
        id="milkshake_chocolate",
        name="Chocolate Milkshake",
        description="Hand-spun chocolate milkshake made with real ice cream.",
        category=ItemCategory.BEVERAGES,
        base_price=4.79,
        calories=580,
        allergens=["milk"],
        preparation_time=3,
        customizations=["extra_thick", "light_ice_cream"]
    ),
    
    # Desserts
    MenuItem(
        id="chocolate_chip_cookie",
        name="Chocolate Chip Cookie",
        description="Warm, soft chocolate chip cookie.",
        category=ItemCategory.DESSERTS,
        base_price=1.99,
        calories=160,
        allergens=["wheat", "milk", "eggs"],
        preparation_time=2,
        customizations=["extra_chocolate_chips"]
    ),
    MenuItem(
        id="brownie",
        name="Chocolate Fudge Brownie",
        description="Rich, fudgy chocolate brownie.",
        category=ItemCategory.DESSERTS,
        base_price=2.99,
        calories=340,
        allergens=["wheat", "milk", "eggs"],
        preparation_time=2,
        customizations=["extra_frosting"]
    ),
    
    # Breakfast Items
    MenuItem(
        id="chicken_biscuit",
        name="ACSP Chicken Biscuit",
        description="A boneless breast of chicken seasoned to perfection, hand-breaded, pressure cooked in 100% refined peanut oil and served on a warm, buttery biscuit.",
        category=ItemCategory.BREAKFAST,
        base_price=4.79,
        calories=450,
        allergens=["wheat", "soy", "milk"],
        preparation_time=5,
        customizations=["no_butter", "grilled_chicken"]
    ),
    MenuItem(
        id="egg_white_grill",
        name="Egg White Grill",
        description="Grilled chicken breast, egg whites and American cheese on a multigrain English muffin.",
        category=ItemCategory.BREAKFAST,
        base_price=4.79,
        calories=300,
        allergens=["wheat", "milk", "eggs"],
        preparation_time=4,
        customizations=["no_cheese", "extra_egg"]
    ),
    
    # Kids Meals
    MenuItem(
        id="kids_nuggets",
        name="Kids ACSP Strips (4 count)",
        description="Four ACSP Nuggets served with a kid's size waffle potato fries and choice of beverage.",
        category=ItemCategory.KIDS_MEALS,
        base_price=6.99,
        calories=400,
        allergens=["wheat", "soy", "milk"],
        preparation_time=5,
        customizations=["grilled_nuggets", "fruit_cup_side"]
    ),
    MenuItem(
        id="kids_sandwich",
        name="Kids ACSP Chicken Sandwich",
        description="A boneless breast of chicken seasoned to perfection, hand-breaded, pressure cooked in 100% refined peanut oil and served on a toasted, buttered bun with dill pickle chips.",
        category=ItemCategory.KIDS_MEALS,
        base_price=6.99,
        calories=420,
        allergens=["wheat", "soy", "milk"],
        preparation_time=5,
        customizations=["no_pickle", "grilled_chicken"]
    ),
]

# Create a dictionary for easy menu item lookup
MENU_DICT = {item.id: item for item in MENU_ITEMS}

def get_menu_by_category(category: ItemCategory) -> list[MenuItem]:
    """Get all menu items in a specific category"""
    return [item for item in MENU_ITEMS if item.category == category]

def get_available_items() -> list[MenuItem]:
    """Get all available menu items"""
    return [item for item in MENU_ITEMS if item.is_available]

def search_menu_items(query: str) -> list[MenuItem]:
    """Search menu items by name or description"""
    query = query.lower()
    return [
        item for item in MENU_ITEMS 
        if query in item.name.lower() or query in item.description.lower()
    ]
