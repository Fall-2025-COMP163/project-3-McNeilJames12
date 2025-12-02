"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: James McNeil
AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""



# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice

    Options:
    1. New Game
    2. Load Game
    3. Exit

    Returns: Integer choice (1-3)
    """
    while True:
        print("\n=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice in ("1", "2", "3"):
            return int(choice)

        print("Invalid choice. Please enter 1, 2, or 3.")


def new_game():
    """
    Start a new game

    Prompts for:
    - Character name
    - Character class

    Creates character and starts game loop
    """
    global current_character

    # Get character name from user
    name = input("Enter your character's name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter your character's name: ").strip()

    # Get character class from user
    print("\nChoose a class:")
    print(" - Warrior")
    print(" - Mage")
    print(" - Rogue")
    print(" - Cleric")

    while True:
        char_class = input("Enter your character's class: ").strip().title()

        # Try to create character with character_manager.create_character()
        try:
            current_character = character_manager.create_character(name, char_class)
            break
        except InvalidCharacterClassError as e:
            print(f"Invalid class: {e}")
            print("Please choose from: Warrior, Mage, Rogue, Cleric")

    print(f"\nCreated {current_character['name']} the {current_character['class']}!")

    # Save character
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Warning: Could not save game: {e}")

    # Start game loop
    game_loop()


def load_game():
    """
    Load an existing saved game

    Shows list of saved characters
    Prompts user to select one
    """
    global current_character

    # Get list of saved characters
    saved_names = character_manager.list_saved_characters()

    if not saved_names:
        print("\nNo saved games found.")
        return

    print("\n=== LOAD GAME ===")
    for idx, name in enumerate(saved_names, start=1):
        print(f"{idx}. {name}")

    # Get user choice
    while True:
        choice = input(f"Select a save (1-{len(saved_names)}) or 'c' to cancel: ").strip()

        if choice.lower() == "c":
            print("Load cancelled.")
            return

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        choice_num = int(choice)
        if 1 <= choice_num <= len(saved_names):
            selected_name = saved_names[choice_num - 1]
            break
        else:
            print(f"Please enter a number between 1 and {len(saved_names)}.")

    # Try to load character with character_manager.load_character()
    try:
        current_character = character_manager.load_character(selected_name)
        print(f"\nLoaded character: {current_character['name']} the {current_character['class']}")
    except CharacterNotFoundError:
        print("Error: Save file not found for that character.")
        return
    except SaveFileCorruptedError as e:
        print(f"Error: Save file is corrupted: {e}")
        return

    # Start game loop
    game_loop()


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character

    game_running = True

    while game_running:
        print("\n=== GAME MENU ===")
        print("1. View Character Status")
        print("2. View Inventory")
        print("3. Exit Game")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            # View Character Status
            print("\n=== CHARACTER STATUS ===")
            print(f"Name:   {current_character.get('name', 'Unknown')}")
            print(f"Class:  {current_character.get('class', 'Unknown')}")
            print(f"Level:  {current_character.get('level', 1)}")
            print(f"HP:     {current_character.get('health', 0)}/{current_character.get('max_health', 0)}")
            print(f"STR:    {current_character.get('strength', 0)}")
            print(f"MAG:    {current_character.get('magic', 0)}")
            print(f"XP:     {current_character.get('experience', 0)}")
            print(f"Gold:   {current_character.get('gold', 0)}")

        elif choice == "2":
            # View Inventory
            print("\n=== INVENTORY ===")
            inv = current_character.get("inventory", [])
            if not inv:
                print("(empty)")
            else:
                for idx, item_id in enumerate(inv, start=1):
                    print(f"{idx}. {item_id}")

        elif choice == "3":
            # Exit Game
            print("Exiting game...")
            game_running = False

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

        # Save game after each action
        try:
            character_manager.save_character(current_character)
        except Exception as e:
            print(f"Warning: Could not save game: {e}")


def game_menu():
    """
    Display game menu and get player choice

    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit

    Returns: Integer choice (1-6)
    """
    while True:
        print("\n=== GAME MENU ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")

        choice = input("Enter choice (1-6): ").strip()

        if choice in ("1", "2", "3", "4", "5", "6"):
            return int(choice)

        print("Invalid choice. Please enter a number between 1 and 6.")


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character

    if current_character is None:
        print("No character loaded.")
        return

    print("\n=== CHARACTER STATS ===")
    print(f"Name:        {current_character.get('name', 'Unknown')}")
    print(f"Class:       {current_character.get('class', 'Unknown')}")
    print(f"Level:       {current_character.get('level', 1)}")
    print(f"Health:      {current_character.get('health', 0)}/{current_character.get('max_health', 0)}")
    print(f"Strength:    {current_character.get('strength', 0)}")
    print(f"Magic:       {current_character.get('magic', 0)}")
    print(f"Gold:        {current_character.get('gold', 0)}")

    level = current_character.get("level", 1)
    xp = current_character.get("experience", 0)
    next_level_xp = level * 100
    print(f"Experience:  {xp} / {next_level_xp} (Next Level)")

    weapon = current_character.get("equipped_weapon")
    armor = current_character.get("equipped_armor")

    print("\nEquipped Gear:")
    print(f" - Weapon: {weapon if weapon else 'None'}")
    print(f" - Armor:  {armor if armor else 'None'}")

    active = current_character.get("active_quests", [])
    completed = current_character.get("completed_quests", [])

    print("\nQuest Progress:")
    print(f"Active Quests:    {len(active)}")
    for q in active:
        print(f"  - {q}")

    print(f"Completed Quests: {len(completed)}")
    for q in completed:
        print(f"  ✓ {q}")


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items

    if current_character is None:
        print("No character loaded.")
        return

    while True:
        print("\n=== INVENTORY MENU ===")
        inventory_system.display_inventory(current_character, all_items)

        print("\nOptions:")
        print("1. Use Item")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Drop Item")
        print("5. Back to Game Menu")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "5":
            break

        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice. Please enter 1-5.")
            continue

        item_id = input("Enter item ID to act on: ").strip()
        if not item_id:
            print("Item ID cannot be empty.")
            continue

        item_data = all_items.get(item_id)
        if item_data is None:
            print(f"Unknown item ID: {item_id}")
            continue

        try:
            if choice == "1":
                message = inventory_system.use_item(current_character, item_id, item_data)
                print(message)

            elif choice == "2":
                message = inventory_system.equip_weapon(current_character, item_id, item_data)
                print(message)

            elif choice == "3":
                message = inventory_system.equip_armor(current_character, item_id, item_data)
                print(message)

            elif choice == "4":
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"Dropped '{item_id}' from inventory.")

        except ItemNotFoundError as e:
            print(f"Error: {e}")
        except InvalidItemTypeError as e:
            print(f"Error: {e}")
        except InventoryFullError as e:
            print(f"Error: {e}")


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests

    if current_character is None:
        print("No character loaded.")
        return

    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "7":
            break

        try:
            if choice == "1":
                active = current_character.get("active_quests", [])
                if not active:
                    print("\nNo active quests.")
                else:
                    print("\n=== ACTIVE QUESTS ===")
                    for qid in active:
                        qdata = all_quests.get(qid, {})
                        title = qdata.get("title", qid)
                        desc = qdata.get("description", "")
                        print(f"- {title} ({qid})")
                        if desc:
                            print(f"  {desc}")

            elif choice == "2":
                print("\n=== AVAILABLE QUESTS ===")
                level = current_character.get("level", 1)
                active = set(current_character.get("active_quests", []))
                completed = set(current_character.get("completed_quests", []))

                available_any = False
                for qid, qdata in all_quests.items():
                    if qid in active or qid in completed:
                        continue

                    required_level = qdata.get("required_level", 1)
                    prereq = qdata.get("prerequisite")

                    if level < required_level:
                        continue

                    if prereq and prereq not in completed:
                        continue

                    available_any = True
                    print(f"- {qdata.get('title', qid)} ({qid})")
                    print(
                        f"  Req Lv: {required_level}, Reward: {qdata.get('reward_xp', 0)} XP, {qdata.get('reward_gold', 0)} gold"
                    )

                if not available_any:
                    print("No quests currently available.")

            elif choice == "3":
                completed = current_character.get("completed_quests", [])
                if not completed:
                    print("\nNo completed quests yet.")
                else:
                    print("\n=== COMPLETED QUESTS ===")
                    for qid in completed:
                        qdata = all_quests.get(qid, {})
                        title = qdata.get("title", qid)
                        print(f"✓ {title} ({qid})")

            elif choice == "4":
                quest_id = input("Enter quest ID to accept: ").strip()
                if quest_id not in all_quests:
                    print("That quest does not exist.")
                    continue

                active = current_character.get("active_quests", [])
                completed = current_character.get("completed_quests", [])

                if quest_id in active:
                    print("You already have that quest active.")
                    continue
                if quest_id in completed:
                    print("You have already completed that quest.")
                    continue

                qdata = all_quests[quest_id]
                required_level = qdata.get("required_level", 1)
                prereq = qdata.get("prerequisite")

                if current_character.get("level", 1) < required_level:
                    print("You do not meet the level requirement for this quest.")
                    continue

                if prereq and prereq not in completed:
                    print(f"You must complete '{prereq}' first.")
                    continue

                active.append(quest_id)
                current_character["active_quests"] = active
                print(f"Accepted quest: {qdata.get('title', quest_id)}")

            elif choice == "5":
                quest_id = input("Enter quest ID to abandon: ").strip()
                active = current_character.get("active_quests", [])
                if quest_id not in active:
                    print("That quest is not currently active.")
                    continue

                active.remove(quest_id)
                current_character["active_quests"] = active
                print(f"Abandoned quest: {quest_id}")

            elif choice == "6":
                quest_id = input("Enter quest ID to complete: ").strip()
                active = current_character.get("active_quests", [])
                completed = current_character.get("completed_quests", [])

                if quest_id not in active:
                    print("That quest is not currently active.")
                    continue

                active.remove(quest_id)
                completed.append(quest_id)
                current_character["active_quests"] = active
                current_character["completed_quests"] = completed

                qdata = all_quests.get(quest_id, {})
                xp = qdata.get("reward_xp", 0)
                gold = qdata.get("reward_gold", 0)

                try:
                    character_manager.gain_experience(current_character, xp)
                    character_manager.add_gold(current_character, gold)
                    print(f"Completed quest: {qdata.get('title', quest_id)}")
                    print(f"Rewards: {xp} XP, {gold} gold")
                except Exception as e:
                    print(f"Quest completed, but error applying rewards: {e}")

            else:
                print("Invalid choice. Please enter 1-7.")

        except Exception as e:
            print(f"Quest error: {e}")


def explore():
    """Find and fight random enemies"""
    global current_character

    if current_character is None:
        print("No character loaded.")
        return

    # Use combat_system.can_character_fight
    try:
        if not combat_system.can_character_fight(current_character):
            print("You are not in condition to fight right now.")
            return
    except Exception as e:
        print(f"Error checking fight readiness: {e}")
        return

    level = current_character.get("level", 1)
    try:
        enemy = combat_system.get_random_enemy_for_level(level)
    except Exception as e:
        print(f"Error generating enemy: {e}")
        return

    print(f"\nYou encounter a {enemy['name']}!")
    print(f"Enemy Stats -> HP: {enemy['health']}, STR: {enemy['strength']}, MAG: {enemy['magic']}")

    battle = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = battle.start_battle()
    except CharacterDeadError as e:
        print(f"Cannot start battle: {e}")
        return
    except Exception as e:
        print(f"Unexpected combat error: {e}")
        return

    winner = result.get("winner")
    xp_gained = result.get("xp_gained", 0)
    gold_gained = result.get("gold_gained", 0)

    if winner == "player":
        print(f"\nYou defeated the {enemy['name']}!")
        print(f"Rewards: {xp_gained} XP, {gold_gained} gold")

        try:
            if xp_gained > 0:
                character_manager.gain_experience(current_character, xp_gained)
            if gold_gained != 0:
                character_manager.add_gold(current_character, gold_gained)
        except CharacterDeadError as e:
            print(f"Error applying rewards: {e}")
        except Exception as e:
            print(f"Unexpected error applying rewards: {e}")

    elif winner == "enemy":
        print(f"\nYou were defeated by the {enemy['name']}...")
        print("You collapse and your vision fades. Maybe try again after resting.")
    else:
        print("\nThe battle ended in an unexpected way.")


def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items

    if current_character is None:
        print("No character loaded.")
        return

    while True:
        print("\n=== SHOP ===")
        print(f"Your Gold: {current_character.get('gold', 0)}\n")

        print("Items for Sale:")
        print(f"{'ID':<15} {'NAME':<20} {'TYPE':<12} {'COST':<6}")
        for item_id, data in all_items.items():
            print(
                f"{item_id:<15} {data.get('name', 'Unknown'):<20} {data.get('type', 'Unknown'):<12} {data.get('cost', 0):<6}"
            )

        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "3":
            print("Leaving shop...")
            break

        elif choice == "1":
            item_id = input("Enter item ID to buy: ").strip()

            if item_id not in all_items:
                print("Invalid item ID.")
                continue

            item_data = all_items[item_id]

            try:
                inventory_system.purchase_item(current_character, item_id, item_data)
                print(f"Purchased {item_data['name']} for {item_data['cost']} gold.")
            except InsufficientResourcesError as e:
                print(f"Error: {e}")
            except InventoryFullError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected shop error: {e}")

        elif choice == "2":
            print("\nYour Inventory:")
            inventory_system.display_inventory(current_character, all_items)

            item_id = input("Enter item ID to sell: ").strip()

            if item_id not in current_character.get("inventory", []):
                print("You don't have that item in your inventory.")
                continue

            item_data = all_items.get(item_id, None)
            if item_data is None:
                print("Error: Item data not found.")
                continue

            try:
                amount = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"Sold {item_data['name']} for {amount} gold.")
            except ItemNotFoundError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error during sale: {e}")

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character

    if current_character is None:
        print("No character loaded. Cannot save.")
        return

    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")


def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items

    all_quests = {}
    all_items = {}

    try:
        all_quests = game_data.load_quests()
    except MissingDataFileError:
        print("Quest data file missing. Creating default data files...")
        game_data.create_default_data_files()
        try:
            all_quests = game_data.load_quests()
        except (InvalidDataFormatError, CorruptedDataError) as e:
            print(f"Error loading quest data after creating defaults: {e}")
            all_quests = {}
    except (InvalidDataFormatError, CorruptedDataError) as e:
        print(f"Error loading quest data: {e}")
        all_quests = {}

    try:
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Item data file missing. Creating default data files...")
        game_data.create_default_data_files()
        try:
            all_items = game_data.load_items()
        except (InvalidDataFormatError, CorruptedDataError) as e:
            print(f"Error loading item data after creating defaults: {e}")
            all_items = {}
    except (InvalidDataFormatError, CorruptedDataError) as e:
        print(f"Error loading item data: {e}")
        all_items = {}


def handle_character_death():
    """Handle character death"""
    global current_character, game_running

    # Not implemented yet
    print("You have died. (death handling not implemented yet)")
    game_running = False


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""

    display_welcome()

    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return

    while True:
        choice = main_menu()

        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()
