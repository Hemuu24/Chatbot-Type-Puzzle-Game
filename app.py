

from flask import Flask, render_template, request, jsonify
from game_logic.depth_limited_search import DepthLimitedSearch
from game_logic.hill_climbing import HillClimbing
from game_logic.first_order_logic import FirstOrderLogic
from game_logic.puzzles import get_puzzles, get_puzzle_by_level



app = Flask(__name__)

# Initialize AI components
dls = DepthLimitedSearch(max_depth=3)
hill_climbing = HillClimbing()
fol = FirstOrderLogic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/puzzle/<int:level>')
def get_puzzle(level):
    puzzle = get_puzzle_by_level(level)
    if puzzle:
        # Don't send solution to frontend
        puzzle_data = puzzle.copy()
        if 'solution' in puzzle_data:
            del puzzle_data['solution']
        return jsonify(puzzle_data)
    return jsonify({'error': 'Puzzle not found'}), 404

@app.route('/api/puzzles/count')
def get_puzzle_count():
    puzzles = get_puzzles()
    return jsonify({'count': len(puzzles)})

@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.json
    level = data.get('level', 0)
    answer = data.get('answer', '').strip().lower()
    hints_used = data.get('hintsUsed', 0)
    
    puzzle = get_puzzle_by_level(level)
    if not puzzle:
        return jsonify({'error': 'Puzzle not found'}), 404
    
    # Increment attempts
    puzzle['attempts'] = puzzle.get('attempts', 0) + 1
    
    # Check if answer is correct using First-Order Logic
    is_correct = fol.evaluate_answer(puzzle, answer)
    
    if is_correct:
        # Calculate score based on attempts and hints
        base_score = 100
        attempt_penalty = puzzle['attempts'] * 5
        hint_penalty = hints_used * 10
        final_score = max(10, base_score - attempt_penalty - hint_penalty)
        
        # Mark puzzle as solved
        puzzle['solved'] = True
        
        # Use Hill Climbing to optimize difficulty for future puzzles
        # (This would be used in a more complex implementation)
        
        return jsonify({
            'correct': True,
            'score': final_score,
            'message': f"Congratulations! You've solved the puzzle and earned {final_score} points."
        })
    else:
        # Generate response using First-Order Logic
        response = fol.generate_response(puzzle, answer)
        return jsonify({
            'correct': False,
            'message': response
        })

@app.route('/api/hint', methods=['POST'])
def get_hint():
    data = request.json
    level = data.get('level', 0)
    hints_used = data.get('hintsUsed', 0)
    
    puzzle = get_puzzle_by_level(level)
    if not puzzle:
        return jsonify({'error': 'Puzzle not found'}), 404
    
    # Use Depth-Limited Search to get the next hint
    hint = dls.get_next_hint(puzzle, hints_used)
    
    if hint:
        return jsonify({
            'hint': hint
        })
    elif dls.has_reached_depth_limit(hints_used):
        return jsonify({
            'message': "I've given you all the hints I can for now. Try to solve the puzzle with what you know."
        })
    else:
        return jsonify({
            'message': "I don't have any more hints for this puzzle. Trust your instincts!"
        })

if __name__ == '__main__':
    app.run(debug=True)