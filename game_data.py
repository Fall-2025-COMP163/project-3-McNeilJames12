"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: James McNeil

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file

    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)

    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # Read file contents safely
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest data file not found: {filename}")
    except OSError as e:
        # Any other low-level file error → corrupted/unreadable
        raise CorruptedDataError(f"Could not read quest data file: {e}")

    # If file is empty or only whitespace, treat as invalid format
    if not content.strip():
        raise InvalidDataFormatError(
            "Quest data file is empty or contains only whitespace."
        )

    quests = {}

    # Split quests by blank lines
    blocks = content.strip().split("\n\n")

    for block in blocks:
        if not block.strip():
            continue  # skip any accidental extra blank sections

        lines = block.splitlines()

        # Use helper to parse one quest block
        quest_data = parse_quest_block(lines)

        # quest_data already has 'quest_id'
        quest_id = quest_data["quest_id"]
        quests[quest_id] = quest_data

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file

    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description

    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # Read file contents safely
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item data file not found: {filename}")
    except OSError as e:
        # Any other low-level file error → corrupted/unreadable
        raise CorruptedDataError(f"Could not read item data file: {e}")

    # Empty or whitespace-only file → invalid format
    if not content.strip():
        raise InvalidDataFormatError(
            "Item data file is empty or contains only whitespace."
        )

    items = {}

    # Each item is separated by a blank line
    blocks = content.strip().split("\n\n")

    for block in blocks:
        if not block.strip():
            continue

        lines = block.splitlines()

        # Use helper to parse one item block
        item_data = parse_item_block(lines)

        # item_data already has 'item_id'
        item_id = item_data["item_id"]
        items[item_id] = item_data

    return items


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields

    Required fields: quest_id, title, description, reward_xp,
                    reward_gold, required_level, prerequisite

    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # Check that all required keys exist
    required_fields = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]

    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {field}")

    # Check that numeric values are actually numbers
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]

    for field in numeric_fields:
        if not isinstance(quest_dict[field], (int, float)):
            raise InvalidDataFormatError(
                f"Quest field '{field}' must be numeric, "
                f"got {type(quest_dict[field]).__name__}"
            )

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields

    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable

    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # Required fields list
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]

    # Check for missing fields
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {field}")

    # Validate type
    valid_types = ["weapon", "armor", "consumable"]

    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(
            f"Invalid item type '{item_dict['type']}'. "
            f"Must be one of: {valid_types}"
        )

    # Validate numeric cost
    if not isinstance(item_dict["cost"], (int, float)):
        raise InvalidDataFormatError(
            f"Item cost must be numeric, "
            f"got {type(item_dict['cost']).__name__}"
        )

    # Validate effect dictionary
    effect = item_dict["effect"]

    if not isinstance(effect, dict):
        raise InvalidDataFormatError("Item effect must be a dictionary.")

    # Effect must contain 'stat' and 'value'
    if "stat" not in effect or "value" not in effect:
        raise InvalidDataFormatError(
            "Item effect must contain 'stat' and 'value' keys."
        )

    # Effect value must be numeric
    if not isinstance(effect["value"], (int, float)):
        raise InvalidDataFormatError(
            f"Item effect value must be numeric, "
            f"got {type(effect['value']).__name__}"
        )

    return True


