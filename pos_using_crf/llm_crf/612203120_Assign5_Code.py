#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
POS Tagging using Conditional Random Fields (CRF)
Assignment 5 - Natural Language Processing

This module implements a CRF-based POS tagger with comprehensive feature engineering
and feature ablation analysis.
"""

import re
import pycrfsuite
from collections import Counter
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np


class CRFPOSTagger:
    """CRF-based Part-of-Speech Tagger with feature engineering"""
    
    def __init__(self):
        self.trainer = pycrfsuite.Trainer(verbose=False)
        self.tagger = None
        self.feature_config = {
            'word_features': True,
            'context_features': True,
            'orthographic_features': True,
            'suffix_prefix_features': True,
            'word_shape_features': True,
        }
    
    def word2features(self, sent, i, feature_config=None):
        """
        Extract features for a word at position i in sentence.
        
        Features include:
        - Word-level: current word, lowercase, is_first, is_last
        - Context: previous and next words
        - Orthographic: capitalization, digits, punctuation
        - Morphological: prefixes, suffixes
        - Word shape: pattern of caps, digits, lowercase
        """
        if feature_config is None:
            feature_config = self.feature_config
            
        word = sent[i][0]
        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'word[-3:]': word[-3:],
            'word[-2:]': word[-2:],
            'word.isupper()': word.isupper(),
            'word.istitle()': word.istitle(),
            'word.isdigit()': word.isdigit(),
        }
        
        # Word-level features
        if feature_config.get('word_features', True):
            features.update({
                'word.lower()': word.lower(),
                'word.length': len(word),
                'word.is_first': i == 0,
                'word.is_last': i == len(sent) - 1,
            })
        
        # Orthographic features
        if feature_config.get('orthographic_features', True):
            features.update({
                'word.isupper()': word.isupper(),
                'word.istitle()': word.istitle(),
                'word.isdigit()': word.isdigit(),
                'word.isalpha()': word.isalpha(),
                'word.isalnum()': word.isalnum(),
                'has.digit': bool(re.search(r'\d', word)),
                'has.hyphen': '-' in word,
                'has.punctuation': bool(re.search(r'[^\w\s]', word)),
            })
        
        # Suffix and prefix features
        if feature_config.get('suffix_prefix_features', True):
            features.update({
                'word.prefix-1': word[0] if len(word) > 0 else '',
                'word.prefix-2': word[:2] if len(word) > 1 else '',
                'word.prefix-3': word[:3] if len(word) > 2 else '',
                'word.suffix-1': word[-1] if len(word) > 0 else '',
                'word.suffix-2': word[-2:] if len(word) > 1 else '',
                'word.suffix-3': word[-3:] if len(word) > 2 else '',
                'word.suffix-4': word[-4:] if len(word) > 3 else '',
            })
        
        # Word shape features
        if feature_config.get('word_shape_features', True):
            shape = self.get_word_shape(word)
            features.update({
                'word.shape': shape,
                'word.short_shape': self.get_short_shape(shape),
            })
        
        # Context features - previous word
        if i > 0 and feature_config.get('context_features', True):
            word1 = sent[i-1][0]
            features.update({
                '-1:word.lower()': word1.lower(),
                '-1:word.istitle()': word1.istitle(),
                '-1:word.isupper()': word1.isupper(),
                '-1:word.suffix-2': word1[-2:] if len(word1) > 1 else '',
                '-1:word.suffix-3': word1[-3:] if len(word1) > 2 else '',
            })
        else:
            features['BOS'] = True  # Beginning of sentence
        
        # Context features - next word
        if i < len(sent) - 1 and feature_config.get('context_features', True):
            word1 = sent[i+1][0]
            features.update({
                '+1:word.lower()': word1.lower(),
                '+1:word.istitle()': word1.istitle(),
                '+1:word.isupper()': word1.isupper(),
                '+1:word.suffix-2': word1[-2:] if len(word1) > 1 else '',
                '+1:word.suffix-3': word1[-3:] if len(word1) > 2 else '',
            })
        else:
            features['EOS'] = True  # End of sentence
        
        # Bi-gram context features
        if i > 0 and i < len(sent) - 1 and feature_config.get('context_features', True):
            features.update({
                'word[-1,0]': sent[i-1][0].lower() + '_' + word.lower(),
                'word[0,+1]': word.lower() + '_' + sent[i+1][0].lower(),
            })
        
        return features
    
    def get_word_shape(self, word):
        """
        Get word shape (e.g., 'Xxxxx' -> 'Aa', '123' -> 'd', 'HELLO' -> 'A')
        """
        shape = []
        for char in word:
            if char.isupper():
                shape.append('X')
            elif char.islower():
                shape.append('x')
            elif char.isdigit():
                shape.append('d')
            else:
                shape.append(char)
        return ''.join(shape)
    
    def get_short_shape(self, shape):
        """
        Compress word shape by removing consecutive duplicates
        """
        if not shape:
            return shape
        short = [shape[0]]
        for char in shape[1:]:
            if char != short[-1]:
                short.append(char)
        return ''.join(short)
    
    def sent2features(self, sent, feature_config=None):
        """Extract features for all words in a sentence"""
        return [self.word2features(sent, i, feature_config) for i in range(len(sent))]
    
    def sent2labels(self, sent):
        """Extract labels for all words in a sentence"""
        return [label for token, label in sent]
    
    def sent2tokens(self, sent):
        """Extract tokens from a sentence"""
        return [token for token, label in sent]
    
    def load_data(self, filename):
        """
        Load data from file.
        Format: word_TAG word_TAG ...
        """
        sentences = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                tokens = line.split()
                sentence = []
                for token in tokens:
                    if '_' in token:
                        # Split only on the last underscore to handle words with underscores
                        parts = token.rsplit('_', 1)
                        if len(parts) == 2:
                            word, tag = parts
                            sentence.append((word, tag))
                
                if sentence:
                    sentences.append(sentence)
        
        return sentences
    
    def load_test_data(self, filename):
        """
        Load test data from file (may be raw text or tagged text)
        """
        # Valid Penn Treebank POS tags
        valid_pos_tags = {
            'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
            'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR',
            'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
            'WDT', 'WP', 'WP$', 'WRB', '.', ',', ':', '(', ')', '``', "''", '#',
            '$', '-LRB-', '-RRB-', '-NONE-', '_', '_.', '_,', '_``', "_''"
        }
        
        sentences = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this looks like tagged data (has word_TAG format with valid POS tags)
                tokens = line.split()
                sentence = []
                
                # Check if most tokens have the word_TAG format with valid POS tags
                valid_tagged_count = 0
                for token in tokens:
                    if '_' in token:
                        parts = token.rsplit('_', 1)
                        if len(parts) == 2 and parts[1] in valid_pos_tags:
                            valid_tagged_count += 1
                
                is_tagged = valid_tagged_count > len(tokens) * 0.5  # If more than 50% have valid tags
                
                if is_tagged:
                    # Parse as tagged data
                    for token in tokens:
                        if '_' in token:
                            parts = token.rsplit('_', 1)
                            if len(parts) == 2 and parts[1] in valid_pos_tags:
                                word, tag = parts
                                sentence.append((word, tag))
                            else:
                                sentence.append((token, None))
                        else:
                            sentence.append((token, None))
                else:
                    # Parse as raw unlabeled text - tokenize by whitespace and punctuation
                    import re
                    # Simple tokenization: split on whitespace and separate punctuation
                    text = line
                    # Add spaces around punctuation for better tokenization
                    text = re.sub(r'([.,;:!?()"\'])', r' \1 ', text)
                    words = text.split()
                    sentence = [(word, None) for word in words if word.strip()]
                
                if sentence:
                    sentences.append(sentence)
        
        return sentences
    
    def train(self, train_sentences, feature_config=None, params=None):
        """
        Train CRF model
        """
        if params is None:
            params = {
                'c1': 0.1,  # L1 regularization coefficient
                'c2': 0.1,  # L2 regularization coefficient
                'max_iterations': 100,
                'feature.possible_transitions': True
            }
        
        # Set feature configuration
        if feature_config:
            self.feature_config = feature_config
        
        # Extract features and labels
        for sent in train_sentences:
            features = self.sent2features(sent, self.feature_config)
            labels = self.sent2labels(sent)
            self.trainer.append(features, labels)
        
        # Set training parameters
        self.trainer.set_params(params)
        
        # Train the model
        self.trainer.train('crf_model.crfsuite')
        
        # Load the trained model
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open('crf_model.crfsuite')
    
    def predict(self, sentences):
        """
        Predict POS tags for sentences
        """
        predictions = []
        for sent in sentences:
            features = self.sent2features(sent, self.feature_config)
            pred = self.tagger.tag(features)
            predictions.append(pred)
        
        return predictions
    
    def evaluate(self, test_sentences):
        """
        Evaluate model performance (only works with labeled data)
        """
        true_labels = []
        pred_labels = []
        
        for sent in test_sentences:
            features = self.sent2features(sent, self.feature_config)
            true = self.sent2labels(sent)
            pred = self.tagger.tag(features)
            
            # Filter out None labels (unlabeled data)
            for t, p in zip(true, pred):
                if t is not None:
                    true_labels.append(t)
                    pred_labels.append(p)
        
        # Check if we have any labeled data
        if len(true_labels) == 0:
            return None, None, [], []
        
        # Calculate accuracy
        accuracy = sum([1 if t == p else 0 for t, p in zip(true_labels, pred_labels)]) / len(true_labels)
        
        # Get unique labels
        labels = sorted(set(true_labels + pred_labels))
        
        # Classification report
        report = classification_report(true_labels, pred_labels, labels=labels, zero_division=0)
        
        return accuracy, report, true_labels, pred_labels
    
    def save_predictions(self, sentences, predictions, output_file):
        """
        Save predictions to file in the same format as input
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            for sent, pred in zip(sentences, predictions):
                tokens = [token for token, _ in sent]
                tagged = ['_'.join([token, tag]) for token, tag in zip(tokens, pred)]
                f.write(' '.join(tagged) + '\n')


