#!/usr/bin/env python3
"""
Split train.txt into train.txt (80%) and test.txt (20%) for evaluation
"""

import random

# Set random seed for reproducibility
random.seed(42)

# Read all sentences from train.txt
print("Reading train.txt...")
with open('train.txt', 'r', encoding='utf-8') as f:
    sentences = f.readlines()

print(f"Total sentences: {len(sentences)}")

# Shuffle sentences
random.shuffle(sentences)

# Split 80-20
split_idx = int(len(sentences) * 0.8)
train_sentences = sentences[:split_idx]
test_sentences = sentences[split_idx:]

print(f"Train sentences: {len(train_sentences)}")
print(f"Test sentences: {len(test_sentences)}")

# Save train.txt
print("\nWriting train.txt...")
with open('train.txt', 'w', encoding='utf-8') as f:
    f.writelines(train_sentences)

# Save test.txt
print("Writing test.txt...")
with open('test.txt', 'w', encoding='utf-8') as f:
    f.writelines(test_sentences)

print("\nData split complete!")
print(f"  - train.txt: {len(train_sentences)} sentences (80%)")
print(f"  - test.txt: {len(test_sentences)} sentences (20%)")
print(f"  - input.txt: unlabeled data for prediction")

