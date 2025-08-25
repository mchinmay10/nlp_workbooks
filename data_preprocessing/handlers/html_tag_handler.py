import re


# Removing HTML tags using Regular expression
def remove_tags(input_file):
    output_file = "inter_files/no_html.txt"
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