# ============================================================================
# DEFAULT DATA CREATION
# ============================================================================

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

    data_dir = "data"
    quests_path = os.path.join(data_dir, "quests.txt")
    items_path = os.path.join(data_dir, "items.txt")

    try:
        os.makedirs(data_dir, exist_ok=True)
    except OSError as e:
        # Could not create data directory — serious problem
        print(f"[ERROR] Could not create data directory: {e}")
        # You could raise CorruptedDataError here if your instructor wants that:
        # raise CorruptedDataError(f"Could not create data directory: {e}")
        return

    # Create default quests file if it doesn't exist
    if not os.path.exists(quests_path):
        try:
            with open(quests_path, "w", encoding="utf-8") as f:
                f.write(
                    "QUEST_ID: intro_quest\n"
                    "TITLE: Welcome to Quest Chronicles\n"
                    "DESCRIPTION: Talk to the village elder to begin your journey.\n"
                    "REWARD_XP: 50\n"
                    "REWARD_GOLD: 20\n"
                    "REQUIRED_LEVEL: 1\n"
                    "PREREQUISITE: NONE\n"
                    "\n"
                    "QUEST_ID: goblin_hunt\n"
                    "TITLE: Goblin Menace\n"
                    "DESCRIPTION: Defeat 3 goblins outside the village.\n"
                    "REWARD_XP: 100\n"
                    "REWARD_GOLD: 50\n"
                    "REQUIRED_LEVEL: 2\n"
                    "PREREQUISITE: intro_quest\n"
                )
            print("[INFO] Created default quests.txt")
        except (OSError, PermissionError) as e:
            print(f"[ERROR] Could not create default quests file: {e}")

    # Create default items file if it doesn't exist
    if not os.path.exists(items_path):
        try:
            with open(items_path, "w", encoding="utf-8") as f:
                f.write(
                    "ITEM_ID: sword_iron\n"
                    "NAME: Iron Sword\n"
                    "TYPE: weapon\n"
                    "EFFECT: strength:5\n"
                    "COST: 100\n"
                    "DESCRIPTION: A sturdy iron sword for beginners.\n"
                    "\n"
                    "ITEM_ID: potion_small\n"
                    "NAME: Small Health Potion\n"
                    "TYPE: consumable\n"
                    "EFFECT: health:20\n"
                    "COST: 50\n"
                    "DESCRIPTION: Restores a small amount of health.\n"
                )
            print("[INFO] Created default items.txt")
        except (OSError, PermissionError) as e:
            print(f"[ERROR] Could not create default items file: {e}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary

    Args:
        lines: List of strings representing one quest

    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # Split each line on ":" to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully

    data = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Expect KEY: VALUE format
        if ":" not in line:
            raise InvalidDataFormatError(
                f"Invalid line in quest block (missing colon): {line}"
            )

        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        data[key] = value

    # Required fields
    required_keys = [
        "QUEST_ID",
        "TITLE",
        "DESCRIPTION",
        "REWARD_XP",
        "REWARD_GOLD",
        "REQUIRED_LEVEL",
        "PREREQUISITE"
    ]

    for key in required_keys:
        if key not in data:
            raise InvalidDataFormatError(f"Missing required quest field: {key}")

    # Convert numeric fields
    try:
        reward_xp = int(data["REWARD_XP"])
        reward_gold = int(data["REWARD_GOLD"])
        required_level = int(data["REQUIRED_LEVEL"])
    except ValueError as e:
        raise InvalidDataFormatError(f"Invalid numeric value in quest block: {e}")

    # Handle prerequisite
    prereq_raw = data["PREREQUISITE"]
    prerequisite = None if prereq_raw.upper() == "NONE" else prereq_raw

    return {
        "quest_id": data["QUEST_ID"],
        "title": data["TITLE"],
        "description": data["DESCRIPTION"],
        "reward_xp": reward_xp,
        "reward_gold": reward_gold,
        "required_level": required_level,
        "prerequisite": prerequisite
    }


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary

    Args:
        lines: List of strings representing one item

    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # Split each line on ":" to get key-value pairs
    data = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ":" not in line:
            raise InvalidDataFormatError(
                f"Invalid line in item block (missing colon): {line}"
            )

        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        data[key] = value

    # Required fields
    required_fields = ["ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"]

    for key in required_fields:
        if key not in data:
            raise InvalidDataFormatError(f"Missing required item field: {key}")

    # Convert cost
    try:
        cost = int(data["COST"])
    except ValueError as e:
        raise InvalidDataFormatError(f"Invalid COST value: {e}")

    # Parse EFFECT (stat_name:value)
    effect_raw = data["EFFECT"]

    if ":" not in effect_raw:
        raise InvalidDataFormatError(
            f"Invalid EFFECT format (missing colon): {effect_raw}"
        )

    stat_name, stat_value_str = effect_raw.split(":", 1)
    stat_name = stat_name.strip()
    stat_value_str = stat_value_str.strip()

    if not stat_name:
        raise InvalidDataFormatError("EFFECT stat name cannot be empty.")

    try:
        stat_value = int(stat_value_str)
    except ValueError as e:
        raise InvalidDataFormatError(f"Invalid EFFECT value: {e}")

    return {
        "item_id": data["ITEM_ID"],
        "name": data["NAME"],
        "type": data["TYPE"],
        "effect": {
            "stat": stat_name,
            "value": stat_value
        },
        "cost": cost,
        "description": data["DESCRIPTION"]
    }


# ============================================================================
# HIGH-LEVEL GAME DATA LOADER
# ============================================================================

def load_game_data():
    """
    High-level helper to create default files (if needed),
    load quests and items, validate them, and return a single
    dictionary for the rest of the game to use.

    Returns:
        dict with at least:
            {
                "quests": {quest_id: quest_dict, ...},
                "items": {item_id: item_dict, ...}
            }

    Raises:
        MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # Ensure data directory/files exist so first run works smoothly
    create_default_data_files()

    # Load raw data
    quests = load_quests()
    items = load_items()

    # Validate all quests and items
    for q in quests.values():
        validate_quest_data(q)

    for it in items.values():
        validate_item_data(it)

    # The integration tests are likely expecting this structure:
    return {
        "quests": quests,
        "items": items
    }


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    # Test creating default files
    # create_default_data_files()

    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")

    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
