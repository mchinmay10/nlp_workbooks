import re

# Regex pattern for extracting abbreviations of the type: U.S.A., CH.
regex = r"(?:[A-Z]+\.)+"


# Extract abbreviations
def extract_abbreviations(input_file):
    output_file = "std_out_abbreviations.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            abbreviations = re.findall(regex, f_in.read())
        f_out.write(f"{len(abbreviations)}" + "\n")
        for abbr in abbreviations:
            f_out.write(abbr + "\n")
    return output_file


# Remove abbreviations from the file for further tokenization
def remove_abbreviations(input_file):
    output_file = "no_abbreviations.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file
