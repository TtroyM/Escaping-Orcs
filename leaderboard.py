import json
import os

LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return []  # Returns an empty list if no LEADERBOARD_FILE exists

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=4)

def update_leaderboard(name, time):
    leaderboard = load_leaderboard()

    # Check if the new score is good enough to be on the leaderboard
    if len(leaderboard) < 5 or time > leaderboard[-1]['time']:
        leaderboard.append({'name': name, 'time': time})
        leaderboard = sorted(leaderboard, key=lambda x: x['time'], reverse=True)

        # Trim the list to the top 5 scores
        if len(leaderboard) > 5:
            leaderboard.pop()
    else:
        # If the score isn't good enough, no need to update
        return leaderboard

    save_leaderboard(leaderboard)
    return leaderboard


def is_top_score(time):
    leaderboard = load_leaderboard()
    if len(leaderboard) < 5:
        return True
    # Check if the current time is higher than the lowest top score
    return time > leaderboard[-1]['time']
