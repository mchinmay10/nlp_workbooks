import re


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
