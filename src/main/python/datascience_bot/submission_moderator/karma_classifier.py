# -*- coding: utf-8 -*-
"""Classify a user as a new user or troll by their karma
"""

def classify_karma(total_karma: int) -> str:
    """Classify a user by their total karma as one of
        - Troll
        - New User

    Args:
        total_karma (int): Total Reddit karma

    Returns:
        str: classification text label
    """
    if not isinstance(total_karma, int):
        raise TypeError(f"total_karma must be an int, not {type(total_karma)}")
    if total_karma <= -10:
        return "troll"
    if total_karma < 50:
        return "new user"
    return None