def feature_ablation_study(train_file, test_file):
    """
    Perform feature ablation study to identify most useful features
    """
    print("=" * 80)
    print("FEATURE ABLATION STUDY")
    print("=" * 80)
    
    # Load data
    tagger = CRFPOSTagger()
    train_sentences = tagger.load_data(train_file)
    test_sentences = tagger.load_data(test_file)
    
    # Use smaller subset for faster ablation study
    train_subset = train_sentences[:5000] if len(train_sentences) > 5000 else train_sentences
    test_subset = test_sentences[:1000] if len(test_sentences) > 1000 else test_sentences
    
    print(f"\nUsing {len(train_subset)} training sentences and {len(test_subset)} test sentences")
    print(f"for feature ablation study\n")
    
    # Define feature configurations to test
    feature_configs = [
        {
            'name': 'All Features',
            'config': {
                'word_features': True,
                'context_features': True,
                'orthographic_features': True,
                'suffix_prefix_features': True,
                'word_shape_features': True,
            }
        },
        {
            'name': 'Without Word Features',
            'config': {
                'word_features': False,
                'context_features': True,
                'orthographic_features': True,
                'suffix_prefix_features': True,
                'word_shape_features': True,
            }
        },
        {
            'name': 'Without Context Features',
            'config': {
                'word_features': True,
                'context_features': False,
                'orthographic_features': True,
                'suffix_prefix_features': True,
                'word_shape_features': True,
            }
        },
        {
            'name': 'Without Orthographic Features',
            'config': {
                'word_features': True,
                'context_features': True,
                'orthographic_features': False,
                'suffix_prefix_features': True,
                'word_shape_features': True,
            }
        },
        {
            'name': 'Without Suffix/Prefix Features',
            'config': {
                'word_features': True,
                'context_features': True,
                'orthographic_features': True,
                'suffix_prefix_features': False,
                'word_shape_features': True,
            }
        },
        {
            'name': 'Without Word Shape Features',
            'config': {
                'word_features': True,
                'context_features': True,
                'orthographic_features': True,
                'suffix_prefix_features': True,
                'word_shape_features': False,
            }
        },
        {
            'name': 'Only Word Features',
            'config': {
                'word_features': True,
                'context_features': False,
                'orthographic_features': False,
                'suffix_prefix_features': False,
                'word_shape_features': False,
            }
        },
        {
            'name': 'Only Context Features',
            'config': {
                'word_features': False,
                'context_features': True,
                'orthographic_features': False,
                'suffix_prefix_features': False,
                'word_shape_features': False,
            }
        },
    ]
    
    results = []
    
    for fc in feature_configs:
        print(f"\nTesting: {fc['name']}")
        print("-" * 40)
        
        # Create new tagger
        tagger = CRFPOSTagger()
        
        # Train with specific feature configuration
        tagger.train(train_subset, feature_config=fc['config'])
        
        # Evaluate
        accuracy, report, _, _ = tagger.evaluate(test_subset)
        
        results.append({
            'name': fc['name'],
            'accuracy': accuracy,
            'config': fc['config']
        })
        
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Print summary
    print("\n" + "=" * 80)
    print("FEATURE ABLATION SUMMARY")
    print("=" * 80)
    print(f"\n{'Feature Configuration':<40} {'Accuracy':<15} {'Degradation':<15}")
    print("-" * 70)
    
    # Sort by accuracy
    results_sorted = sorted(results, key=lambda x: x['accuracy'], reverse=True)
    baseline_acc = results_sorted[0]['accuracy']
    
    for r in results_sorted:
        degradation = baseline_acc - r['accuracy']
        print(f"{r['name']:<40} {r['accuracy']*100:>6.2f}% {degradation*100:>14.2f}%")
    
    return results


