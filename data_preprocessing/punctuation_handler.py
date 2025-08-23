import re

# Regex pattern for extracting all types of punctuations leftover in the corpus
regex = r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]+'


# Extract punctuations
def extract_puncts(input_file):
    output_file = "std_out_punctuations.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            punctuations = re.findall(regex, f_in.read())
        f_out.write(f"{len(punctuations)}" + "\n")
        for punct in punctuations:
            f_out.write(punct + "\n")
    return output_file


# Remove punctuations from the file for further tokenization
def remove_puncts(input_file):
    output_file = "no_punctuations.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file
