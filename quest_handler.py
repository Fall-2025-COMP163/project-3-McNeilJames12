"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: James McNeil

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

import character_manager  # to grant XP and gold

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest

    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data

    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active

    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    quest = quest_data_dict[quest_id]

    # Make sure character has the needed quest lists
    character.setdefault("active_quests", [])
    character.setdefault("completed_quests", [])

    # Check level requirement
    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        raise InsufficientLevelError(
            f"Level {required_level} required to accept this quest."
        )

    # Check prerequisite (if not "NONE")
    prerequisite_id = quest.get("prerequisite", "NONE")
    if prerequisite_id not in ("NONE", None, ""):
        if prerequisite_id not in character["completed_quests"]:
            raise QuestRequirementsNotMetError(
                f"Prerequisite quest '{prerequisite_id}' not completed."
            )

    # Check not already completed
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed.")

    # Check not already active
    if quest_id in character["active_quests"]:
        # Treat "already active" as "requirements not met"
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' is already active.")

    # Add to character['active_quests]
    character["active_quests"].append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards

    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data

    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)

    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    quest = quest_data_dict[quest_id]

    character.setdefault("active_quests", [])
    character.setdefault("completed_quests", [])

    # Check quest is active
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    # Remove from active_quests
    character["active_quests"].remove(quest_id)

    # Add to completed_quests
    if quest_id not in character["completed_quests"]:
        character["completed_quests"].append(quest_id)

    # Grant rewards (use character_manager.gain_experience and add_gold)
    reward_xp = quest.get("reward_xp", 0)
    reward_gold = quest.get("reward_gold", 0)

    if reward_xp:
        character_manager.gain_experience(character, reward_xp)
    if reward_gold:
        character_manager.add_gold(character, reward_gold)

    # Return reward summary
    return {
        "xp": reward_xp,
        "gold": reward_gold
    }


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it

    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    character.setdefault("active_quests", [])

    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    character["active_quests"].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests

    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    character.setdefault("active_quests", [])
    active_quests = []

    for qid in character["active_quests"]:
        if qid in quest_data_dict:
            active_quests.append(quest_data_dict[qid])

    return active_quests


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests

    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    character.setdefault("completed_quests", [])
    completed_quests = []

    for qid in character["completed_quests"]:
        if qid in quest_data_dict:
            completed_quests.append(quest_data_dict[qid])

    return completed_quests


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept

    Available = meets level req + prerequisite done + not completed + not active

    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    character.setdefault("active_quests", [])
    character.setdefault("completed_quests", [])

    available = []
    for quest_id, quest in quest_data_dict.items():
        # Skip if already active or completed
        if quest_id in character["active_quests"]:
            continue
        if quest_id in character["completed_quests"]:
            continue

        # Level requirement
        required_level = quest.get("required_level", 1)
        if character.get("level", 1) < required_level:
            continue

        # Prerequisite requirement
        prereq_id = quest.get("prerequisite", "NONE")
        if prereq_id not in ("NONE", None, ""):
            if prereq_id not in character["completed_quests"]:
                continue

        available.append(quest)

    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed

    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    character.setdefault("completed_quests", [])
    return quest_id in character["completed_quests"]


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active

    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    character.setdefault("active_quests", [])
    return quest_id in character["active_quests"]


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest

    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]
    character.setdefault("active_quests", [])
    character.setdefault("completed_quests", [])

    # Level requirement
    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        return False

    # Already completed
    if quest_id in character["completed_quests"]:
        return False

    # Already active
    if quest_id in character["active_quests"]:
        return False

    # Prerequisite
    prereq_id = quest.get("prerequisite", "NONE")
    if prereq_id not in ("NONE", None, ""):
        if prereq_id not in character["completed_quests"]:
            return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest

    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]

    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    chain = []
    current_id = quest_id
    visited = set()

    while current_id is not None:
        if current_id in visited:
            # Prevent infinite loops if data is bad; break the chain
            break
        visited.add(current_id)

        if current_id not in quest_data_dict:
            # Invalid prerequisite link
            raise QuestNotFoundError(f"Prerequisite quest '{current_id}' not found.")

        chain.append(current_id)

        current_quest = quest_data_dict[current_id]
        prereq_id = current_quest.get("prerequisite", "NONE")

        if prereq_id in ("NONE", None, ""):
            break

        current_id = prereq_id

    # Currently chain is [quest, prereq, prereq_of_prereq, ...]
    # We need earliest -> quest
    chain.reverse()
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed

    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0

    character.setdefault("completed_quests", [])
    completed_quests = len(character["completed_quests"])

    percentage = (completed_quests / total_quests) * 100
    return float(percentage)


def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests

    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    character.setdefault("completed_quests", [])

    total_xp = 0
    total_gold = 0

    for quest_id in character["completed_quests"]:
        quest = quest_data_dict.get(quest_id)
        if quest is None:
            continue
        total_xp += quest.get("reward_xp", 0)
        total_gold += quest.get("reward_gold", 0)

    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range

    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    quests_in_range = []

    for quest in quest_data_dict.values():
        required_level = quest.get("required_level", 1)
        if min_level <= required_level <= max_level:
            quests_in_range.append(quest)

    return quests_in_range

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information

    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    reward_xp = quest_data.get("reward_xp", 0)
    reward_gold = quest_data.get("reward_gold", 0)
    required_level = quest_data.get("required_level", 1)
    prerequisite = quest_data.get("prerequisite", "NONE")

    print(f"Required Level: {required_level}")
    print(f"Rewards: {reward_xp} XP, {reward_gold} gold")
    if prerequisite in ("NONE", None, ""):
        print("Prerequisite: None")
    else:
        print(f"Prerequisite Quest ID: {prerequisite}")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format

    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("No quests to display.")
        return

    print("\n=== Quest List ===")
    for quest in quest_list:
        title = quest.get("title", "Unknown Quest")
        required_level = quest.get("required_level", 1)
        reward_xp = quest.get("reward_xp", 0)
        reward_gold = quest.get("reward_gold", 0)
        print(
            f"- {title} (Req. Level: {required_level}) | "
            f"Rewards: {reward_xp} XP, {reward_gold} gold"
        )


def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress

    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    character.setdefault("active_quests", [])
    character.setdefault("completed_quests", [])

    active_count = len(character["active_quests"])
    completed_count = len(character["completed_quests"])
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict)
    total_rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== Quest Progress ===")
    print(f"Active quests: {active_count}")
    print(f"Completed quests: {completed_count}")
    print(f"Completion: {completion_percentage:.1f}%")
    print(
        f"Total rewards earned: {total_rewards['total_xp']} XP, "
        f"{total_rewards['total_gold']} gold"
    )

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist

    Checks that every prerequisite (that's not "NONE") refers to a real quest

    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for quest_id, quest in quest_data_dict.items():
        prereq_id = quest.get("prerequisite", "NONE")
        if prereq_id not in ("NONE", None, ""):
            if prereq_id not in quest_data_dict:
                raise QuestNotFoundError(
                    f"Quest '{quest_id}' has invalid prerequisite '{prereq_id}'."
                )
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")

    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }


    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
 }

    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")
