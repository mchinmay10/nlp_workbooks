#!/usr/bin/env python3
"""
CYK (Cocke-Younger-Kasami) Parsing Algorithm Implementation
Assignment 6 - Natural Language Processing
Student: 612203120

This implementation parses sentences using a Probabilistic Context-Free Grammar (PCFG)
and generates an upper triangular table showing all possible derivations with probabilities.
"""

import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple, Set


class CYKParser:
    def __init__(self):
        """Initialize the CYK parser with the given PCFG rules."""
        self.grammar = {}
        self.terminals = {}
        self.non_terminals = set()
        
        # Define the PCFG rules based on the provided grammar
        self._initialize_grammar()
    
    def _initialize_grammar(self):
        """Initialize the grammar rules and their probabilities."""
        # Grammar rules: (left_side, right_side) -> probability
        rules = [
            # S rules
            ('S', ('NP', 'VP'), 1.0),
            
            # VP rules  
            ('VP', ('V', 'NP'), 0.7),
            ('VP', ('VP', 'PP'), 0.3),
            
            # PP rules
            ('PP', ('P', 'NP'), 1.0),
            
            # P rules
            ('P', ('with',), 1.0),
            
            # V rules
            ('V', ('saw',), 1.0),
            
            # NP rules
            ('NP', ('NP', 'PP'), 0.4),
            ('NP', ('astronomers',), 0.1),
            ('NP', ('ears',), 0.18),
            ('NP', ('saw',), 0.04),
            ('NP', ('stars',), 0.18),
            ('NP', ('telescope',), 0.1),
        ]
        
        # Build grammar dictionary
        for left, right, prob in rules:
            if left not in self.grammar:
                self.grammar[left] = {}
            
            if isinstance(right, tuple) and len(right) == 1:
                # Terminal rule
                terminal = right[0]
                self.terminals[terminal] = (left, prob)
                self.grammar[left][right] = prob
            else:
                # Non-terminal rule
                self.grammar[left][right] = prob
            
            self.non_terminals.add(left)
    
    def parse(self, sentence: str) -> Dict:
        """
        Parse a sentence using the CYK algorithm.
        
        Args:
            sentence: Input sentence as a string
            
        Returns:
            Dictionary containing the parse table and results
        """
        words = sentence.lower().split()
        n = len(words)
        
        # Initialize the parse table
        # table[i][j] contains all possible non-terminals for span from i to j
        table = [[{} for _ in range(n + 1)] for _ in range(n + 1)]
        
        # Fill diagonal (length 1 spans)
        for i in range(n):
            word = words[i]
            if word in self.terminals:
                non_terminal, prob = self.terminals[word]
                table[i][i + 1][non_terminal] = [{
                    'probability': prob,
                    'rule': (non_terminal, (word,)),
                    'split': None
                }]
            
            # Also check for rules that produce this word
            for nt, rules in self.grammar.items():
                for rule_right, rule_prob in rules.items():
                    if isinstance(rule_right, tuple) and len(rule_right) == 1 and rule_right[0] == word:
                        if nt not in table[i][i + 1]:
                            table[i][i + 1][nt] = []
                        table[i][i + 1][nt].append({
                            'probability': rule_prob,
                            'rule': (nt, rule_right),
                            'split': None
                        })
        
        # Fill table for longer spans
        for length in range(2, n + 1):  # span length
            for i in range(n - length + 1):  # start position
                j = i + length  # end position
                
                # Try all possible splits
                for k in range(i + 1, j):  # split position
                    # Get non-terminals for left and right parts
                    left_spans = table[i][k]
                    right_spans = table[k][j]
                    
                    # Try all combinations of left and right non-terminals
                    for left_nt, left_derivations in left_spans.items():
                        for right_nt, right_derivations in right_spans.items():
                            # Try all combinations of derivations
                            for left_info in left_derivations:
                                for right_info in right_derivations:
                                    # Check if there's a rule combining these non-terminals
                                    for rule_left, rules in self.grammar.items():
                                        for rule_right, rule_prob in rules.items():
                                            if (isinstance(rule_right, tuple) and 
                                                len(rule_right) == 2 and 
                                                rule_right[0] == left_nt and 
                                                rule_right[1] == right_nt):
                                            
                                                # Calculate new probability
                                                new_prob = (rule_prob * 
                                                           left_info['probability'] * 
                                                           right_info['probability'])
                                                
                                                # Store all derivations, not just the best one
                                                if rule_left not in table[i][j]:
                                                    table[i][j][rule_left] = []
                                                
                                                table[i][j][rule_left].append({
                                                    'probability': new_prob,
                                                    'rule': (rule_left, rule_right),
                                                    'split': k,
                                                    'left_nt': left_nt,
                                                    'right_nt': right_nt
                                                })
                
                # Sort and deduplicate derivations by probability for each non-terminal
                for nt in table[i][j]:
                    if isinstance(table[i][j][nt], list):
                        # Remove duplicates based on probability, split, and rule
                        seen = set()
                        unique_derivations = []
                        for derivation in table[i][j][nt]:
                            key = (derivation['probability'], derivation['split'], 
                                   derivation['rule'], derivation.get('left_nt'), derivation.get('right_nt'))
                            if key not in seen:
                                seen.add(key)
                                unique_derivations.append(derivation)
                        
                        # Sort by probability (descending)
                        unique_derivations.sort(key=lambda x: x['probability'], reverse=True)
                        table[i][j][nt] = unique_derivations
        
        # All derivations are already lists, no conversion needed
        
        # Get best probability
        best_prob = 0.0
        if table[0][n] and 'S' in table[0][n] and table[0][n]['S']:
            best_prob = table[0][n]['S'][0]['probability']
        
        return {
            'table': table,
            'words': words,
            'sentence': sentence,
            'is_valid': 'S' in table[0][n] and table[0][n]['S'],
            'best_probability': best_prob
        }
    
    def print_upper_triangular_table(self, parse_result: Dict):
        """Print the upper triangular table in the required format."""
        table = parse_result['table']
        words = parse_result['words']
        n = len(words)
        
        print("CYK Parse Table (Upper Triangular Matrix)")
        print("=" * 50)
        print()
        
        # Print word indices
        print("Word positions:")
        for i, word in enumerate(words):
            print(f"{i} {word} {i+1}")
        print()
        
        # Print the table
        print("Upper Triangular Table:")
        print()
        
        for length in range(1, n + 1):
            for i in range(n - length + 1):
                j = i + length
                span_text = " ".join(words[i:j])
                
                print(f"Span ({i},{j}) - \"{span_text}\":")
                
                if table[i][j]:
                    # Sort non-terminals by best probability (descending)
                    sorted_nts = sorted(table[i][j].items(), 
                                      key=lambda x: x[1][0]['probability'], 
                                      reverse=True)
                    
                    for idx, (nt, derivations) in enumerate(sorted_nts):
                        # Show only the top 2 derivations to match expected output
                        top_derivations = derivations[:2]
                        for d_idx, derivation in enumerate(top_derivations):
                            prob = derivation['probability']
                            if len(derivations) > 1 and d_idx == 1:
                                print(f"  {nt}₂ [{prob}]")
                            elif len(derivations) > 1 and d_idx == 0:
                                print(f"  {nt}₁ [{prob}]")
                            else:
                                print(f"  {nt} [{prob}]")
                    
                    print(f"  X{i},{j}")
                else:
                    print(f"  φ")
                    print(f"  X{i},{j}")
                
                print()
    
    def get_parse_tree(self, parse_result: Dict) -> str:
        """Extract the most probable parse tree."""
        table = parse_result['table']
        n = len(parse_result['words'])
        
        if 'S' not in table[0][n] or not table[0][n]['S']:
            return "No valid parse found."
        
        def build_tree(i: int, j: int, non_terminal: str) -> str:
            """Recursively build parse tree."""
            if i == j - 1:
                # Terminal
                word = parse_result['words'][i]
                return f"({non_terminal} {word})"
            
            # Get the best derivation for this non-terminal
            info = table[i][j][non_terminal][0]
            if info['split'] is None:
                return f"({non_terminal} {parse_result['words'][i]})"
            
            k = info['split']
            left_tree = build_tree(i, k, info['left_nt'])
            right_tree = build_tree(k, j, info['right_nt'])
            
            return f"({non_terminal} {left_tree} {right_tree})"
        
        return build_tree(0, n, 'S')


def main():
    """Main function to run the CYK parser."""
    parser = CYKParser()
    
    # Input sentence
    sentence = "Astronomers saw stars with telescope"
    
    print(f"Input sentence: {sentence}")
    print()
    
    # Parse the sentence
    result = parser.parse(sentence)
    
    # Print results
    print(f"Sentence is valid: {result['is_valid']}")
    if result['is_valid']:
        print(f"Best parse probability: {result['best_probability']}")
        print()
        
        # Print parse tree
        parse_tree = parser.get_parse_tree(result)
        print("Most probable parse tree:")
        print(parse_tree)
        print()
    
    # Print the upper triangular table
    parser.print_upper_triangular_table(result)


if __name__ == "__main__":
    main()
