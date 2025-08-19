import re


# Extracts user mentions eg; @elonmusk and they are treated as a single token
def extract_usermentions(input_file):
    output_file = "std_out_usermentions.txt"
    regex = r"@\w+"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            mentions = re.findall(regex, f_in.read())
        f_out.write(f"{len(mentions)}" + "\n")
        for mention in mentions:
            f_out.write(mention + "\n")
    return output_file


# Removes user mentions from file for further tokenization
def remove_usermentions(input_file):
    output_file = "no_usermentions.txt"
    regex = r"@\w+"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file
