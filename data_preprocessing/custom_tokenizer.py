import re
import string
from canonical_date_time import date_to_canonical, time_to_canonical
from inter_cleanup import clean_up_files


# Removing HTML tags using Regular expression
def remove_tags(input_file):
    output_file = "no_html.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            test_string = f_in.read()
            new_string = re.sub(
                r"<[^>]*>",
                "",
                test_string,
            )
            f_out.write(new_string)
    return output_file


# Converts every blank space to a new line character
# Output is a word / word-composition on a single line
def word_new_line(input_file):
    output_file = "split_words.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            [
                f_out.write(
                    re.sub(
                        r"^\s*$",
                        "\n",
                        row,
                        flags=re.MULTILINE,
                    )
                )
                for row in f_in.read()
            ]
    return output_file


def handle_special_chars():
    input_file = input("Enter name of input file: ")
    output_file = input("Enter name of output file: ")
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            punct_pattern = re.compile(f"[{re.escape(string.punctuation)}]+")
            spcl_chars = punct_pattern.findall(f_in.read())
            f_out.write(str(spcl_chars))


def stanford_ner():
    pass


def handle_clitics():
    pass


# Extracts user mentions eg; @elonmusk and they are treated as a single token
def extract_usermentions():
    input_file = input("Enter name of input file: ")
    output_file = input("Enter name of output file: ")
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            mentions = re.findall(r"@\w+", f_in.read())
            f_out.write(str(mentions))


def handle_emojis():
    pass


# Extracts urls eg; https://www.apple.com/in/ and treats them as a single token
def extract_urls():
    input_file = input("Enter the name of input file: ")
    output_file = input("Enter name of output file: ")
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            urls = re.findall(r"\bhttps?://\S+\b", f_in.read())
            f_out.write(str(urls))


# Complete pipeline for tokenization
def tokenize():
    inter_files = []
    print("----Custom Tokenizer----")
    input_file = input("Enter the name of the input file: ")
    # Stage 1: Removing HTML tags (if they are present)
    no_html = remove_tags(input_file)  # Does not contain any html tags
    print("Removal of HTML Tags complete")
    print(f"File generated: {no_html}")
    inter_files.append(no_html)
    # Stage 2: Convert dates to canonical format
    canonical_dates = date_to_canonical(no_html)
    print("Conversion of date to Canonical format done")
    print(f"File generated: {canonical_dates}")
    inter_files.append(canonical_dates)
    # Stage 3: Convert time to canonical format
    canonical_times = time_to_canonical(canonical_dates)
    print("Conversion of time to Canonical format done")
    print(f"File generated: {canonical_times}")
    inter_files.append(canonical_times)
    # Stage 4: Split words / word composition into new lines and create a seperate file to work on
    split_words = word_new_line(canonical_times)
    print("Word / word compositions are now split into new lines")
    print(f"File generated: {split_words}")
    inter_files.append(split_words)
    # Stage 5a: Extract dates as a single token into a seperate file
    # Stage 5b: Extract time as a single token into a seperate file
    # Clean up stage to save memory in case of large corpus
    inter_clean = input(
        "Tokenization complete. Do you want to delete the intermediate files? [y/n]: "
    )
    if inter_clean == "y":
        clean_up_files(inter_files)


if __name__ == "__main__":
    # remove_tags()
    # word_new_line()
    # handle_usermentions()
    # handle_urls()
    # handle_special_chars()
    # date_to_canonical("master_test.txt")
    tokenize()
