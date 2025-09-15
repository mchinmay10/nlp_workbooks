import sys


def load_ngram_model(file_path):
    """Loads an n-gram model from a file into a dictionary."""
    model = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                # The n-gram is all parts except the last, count is the last part
                ngram = tuple(parts[:-1])
                count = int(parts[-1])
                model[ngram] = count
    except FileNotFoundError:
        return None  # Return None if the model file doesn't exist
    return model


def predict_next_word(input_phrase, mis_no):
    """Predicts the next word based on the input phrase using the generated n-gram models."""
    tokens = input_phrase.lower().split()
    n = len(tokens) + 1  # We need the (n+1)-gram model

    # Determine which model file to use
    model_map = {2: "bigram", 3: "trigram", 4: "four-gram", 5: "five-gram"}

    if n not in model_map:
        return "Cannot predict. Please provide between 1 and 4 words."

    model_name = model_map[n]
    file_name = f"{mis_no}_{model_name}-output.txt"

    # Load the corresponding n-gram model
    ngram_model = load_ngram_model(file_name)

    if ngram_model is None:
        return (
            f"Model file '{file_name}' not found. Please run the model builder first."
        )

    # Find all n-grams that start with the input phrase
    prefix = tuple(tokens)
    candidates = {}
    for ngram, count in ngram_model.items():
        if ngram[:-1] == prefix:
            candidates[ngram] = count

    if not candidates:
        return "Could not find a match to predict the next word."

    # Find the most frequent n-gram among the candidates
    most_likely_ngram = max(candidates, key=candidates.get)

    # The prediction is the last word of this n-gram
    prediction = most_likely_ngram[-1]

    return prediction


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict_word.py <your_mis_no>")
    else:
        mis_number = sys.argv[1]
        print("Next Word Prediction Model is ready.")
        print("Enter a phrase (1-4 words) or type 'exit' to quit.")

        while True:
            user_input = input("> ")
            if user_input.lower() == "exit":
                break

            prediction = predict_next_word(user_input, mis_number)
            print(f"Input: '{user_input}'")
            print(f"Predicted next word: {prediction}\n")