def main():
    """
    Main function to train and evaluate CRF POS tagger
    """
    train_file = 'train.txt'
    test_file = 'test.txt'
    input_file = 'input.txt'
    output_file = '612203120_Assign5_Output.txt'
    input_copy_file = '612203120_Assign5_Input.txt'
    
    print("=" * 80)
    print("CRF-BASED POS TAGGER")
    print("=" * 80)
    
    # Initialize tagger
    tagger = CRFPOSTagger()
    
    # Load training data
    print(f"\nLoading training data from {train_file}...")
    train_sentences = tagger.load_data(train_file)
    print(f"Loaded {len(train_sentences)} training sentences")
    
    # Load test data (for evaluation)
    print(f"\nLoading test data from {test_file}...")
    test_sentences = tagger.load_data(test_file)  # Use load_data for labeled test data
    print(f"Loaded {len(test_sentences)} test sentences")
    
    # Train model with all features
    print("\nTraining CRF model with all features...")
    tagger.train(train_sentences)
    print("Training complete!")
    
    # Evaluate on test data
    print("\n" + "=" * 80)
    print("EVALUATION ON TEST DATA")
    print("=" * 80)
    accuracy, report, true_labels, pred_labels = tagger.evaluate(test_sentences)
    
    if accuracy is not None:
        print(f"\nOverall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print("\nDetailed Classification Report:")
        print(report)
        
        # Show some example predictions
        print("\nSample Predictions on Test Data:")
        print("-" * 80)
        for i in range(min(5, len(test_sentences))):
            tokens = [token for token, _ in test_sentences[i]]
            true = [label for _, label in test_sentences[i]]
            test_pred = tagger.predict([test_sentences[i]])[0]
            
            print(f"\nSentence {i+1}:")
            print("Tokens:", ' '.join(tokens[:15]) + ('...' if len(tokens) > 15 else ''))
            print("True:  ", ' '.join(true[:15]) + ('...' if len(true) > 15 else ''))
            print("Pred:  ", ' '.join(test_pred[:15]) + ('...' if len(test_pred) > 15 else ''))
    
    # Predict on unlabeled input data
    import os
    if os.path.exists(input_file):
        print("\n" + "=" * 80)
        print("PREDICTION ON UNLABELED INPUT DATA")
        print("=" * 80)
        
        print(f"\nLoading unlabeled input data from {input_file}...")
        input_sentences = tagger.load_test_data(input_file)
        print(f"Loaded {len(input_sentences)} input sentences")
        
        # Make predictions
        print("\nMaking predictions on input data...")
        input_predictions = tagger.predict(input_sentences)
        
        # Save predictions
        print(f"\nSaving predictions to {output_file}...")
        tagger.save_predictions(input_sentences, input_predictions, output_file)
        
        # Copy input
        print(f"Copying input to {input_copy_file}...")
        import shutil
        shutil.copy(input_file, input_copy_file)
        
        # Show sample predictions
        print("\nSample Predictions on Input Data:")
        print("-" * 80)
        for i in range(min(3, len(input_sentences))):
            tokens = [token for token, _ in input_sentences[i]]
            pred = input_predictions[i]
            
            print(f"\nSentence {i+1}:")
            print("Tokens:", ' '.join(tokens[:15]) + ('...' if len(tokens) > 15 else ''))
            print("Pred:  ", ' '.join(pred[:15]) + ('...' if len(pred) > 15 else ''))
    
    print("\n" + "=" * 80)
    print("MAIN TRAINING AND EVALUATION COMPLETE")
    print("=" * 80)
    
    # Perform feature ablation study
    if accuracy is not None:
        print("\n")
        ablation_results = feature_ablation_study(train_file, test_file)
    else:
        print("\nSkipping feature ablation study (requires labeled test data)")
        ablation_results = None
    
    print("\n" + "=" * 80)
    print("ALL TASKS COMPLETE")
    print("=" * 80)
    print(f"\nGenerated files:")
    print(f"  - {output_file}: POS tagged output (from input.txt)")
    print(f"  - {input_copy_file}: Copy of input.txt")
    print(f"  - crf_model.crfsuite: Trained CRF model")
    if accuracy is not None:
        print(f"\nModel Performance on Test Set:")
        print(f"  - Accuracy: {accuracy*100:.2f}%")
    
    return ablation_results


if __name__ == '__main__':
    results = main()

