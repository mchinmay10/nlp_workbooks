import re

# Regex to match hyphenated words
regex = r"\b[\w.]+(?:-[\w.]+)+\b"


# Extract hyphenated words as a single token
def extract_hyphen_words(input_file):
    words_list = []
    with open(input_file, "r") as f_in:
        row = f_in.read()
        hyphen_words = re.findall(regex, row)
        for word in hyphen_words:
            words_list.append(word)
    return words_list


# Remove hyphenated words the file for further tokenization
def remove_hyphen_words(input_file):
    output_file = "inter_files/no_hyphen_words.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file


# Process hyphenated words for splitting and for generating standard output
def process_hyphen_words(input_file):
    output_file = "std_outs/std_out_hyphen_words.txt"
    hyphen_words = extract_hyphen_words(input_file)
    words_list = []
    with open(output_file, "w") as f_out:
        f_out.write(f"{2*len(hyphen_words)}" + "\n")
        for word in hyphen_words:
            split_words = re.split(r"(?<=[\w.])(?=-)", word)
            for split_word in split_words:
                words_list.append(split_word)
        for word in words_list:
            f_out.write(word + "\n")
    return output_file
