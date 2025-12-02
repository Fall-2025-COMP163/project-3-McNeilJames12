"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: James McNeil

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""


import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    valid_classes = ['Warrior', 'Mage', 'Rogue', 'Cleric']
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f'{character_class} is not a valid class')
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }
    stats = base_stats[character_class]

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    try:
        os.makedirs(save_directory, exist_ok=True)

        filename = f"{character['name']}_save.txt"
        filepath = os.path.join(save_directory, filename)

        # Prepare list fields as comma-separated values
        inventory = character.get("inventory", [])
        active_quests = character.get("active_quests", [])
        completed_quests = character.get("completed_quests", [])

        inventory_str = ",".join(map(str, inventory))
        active_quests_str = ",".join(map(str, active_quests))
        completed_quests_str = ",".join(map(str, completed_quests))

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"NAME: {character.get('name', '')}\n")
            f.write(f"CLASS: {character.get('class', '')}\n")
            f.write(f"LEVEL: {character.get('level', 1)}\n")
            f.write(f"HEALTH: {character.get('health', 0)}\n")
            f.write(f"MAX_HEALTH: {character.get('max_health', 0)}\n")
            f.write(f"STRENGTH: {character.get('strength', 0)}\n")
            f.write(f"MAGIC: {character.get('magic', 0)}\n")
            f.write(f"EXPERIENCE: {character.get('experience', 0)}\n")
            f.write(f"GOLD: {character.get('gold', 0)}\n")
            f.write(f"INVENTORY: {inventory_str}\n")
            f.write(f"ACTIVE_QUESTS: {active_quests_str}\n")
            f.write(f"COMPLETED_QUESTS: {completed_quests_str}\n")

        return True
    except (PermissionError, IOError) as e:
        print(f'Failed to save character: {e}')
        raise

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Save file for '{character_name}' not found.")

    # Try to read file → SaveFileCorruptedError
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, IOError) as e:
        raise SaveFileCorruptedError(f"Could not read save file: {e}")

    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    data = {}
    for line in lines:
        line = line.strip()
        if not line:
            # skip empty lines if any
            continue

        if ":" not in line:
            raise InvalidSaveDataError(f"Invalid line (missing colon): {line}")

        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()
        data[key] = value

    required_keys = [
        "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH",
        "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD",
        "INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"
    ]

    for key in required_keys:
        if key not in data:
            raise InvalidSaveDataError(f"Missing required field: {key}")

    # Convert numeric fields and handle format errors
    try:
        level = int(data["LEVEL"])
        health = int(data["HEALTH"])
        max_health = int(data["MAX_HEALTH"])
        strength = int(data["STRENGTH"])
        magic = int(data["MAGIC"])
        experience = int(data["EXPERIENCE"])
        gold = int(data["GOLD"])
    except ValueError as e:
        raise InvalidSaveDataError(f"Invalid numeric value in save data: {e}")

    def parse_list_field(field_value: str):
        if not field_value:
            return []
        return [item for item in field_value.split(",") if item]

    inventory = parse_list_field(data["INVENTORY"])
    active_quests = parse_list_field(data["ACTIVE_QUESTS"])
    completed_quests = parse_list_field(data["COMPLETED_QUESTS"])

    # Build the character dictionary to return
    character = {
        "name": data["NAME"],
        "class": data["CLASS"],
        "level": level,
        "health": health,
        "max_health": max_health,
        "strength": strength,
        "magic": magic,
        "experience": experience,
        "gold": gold,
        "inventory": inventory,
        "active_quests": active_quests,
        "completed_quests": completed_quests,
    }

    return character


