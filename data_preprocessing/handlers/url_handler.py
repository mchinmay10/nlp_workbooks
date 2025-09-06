import re

regex = r"\bhttps?://\S+\b"


# Extracts urls eg; https://www.apple.com/in/ and treats them as a single token
def extract_urls(input_file):
    output_file = "std_outs/std_out_urls.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            urls = re.findall(regex, f_in.read())
        f_out.write(f"{len(urls)}" + "\n")
        for url in urls:
            f_out.write(url + "\n")
    return output_file


# Removes urls from file for further tokenization
def remove_urls(input_file):
    output_file = "inter_files/no_urls.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex, "", row)
            f_out.write(mod_content)
    return output_file


# Combined function that executes both the above functions
def handle_urls(input_file):
    extract_file = extract_urls(input_file)
    remove_file = remove_urls(input_file)
    return extract_file, remove_file
