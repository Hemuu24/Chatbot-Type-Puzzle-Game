# Initial puzzles data
_puzzles = [
    {
        'id': 'puzzle-1',
        'type': 'riddle',
        'title': "The Guardian's Riddle",
        'description': "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        'hints': [
            "I am not alive, but I can make sounds.",
            "You might find me in mountains or valleys.",
            "I can be loud or soft, depending on the wind."
        ],
        'solution': ['echo', 'an echo', 'the echo'],
        'difficulty': 1,
        'attempts': 0,
        'solved': False
    },
    {
        'id': 'puzzle-2',
        'type': 'logic',
        'title': "The Alchemist's Challenge",
        'description': "Three potions sit before you: red, blue, and green. One grants wisdom, one grants strength, and one is poison. The wise potion is not red. The poison is not green. If the blue potion grants strength, which potion grants wisdom?",
        'hints': [
            "Start by listing all possible combinations.",
            "If blue grants strength, what must red be?",
            "Process of elimination will lead you to the answer."
        ],
        'solution': ['green', 'the green potion', 'green potion'],
        'difficulty': 2,
        'attempts': 0,
        'solved': False,
        'rules': [
            {'id': 'rule-1', 'premise': 'The wise potion is not red', 'conclusion': 'The wise potion is either blue or green'},
            {'id': 'rule-2', 'premise': 'The poison is not green', 'conclusion': 'The poison is either red or blue'},
            {'id': 'rule-3', 'premise': 'The blue potion grants strength', 'conclusion': 'The blue potion is neither poison nor wisdom'}
        ]
    },
    {
        'id': 'puzzle-3',
        'type': 'pattern',
        'title': 'The Sequence of Symbols',
        'description': 'What comes next in this sequence? ◯, △, □, ◯, △, ?',
        'hints': [
            "Look for a repeating pattern.",
            "Count how many symbols appear before the pattern repeats.",
            "The pattern has 3 symbols that repeat."
        ],
        'solution': ['square', 'a square', 'the square', '□'],
        'difficulty': 1,
        'attempts': 0,
        'solved': False
    },
    {
        'id': 'puzzle-4',
        'type': 'riddle',
        'title': 'The Timeless Enigma',
        'description': 'I am taken from a mine, and shut in a wooden case, from which I am never released, yet I am used by almost every person. What am I?',
        'hints': [
            "You might use me to write something down.",
            "I leave marks when used properly.",
            "I am made of a mineral substance."
        ],
        'solution': ['pencil lead', 'lead', 'graphite', 'pencil'],
        'difficulty': 2,
        'attempts': 0,
        'solved': False
    },
    {
        'id': 'puzzle-5',
        'type': 'logic',
        'title': 'The Enchanted Doors',
        'description': 'Before you stand three doors. One leads to freedom, one to an endless maze, and one to a dragon. A guardian at each door will answer one question, but one always lies, one always tells the truth, and one answers randomly. What single question can you ask one guardian to determine which door leads to freedom?',
        'hints': [
            "You need a question that works regardless of which guardian you ask.",
            "Consider what would happen if you asked about what another guardian would say.",
            "Nested questions can reveal the truth even from liars."
        ],
        'solution': [
            'what door would another guardian say leads to freedom',
            'which door would the other guardian say leads to freedom'
        ],
        'difficulty': 3,
        'attempts': 0,
        'solved': False,
        'rules': [
            {'id': 'rule-1', 'premise': 'One guardian always lies', 'conclusion': "This guardian's statements are always false"},
            {'id': 'rule-2', 'premise': 'One guardian always tells the truth', 'conclusion': "This guardian's statements are always true"},
            {'id': 'rule-3', 'premise': 'One guardian answers randomly', 'conclusion': "This guardian's statements have no pattern"}
        ]
    }
]

def get_puzzles():
    """Get all puzzles"""
    return _puzzles

def get_puzzle_by_level(level):
    """Get a puzzle by level"""
    if 0 <= level < len(_puzzles):
        return _puzzles[level]
    return None