"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: James McNeil

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""



from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)


from collections import Counter

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    inventory = character.get("inventory", [])

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    # Add item_id to character['inventory'] list
    inventory.append(item_id)
    character["inventory"] = inventory

    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    inventory = character.get("inventory", [])

    # Check if item exists in inventory
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    # Remove item from list
    inventory.remove(item_id)
    character["inventory"] = inventory

    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    return item_id in character.get("inventory", [])


def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    return character.get("inventory", []).count(item_id)


def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    current_items = len(character.get("inventory", []))
    return MAX_INVENTORY_SIZE - current_items

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    removed_items = character.get("inventory", []).copy()

    # Clear character's inventory list
    character["inventory"] = []

    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory

    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data

    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped

    Returns: String describing what happened
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # Check if character has the item
    inventory = character.get("inventory", [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")

    # Check if item type is 'consumable'
    if item_data.get("type") != "consumable":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a consumable.")

    # Effect can be either:
    # - a dict: {"stat": ..., "value": ...}
    # - a string: "stat:value" (e.g., "health:20")
    effect = item_data.get("effect")
    if isinstance(effect, dict):
        stat_name = effect.get("stat")
        stat_value = effect.get("value", 0)
    elif isinstance(effect, str):
        # Use helper to parse "health:20" → ("health", 20)
        stat_name, stat_value = parse_item_effect(effect)
    else:
        raise ValueError(f"Invalid effect data for item '{item_id}': {effect!r}")

    # Default message
    item_name = item_data.get("name", item_id)
    char_name = character.get("name", "Character")

    # Apply effect to character
    if stat_name == "health":
        before = character.get("health", 0)
        # Ensure we don't go over max_health if it exists
        max_health = character.get("max_health", before + stat_value)
        character["health"] = min(before + stat_value, max_health)
        healed = character["health"] - before
        message = f"{char_name} used {item_name} and healed {healed} HP."
    else:
        # For other stats, use helper so we respect max_health rules, etc.
        apply_stat_effect(character, stat_name, stat_value)
        message = f"{char_name} used {item_name} and gained +{stat_value} {stat_name}."

    # Remove item from inventory
    inventory.remove(item_id)
    character["inventory"] = inventory

    return message


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    inventory = character.get("inventory", [])

    # Check item exists and is type 'weapon'
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")

    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon.")

    # Handle unequipping current weapon if exists
    old_weapon_id = character.get("equipped_weapon")
    old_weapon_bonus = character.get("equipped_weapon_bonus", 0)

    if old_weapon_id is not None:
        # Remove old bonus
        character["strength"] -= old_weapon_bonus
        # Add old weapon back to inventory
        inventory.append(old_weapon_id)

    # Parse effect and apply to character stats
    effect = item_data.get("effect", {})
    stat_name = effect.get("stat")
    stat_value = effect.get("value", 0)

    # For this project, weapon stat should be strength
    if stat_name == "strength":
        character["strength"] += stat_value
    else:
        # If some other stat is used, still apply it generically
        if stat_name in character:
            character[stat_name] += stat_value
    # Store equipped_weapon in character dictionary
    character["equipped_weapon"] = item_id
    character["equipped_weapon_bonus"] = stat_value

    # Remove item from inventory
    inventory.remove(item_id)
    character["inventory"] = inventory

    if old_weapon_id is None:
        return f"{character['name']} equipped {item_data['name']}."
    else:
        return f"{character['name']} swapped {old_weapon_id} for {item_data['name']}."



def equip_armor(character, item_id, item_data):
    """
    Equip armor

    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary

    Armor effect format: "max_health:10" (adds 10 to max_health)

    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory

    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor

    inventory = character.get("inventory", [])

    # Check if item exists
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")

    # Check type
    if item_data.get("type") != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor.")

    # Handle unequipping current armor if exists
    old_armor_id = character.get("equipped_armor")
    old_armor_bonus = character.get("equipped_armor_bonus", 0)

    if old_armor_id is not None:
        # Remove previous armor's bonus
        character["max_health"] -= old_armor_bonus

        # Make sure current health doesn't exceed new max
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]

        # Return old armor to inventory
        inventory.append(old_armor_id)

    # Parse effect and apply to character stats
    effect = item_data.get("effect", {})
    stat_name = effect.get("stat")
    stat_value = effect.get("value", 0)

    if stat_name == "max_health":
        character["max_health"] += stat_value

        # Optionally auto-heal the difference — depends on assignment rules
        # Usually we DO NOT heal automatically unless project says otherwise

    else:
        # Generic stat support, just in case
        if stat_name in character:
            character[stat_name] += stat_value

    # Store equipped armor info
    character["equipped_armor"] = item_id
    character["equipped_armor_bonus"] = stat_value

    # Remove armor from inventory
    inventory.remove(item_id)
    character["inventory"] = inventory

    if old_armor_id is None:
        return f"{character['name']} equipped {item_data['name']}."
    else:
        return f"{character['name']} swapped {old_armor_id} for {item_data['name']}."




def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory

    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping

    # Check if weapon is equipped
    weapon_id = character.get("equipped_weapon")
    bonus = character.get("equipped_weapon_bonus", 0)

    if weapon_id is None:
        return None  # nothing to unequip

    # Remove stat bonuses
    character["strength"] -= bonus
    if character["strength"] < 0:
        character["strength"] = 0  # safety fallback

    # Add weapon back to inventory
    inventory = character.get("inventory", [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip — inventory is full.")

    inventory.append(weapon_id)
    character["inventory"] = inventory

    # Clear equipped_weapon from character
    character["equipped_weapon"] = None
    character["equipped_weapon_bonus"] = 0

    return weapon_id




def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory

    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping

    armor_id = character.get("equipped_armor")
    bonus = character.get("equipped_armor_bonus", 0)

    # If no armor equipped
    if armor_id is None:
        return None

    # Remove armor's bonus (usually max_health)
    character["max_health"] -= bonus
    if character["max_health"] < 1:
        character["max_health"] = 1  # safety fallback

    # Ensure health does not exceed new max
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    # Add armor back into inventory
    inventory = character.get("inventory", [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip — inventory is full.")

    inventory.append(armor_id)
    character["inventory"] = inventory

    # Clear equipped armor fields
    character["equipped_armor"] = None
    character["equipped_armor_bonus"] = 0

    return armor_id


# ============================================================================
# SHOP SYSTEM
# ============================================================================



def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop

    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field

    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing

    cost = item_data.get("cost", 0)
    inventory = character.get("inventory", [])

    # Check if character has enough gold
    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError(
            f"Not enough gold to purchase '{item_id}'. Cost: {cost}, Gold: {character.get('gold', 0)}"
        )

    # Check if inventory has space
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full. Cannot purchase item.")

    # Subtract gold from character
    character["gold"] -= cost

    # Add item to inventory
    inventory.append(item_id)
    character["inventory"] = inventory

    return True




def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost

    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field

    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling

    inventory = character.get("inventory", [])

    # Check if character has item
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    # Calculate sell price (cost // 2)
    cost = item_data.get("cost", 0)
    sell_price = cost // 2

    # Remove item from inventory
    inventory.remove(item_id)
    character["inventory"] = inventory

    # Add gold to character
    character["gold"] = character.get("gold", 0) + sell_price

    return sell_price


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value

    Args:
        effect_string: String in format "stat_name:value"

    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    parts = effect_string.split(":")

    if len(parts) != 2:
        raise ValueError(f"Invalid effect format: {effect_string}")

    stat_name = parts[0].strip()
    value_string = parts[1].strip()

    # Convert value to integer
    try:
        value = int(value_string)
    except ValueError:
        raise ValueError(f"Invalid numeric value in effect: {value_string}")

    return stat_name, value


def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character

    Valid stats: health, max_health, strength, magic

    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application

    # Add value to character[stat_name]
    if stat_name not in character:
        raise ValueError(f"Invalid stat: {stat_name}")

    character[stat_name] += value

    # If stat is health, ensure it doesn't exceed max_health
    if stat_name == "health":
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]

        # Optional safety: prevent negative HP
        if character["health"] < 0:
            character["health"] = 0

    # Optional: prevent negative stats for others
    if stat_name in ["strength", "magic", "max_health"] and character[stat_name] < 0:
        character[stat_name] = 0




def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way

    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data

    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display

    inventory = character.get("inventory", [])

    if not inventory:
        print("\n=== INVENTORY ===")
        print("(empty)")
        return

    # Count items (some may appear multiple times)
    counts = Counter(inventory)

    print("\n=== INVENTORY ===")
    print(f"{'ITEM NAME':<20} {'TYPE':<12} {'QTY':<5}")

    # Display with item names from item_data_dict
    for item_id, quantity in counts.items():
        data = item_data_dict.get(item_id, {})

        item_name = data.get("name", item_id)
        item_type = data.get("type", "unknown")

        print(f"{item_name:<20} {item_type:<12} {quantity:<5}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    # 
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

