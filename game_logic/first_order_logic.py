class FirstOrderLogic:
    def __init__(self):
        self.knowledge_base = {}
    
    def initialize_knowledge_base(self, puzzle):
        """Initialize the knowledge base with puzzle rules"""
        self.knowledge_base = {}
        
        if 'rules' not in puzzle:
            return
        
        for rule in puzzle['rules']:
            # Parse the premise and conclusion into logical statements
            premise = self._parse_statement(rule['premise'])
            conclusion = self._parse_statement(rule['conclusion'])
            
            # Add to knowledge base
            if premise and conclusion:
                key = self._get_predicate_key(premise['predicate'])
                
                if key not in self.knowledge_base:
                    self.knowledge_base[key] = []
                
                self.knowledge_base[key].append(conclusion)
    
    def _parse_statement(self, statement):
        """Parse a natural language statement into a logical statement"""
        # This is a simplified parser for demonstration
        # In a real implementation, you would use NLP techniques
        
        negation_patterns = ['not', 'never', 'cannot']
        negated = False
        
        for pattern in negation_patterns:
            if pattern in statement.lower():
                negated = True
                break
        
        # Extract the main subject and predicate
        # This is highly simplified
        parts = statement.split(' ')
        subject = next((p for p in parts if len(p) > 3), '')
        
        return {
            'predicate': {
                'name': statement.replace(',', '').strip(),
                'args': [subject]
            },
            'negated': negated
        }
    
    def _get_predicate_key(self, predicate):
        """Get a unique key for a predicate"""
        return f"{predicate['name']}({','.join(predicate['args'])})"
    
    def is_valid_statement(self, statement):
        """Check if a statement is valid according to the knowledge base"""
        parsed_statement = self._parse_statement(statement)
        if not parsed_statement:
            return False
        
        key = self._get_predicate_key(parsed_statement['predicate'])
        
        # Direct lookup in knowledge base
        if key in self.knowledge_base:
            statements = self.knowledge_base[key]
            
            # Check if the statement or its negation exists in the knowledge base
            for existing_statement in statements:
                if existing_statement['negated'] == parsed_statement['negated']:
                    return True
        
        # Inference through rules
        # This is a simplified inference mechanism
        for rule_key, conclusions in self.knowledge_base.items():
            if self._can_infer(parsed_statement, rule_key, conclusions):
                return True
        
        return False
    
    def _can_infer(self, statement, rule_key, conclusions):
        """Check if we can infer a statement from the knowledge base"""
        # Simple inference: if the rule key is related to the statement
        # and there's a matching conclusion, then the statement is valid
        statement_key = self._get_predicate_key(statement['predicate'])
        
        if rule_key in statement_key or statement_key in rule_key:
            for conclusion in conclusions:
                conclusion_key = self._get_predicate_key(conclusion['predicate'])
                
                if conclusion_key in statement_key or statement_key in conclusion_key:
                    return conclusion['negated'] == statement['negated']
        
        return False
    
    def evaluate_answer(self, puzzle, answer):
        """Evaluate a player's answer against the puzzle solution"""
        # Normalize the answer
        normalized_answer = answer.lower().strip()
        
        # Check against solution array
        return any(
            normalized_answer == sol.lower() or normalized_answer in sol.lower()
            for sol in puzzle.get('solution', [])
        )
    
    def generate_response(self, puzzle, query):
        """Generate a response based on the player's query"""
        # Initialize knowledge base if not already done
        if not self.knowledge_base and 'rules' in puzzle:
            self.initialize_knowledge_base(puzzle)
        
        # Check if the query is a question about the rules
        if 'can i' in query.lower() or 'is it' in query.lower() or 'does' in query.lower():
            is_valid = self.is_valid_statement(query)
            
            if is_valid:
                return "Yes, that seems correct based on the puzzle's rules."
            else:
                return "I'm not sure that follows from what we know about the puzzle."
        
        # Check if the query is an answer attempt
        if self.evaluate_answer(puzzle, query):
            return "That's correct! You've solved the puzzle."
        
        # Default response
        return "I'm here to help you solve the puzzle. You can ask me about the rules or try to answer."