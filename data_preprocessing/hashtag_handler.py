import re

# Regex patter for detecting hashtags of the type: #example_hashtag01
regex = r"#\w+"


# Extracts hashtags eg; #nlpisgreat and treats them as a single token
def extract_hashtags(input_file):
    output_file = "std_out_hashtags.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            hashtags = re.findall(regex, f_in.read())
        f_out.write(f"{len(hashtags)}" + "\n")
        for hashtag in hashtags:
            f_out.write(hashtag + "\n")
    return output_file


# Removes urls from files for further tokenization
def remove_hashtags(input_file):
    output_file = "no_hashtags.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file
