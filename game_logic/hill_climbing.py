import random

class HillClimbing:
    def __init__(self, max_iterations=10, step_size=0.2, random_restart_probability=0.1):
        self.max_iterations = max_iterations
        self.step_size = step_size
        self.random_restart_probability = random_restart_probability
    
    def optimize_difficulty(self, current_difficulty, solve_time, attempts, hints_used):
        """Optimize puzzle difficulty based on player performance"""
        best_difficulty = current_difficulty
        best_score = self._evaluate_difficulty(current_difficulty, solve_time, attempts, hints_used)
        
        for i in range(self.max_iterations):
            # Random restart with some probability
            if random.random() < self.random_restart_probability:
                best_difficulty = random.random() * 3 + 1  # Random difficulty between 1 and 4
                best_score = self._evaluate_difficulty(best_difficulty, solve_time, attempts, hints_used)
                continue
            
            # Try increasing difficulty
            increased_difficulty = min(5, best_difficulty + self.step_size)
            increased_score = self._evaluate_difficulty(increased_difficulty, solve_time, attempts, hints_used)
            
            # Try decreasing difficulty
            decreased_difficulty = max(1, best_difficulty - self.step_size)
            decreased_score = self._evaluate_difficulty(decreased_difficulty, solve_time, attempts, hints_used)
            
            # Find the best move
            if increased_score > best_score and increased_score >= decreased_score:
                best_difficulty = increased_difficulty
                best_score = increased_score
            elif decreased_score > best_score:
                best_difficulty = decreased_difficulty
                best_score = decreased_score
            else:
                # We've reached a local optimum
                break
        
        return best_difficulty
    
    def _evaluate_difficulty(self, difficulty, solve_time, attempts, hints_used):
        """Evaluate how good a difficulty setting is based on player performance"""
        # Target values for an engaging experience
        target_attempts = 3
        target_hints = 1
        target_solve_time_per_difficulty = 60  # seconds per difficulty level
        
        # Calculate expected solve time based on difficulty
        expected_solve_time = difficulty * target_solve_time_per_difficulty
        
        # Calculate how close the actual values are to the targets
        attempts_score = 1 - abs(attempts - target_attempts) / 10
        hints_score = 1 - abs(hints_used - target_hints) / 5
        time_score = 1 - abs(solve_time - expected_solve_time) / expected_solve_time
        
        # Weight the scores (can be adjusted based on importance)
        return attempts_score * 0.4 + hints_score * 0.3 + time_score * 0.3
    
    def generate_optimized_puzzle(self, puzzles, current_difficulty, player_performance):
        """Generate a new puzzle with optimized difficulty"""
        # Optimize the difficulty based on player performance
        optimized_difficulty = self.optimize_difficulty(
            current_difficulty,
            player_performance['solve_time'],
            player_performance['attempts'],
            player_performance['hints_used']
        )
        
        # Find puzzles close to the optimized difficulty
        candidate_puzzles = [p for p in puzzles if abs(p['difficulty'] - optimized_difficulty) < 0.5 and not p.get('solved', False)]
        
        if candidate_puzzles:
            # Return a random puzzle from the candidates
            return candidate_puzzles[random.randint(0, len(candidate_puzzles) - 1)].copy()
        else:
            # If no suitable puzzles found, adjust an existing puzzle
            base_puzzle = puzzles[random.randint(0, len(puzzles) - 1)].copy()
            base_puzzle['difficulty'] = optimized_difficulty
            base_puzzle['solved'] = False
            base_puzzle['attempts'] = 0
            return base_puzzle