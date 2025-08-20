import re

# Dictionary to map emojis to their semantics
emojis_dict = {
    ":)": "smiley face",
    ":(": "sad face",
    ":D": "laughing",
    ":o": "surprised",
    ";)": "winking",
    ":P": "sticking out tongue",
    "<3": "heart",
    "8)": "nerd",
    "^-^": "anime happy face",
    ":|": "neutral face",
    ":/": "disappointed face",
    ":'(": "crying",
    "XD": "laughing hard",
}

# Regex to match emoticons
regex = r"(?:[:;]-?['\)\(DPp3o|/])|(?:<3)|(?:\^_?\^)|(?:[xX]D)|(?:8\))"


# Extract emoticons in standard format
def extract_emoticons(input_file):
    output_file = "std_out_emoticons.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            emoticons = re.findall(regex, f_in.read())
        f_out.write(f"{len(emoticons)}" + "\n")
        for emoticon in emoticons:
            f_out.write(emoticon + "\n")
    return output_file


# Remove emoticons from file for further tokenization
def remove_emoticons(input_file):
    output_file = "no_emoticons.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file
