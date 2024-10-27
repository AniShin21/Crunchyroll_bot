# database.py

from accounts_store import user_data, used_accounts  # Import user_data from accounts_store

async def full_userbase():
    """Fetch all user IDs from the user_data."""
    return list(user_data.keys())

async def del_user(user_id):
    """Delete a user from user_data and used_accounts if exists."""
    if user_id in user_data:
        del user_data[user_id]  # Remove from user_data
    if user_id in used_accounts:
        used_accounts.remove(user_id)  # Remove from used_accounts if present



async def get_leaderboard():
    """Fetch the leaderboard data sorted by points."""
    # Create a sorted list of users based on their points
    leaderboard = sorted(user_data.items(), key=lambda x: x[1].get('points', 0), reverse=True)
    return leaderboard

async def add_points(user_id, points):
    """Add points to a user's score."""
    if user_id not in user_data:
        user_data[user_id] = {'points': 0}  # Initialize if not present
    user_data[user_id]['points'] += points  # Update points