def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    if not os.path.exists(save_directory):
        return []
    # Extract character names from filenames
    try:
        files = os.listdir(save_directory)
    except (OSError, IOError):
        # If directory exists but can't be read → treat as empty
        return []

    save_files = [f for f in files if f.endswith("_save.txt")]

    character_names = [f.replace("_save.txt", "") for f in save_files]

    return character_names


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character '{character_name}' does not have a save file.")

    # Attempt deletion (IOError/PermissionError will naturally propagate)
    os.remove(filepath)

    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    if character.get("health", 0) <= 0:
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain experience.")

    # Add experience
    character["experience"] += xp_amount

    # Check for level up (can level up multiple times)
    # Update stats on level up
    while True:
        current_level = character["level"]
        level_up_xp = current_level * 100

        if character["experience"] < level_up_xp:
            break  # no more level-ups possible

        # Perform level up
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2

        # Reduce XP by the cost for this level
        character["experience"] -= level_up_xp

        # Restore health to new max_health
        character["health"] = character["max_health"]

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    new_total = character.get("gold", 0) + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative.")
    # Update character's gold
    character["gold"] = new_total

    return new_total

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    current_health = character.get("health", 0)
    max_health = character.get("max_health", 0)

    # Calculate actual healing (don't exceed max_health)
    healable_amount = max_health - current_health
    actual_healed = min(amount, healable_amount)
    # Update character health
    character["health"] = current_health + actual_healed

    return actual_healed


def revive_character(character):
    """
    Revive a dead character with 50% health

    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health

    # Only revive if character is dead
    if character.get("health", 0) > 0:
        return False  # character is already alive

    max_hp = character.get("max_health", 0)
    half_hp = max_hp // 2  # floor division for game-style rounding

    character["health"] = half_hp

    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields

    Required fields: name, class, level, health, max_health,
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests

    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation

    # Check all required keys exist
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")

    # Check that numeric values are numbers
    numeric_fields = [
        "level", "health", "max_health", "strength",
        "magic", "experience", "gold"
    ]

    for field in numeric_fields:
        if not isinstance(character[field], (int, float)):
            raise InvalidSaveDataError(
                f"Field '{field}' must be numeric (int or float), got {type(character[field]).__name__}"
            )

    # Check that lists are actually lists
    list_fields = ["inventory", "active_quests", "completed_quests"]

    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(
                f"Field '{field}' must be a list, got {type(character[field]).__name__}"
            )

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    # ----------- TEST: Character Creation -----------
    try:
        char = create_character("TestHero", "Warrior")
        print(f"[CREATED] {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']} STR={char['strength']} MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"[ERROR] Invalid class: {e}")
        exit()

    # ----------- TEST: Saving -----------
    try:
        save_character(char)
        print("[SAVED] Character saved successfully.")
    except Exception as e:
        print(f"[ERROR] Save error: {e}")

    # ----------- TEST: Loading -----------
    try:
        loaded = load_character("TestHero")
        print(f"[LOADED] Character loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("[ERROR] Character not found")
    except SaveFileCorruptedError:
        print("[ERROR] Save file corrupted")

    # ----------- TEST: Gaining Experience / Leveling-Up -----------
    print("\n=== LEVELING TEST ===")
    print(f"Current Level: {loaded['level']} | XP: {loaded['experience']}")
    gain_experience(loaded, 250)  # should level up at least once
    print(f"After XP gain: Level={loaded['level']} | XP={loaded['experience']}")
    print(f"New Stats: HP={loaded['health']} / {loaded['max_health']}, STR={loaded['strength']}, MAG={loaded['magic']}")

    # ----------- TEST: Gold Management -----------
    print("\n=== GOLD TEST ===")
    print(f"Gold before: {loaded['gold']}")
    add_gold(loaded, 50)
    print(f"Gold after +50: {loaded['gold']}")
    try:
        add_gold(loaded, -1000)  # Should raise ValueError
    except ValueError as e:
        print(f"[EXPECTED ERROR] {e}")

    # ----------- TEST: Healing -----------
    print("\n=== HEALING TEST ===")
    loaded["health"] = 20
    healed = heal_character(loaded, 50)
    print(f"Healed for {healed} → New HP: {loaded['health']}")

    # ----------- TEST: Revival -----------
    print("\n=== REVIVE TEST ===")
    loaded["health"] = 0
    revived = revive_character(loaded)
    print(f"Revived? {revived} → HP: {loaded['health']}")

    # ----------- TEST: Listing Saves -----------
    print("\n=== LIST SAVED CHARACTERS ===")
    saves = list_saved_characters()
    print("Saved characters:", saves)

    # ----------- TEST: Deleting Save -----------
    print("\n=== DELETE TEST ===")
    try:
        delete_character("TestHero")
        print("[DELETED] TestHero save file removed.")
    except CharacterNotFoundError:
        print("[ERROR] Tried to delete but not found.")


