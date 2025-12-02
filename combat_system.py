"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: James McNeil

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""


import random

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================


def create_enemy(enemy_type):
    """
    Create an enemy based on type

    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100

    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward

    enemy_type = enemy_type.lower()

    enemy_stats = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100},
    }

    if enemy_type not in enemy_stats:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")

    stats = enemy_stats[enemy_type]

    enemy = {
        "name": enemy_type.capitalize(),
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "xp_reward": stats["xp_reward"],
        "gold_reward": stats["gold_reward"],
    }

    return enemy


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"

    return create_enemy(enemy_type)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system

    Manages combat between character and enemy
    """

    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        self.character = character
        self.enemy = enemy

        # Set combat_active flag
        self.combat_active = True

        # Initialize turn counter
        self.turn_count = 0


    def start_battle(self):
        """
        Start the combat loop

        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}

        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        if self.character.get("health", 0) <= 0:
            raise CharacterDeadError("Character is already dead and cannot battle.")

        # Loop until someone dies
        while self.combat_active:

            self.turn_count += 1

            # --- Character attacks first ---
            self.enemy["health"] -= self.character["strength"]

            if self.enemy["health"] <= 0:
                self.enemy["health"] = 0
                self.combat_active = False

                # Award XP and gold if player wins
                return {
                    "winner": "player",
                    "xp_gained": self.enemy.get("xp_reward", 0),
                    "gold_gained": self.enemy.get("gold_reward", 0)
                }

            # --- Enemy attacks next ---
            self.character["health"] -= self.enemy["strength"]

            if self.character["health"] <= 0:
                self.character["health"] = 0
                self.combat_active = False

                return {
                    "winner": "enemy",
                    "xp_gained": 0,
                    "gold_gained": 0
                }



    def player_turn(self):
        """
        Handle player's turn

        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run

        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        if not self.combat_active:
            raise CombatNotActiveError("Cannot act — combat is not active.")

        # Display options
        print("\n--- PLAYER TURN ---")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        # Get player choice
        choice = input("Choose an action (1-3): ").strip()

        # Execute chosen action
        if choice == "1":
            # Basic Attack
            damage = self.character["strength"]
            self.enemy["health"] -= damage
            print(f"You attack the {self.enemy['name']} for {damage} damage!")

            if self.enemy["health"] <= 0:
                self.enemy["health"] = 0
                self.combat_active = False
                print(f"The {self.enemy['name']} has been defeated!")

        elif choice == "2":
            # Special Ability placeholder
            print("You attempt a special ability...")
            print("But nothing happens yet! (Not implemented)")

        elif choice == "3":
            # Try to Run (50% success)
            print("You attempt to run away...")
            if random.random() < 0.5:
                print("You escaped successfully!")
                self.combat_active = False
            else:
                print("You failed to escape!")

        else:
            print("Invalid choice. Turn wasted!")


    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI

        Enemy always attacks

        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        if not self.combat_active:
            raise CombatNotActiveError("Cannot act — combat is not active.")

        print("\n--- ENEMY TURN ---")
        damage = self.enemy["strength"]

        # Calculate damage
        print(f"The {self.enemy['name']} attacks you for {damage} damage!")

        # Apply to character
        self.character["health"] -= damage

        if self.character["health"] <= 0:
            self.character["health"] = 0
            self.combat_active = False
            print("You have been defeated!")

    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        base = attacker["strength"]
        reduction = defender["strength"] // 4

        damage = base - reduction

        # Minimum damage: 1
        if damage < 1:
            damage = 1

        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target["health"] -= damage

        if target["health"] < 0:
            target["health"] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check

        # Enemy dead → player wins
        if self.enemy["health"] <= 0:
            return "player"

        # Player dead → enemy wins
        if self.character["health"] <= 0:
            return "enemy"

        # Otherwise still ongoing
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        success = random.random() < 0.5
        # If successful, set combat_active to False
        if success:
            self.combat_active = False

        return success

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    char_class = character.get("class")

    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    if char_class == "Warrior":
        damage = character["strength"] * 2
        enemy["health"] -= damage
        return f"Warrior uses Power Strike for {damage} damage!"

    elif char_class == "Mage":
        damage = character["magic"] * 2
        enemy["health"] -= damage
        return f"Mage casts Fireball for {damage} damage!"

    elif char_class == "Rogue":
        if random.random() < 0.5:
            damage = character["strength"] * 3
            enemy["health"] -= damage
            return f"Rogue lands a CRITICAL STRIKE for {damage} damage!"
        else:
            return "Rogue attempted Critical Strike but MISSED!"

    elif char_class == "Cleric":
        heal_amount = 30
        before = character["health"]
        character["health"] = min(character["health"] + heal_amount, character["max_health"])
        healed = character["health"] - before
        return f"Cleric heals for {healed} health!"

    else:
        return "Unknown class — ability fails."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    damage = character["strength"] * 2
    enemy["health"] -= damage

    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"{character['name']} uses Power Strike for {damage} damage!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    damage = character["magic"] * 2
    enemy["health"] -= damage

    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"{character['name']} casts Fireball for {damage} damage!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    if random.random() < 0.5:
        damage = character["strength"] * 3
        enemy["health"] -= damage

        if enemy["health"] < 0:
            enemy["health"] = 0

        return f"{character['name']} lands a CRITICAL STRIKE for {damage} damage!"
    else:
        return f"{character['name']} attempted Critical Strike but MISSED!"

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    before = character["health"]

    character["health"] = min(character["health"] + heal_amount, character["max_health"])

    actual_healed = character["health"] - before

    return f"{character['name']} heals for {actual_healed} HP!"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    health_ok = character.get("health", 0) > 0
    not_in_battle = not character.get("in_battle", False)

    return health_ok and not_in_battle

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0)
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")


def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
         print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
         'name': 'Hero',
         'class': 'Warrior',
         'health': 120,
         'max_health': 120,
         'strength': 15,
         'magic': 5
     }
    #
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

