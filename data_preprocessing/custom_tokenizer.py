import re
import string
from tokenize_pipeline import tokenize


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


if __name__ == "__main__":
    # remove_tags()
    # word_new_line()
    # handle_usermentions()
    # handle_urls()
    # handle_special_chars()
    # date_to_canonical("master_test.txt")
    tokenize()
