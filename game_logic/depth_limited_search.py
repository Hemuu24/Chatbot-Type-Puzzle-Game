class DepthLimitedSearch:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.hint_tree = None
    
    def build_hint_tree(self, puzzle):
        """Build a hint tree based on the puzzle"""
        self.hint_tree = {
            'hint_index': -1,  # Root node
            'depth': 0,
            'relevance': 1.0,
            'children': []
        }
        
        # For each hint, create a node in the tree
        for i, hint in enumerate(puzzle.get('hints', [])):
            # Calculate relevance based on hint position (earlier hints are more general)
            relevance = 1.0 - (i / len(puzzle.get('hints', []))) * 0.5
            
            self.hint_tree['children'].append({
                'hint_index': i,
                'depth': 1,
                'relevance': relevance,
                'children': []
            })
    
    def get_next_hint(self, puzzle, hints_used):
        """Get the next best hint within the depth limit"""
        if not self.hint_tree:
            self.build_hint_tree(puzzle)
        
        if not self.hint_tree or hints_used >= self.max_depth:
            return None  # No more hints available within depth limit
        
        # Find the most relevant hint that hasn't been used yet
        available_hints = self._find_available_hints(self.hint_tree, hints_used)
        if not available_hints:
            return None
        
        # Sort by relevance and return the most relevant hint
        available_hints.sort(key=lambda x: x['relevance'], reverse=True)
        return puzzle.get('hints', [])[available_hints[0]['hint_index']]
    
    def _find_available_hints(self, node, hints_used):
        """Find all available hints within the depth limit"""
        hints = []
        
        if node['depth'] > 0 and node['hint_index'] < hints_used:
            # This hint has already been used
            return hints
        
        if node['depth'] > 0 and node['depth'] <= self.max_depth:
            hints.append(node)
        
        for child in node.get('children', []):
            hints.extend(self._find_available_hints(child, hints_used))
        
        return hints
    
    def has_reached_depth_limit(self, hints_used):
        """Check if we've reached the maximum depth of hints"""
        return hints_used >= self.max_depth