import sys
import re
from collections import Counter
import nltk
from nltk.util import ngrams


def generate_ngram_model(input_file_path, mis_no):
    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
        return

    # Normalize and tokenize the text into sentences and then words
    # Using a simple regex to split into sentences
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    all_tokens = [
        word.lower() for sentence in sentences for word in nltk.word_tokenize(sentence)
    ]

    # Define the range of n-grams you want to create
    n_values = {"bigram": 2, "trigram": 3, "four-gram": 4, "five-gram": 5}

    for name, n in n_values.items():
        print(f"Generating {name} model...")

        # Generate n-grams
        n_grams = ngrams(all_tokens, n)

        # Count the frequency of each n-gram
        ngram_counts = Counter(n_grams)

        # Prepare the output lines
        output_lines = []
        for ngram, count in ngram_counts.items():
            # Format: "word1 word2... count"
            output_lines.append(f"{' '.join(ngram)} {count}")

        # Write to the output file
        output_file_name = f"{mis_no}_{name}-output.txt"
        try:
            with open(output_file_name, "w", encoding="utf-8") as f:
                # Join with newline to avoid extra line at the end
                f.write("\n".join(output_lines))
            print(f"Successfully created '{output_file_name}'")
        except IOError:
            print(f"Error: Could not write to file '{output_file_name}'.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python build_model.py <your_mis_no> <input_dataset.txt>")
    else:
        mis_number = sys.argv[1]
        input_file = sys.argv[2]
        generate_ngram_model(input_file, mis_number)
