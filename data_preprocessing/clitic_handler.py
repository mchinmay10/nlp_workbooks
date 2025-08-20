import re

# Dictionary to map clitics to their expanded forms
clitics_dict = {
    "don't": ["do", "not"],
    "can't": ["can", "not"],
    "won't": ["will", "not"],
    "isn't": ["is", "not"],
    "i'm": ["i", "am"],
    "you're": ["you", "are"],
    "it's": ["it", "is"],
    "they're": ["they", "are"],
    "we're": ["we", "are"],
    "what's": ["what", "is"],
    "who's": ["who", "is"],
    "nlp's": ["nlp", "'s"],
    "that's": ["that", "is"],
}

# Regex to match clitics
regex = r"\b(\w+'\w+)(?=\s|\b|$|[,.;?!:])"


# Function to extract clitics as a single token
def extract_clitics(input_file):
    clitics_list = []
    with open(input_file, "r") as f_in:
        row = f_in.read()
        clitics = re.findall(regex, row)
        for clitic in clitics:
            clitics_list.append(clitic)
    # Used for testing
    # print(clitics_list)
    return clitics_list


# Function to remove clitics from the file for further tokenization
def remove_clitics(input_file):
    output_file = "no_clitics.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file


# Function that processes the clitics, maps them and them splits them into corresponding parts
def process_clitics(input_file):
    output_file = "std_out_clitics.txt"
    clitics = extract_clitics(input_file)
    with open(output_file, "w") as f_out:
        f_out.write(f"{2*len(clitics)}" + "\n")
        for clitic in clitics:
            clitic = clitic.lower()
            if clitic in clitics_dict:
                clitic_list = clitics_dict[clitic]
                for c in clitic_list:
                    f_out.write(c + "\n")
            else:
                f_out.write("Clitic: " + clitic + " not mapped!\n")
    return output_file
