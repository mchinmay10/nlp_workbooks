# Extract all remaining tokens
def extract_remaining(input_file):
    output_file = "std_out_remaining.txt"
    tokens = []
    with open(input_file, "r") as f_in:
        for line in f_in:
            token = line.strip()
            if token:
                tokens.append(token)
    with open(output_file, "w") as f_out:
        f_out.write(f"{len(tokens)}" + "\n")
        for token in tokens:
            f_out.write(token + "\n")
    return output_file


# Remove all remaining tokens - empty corpus for consistency and error checking
def remove_remaining(input_file):
    output_file = "no_remaining.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            f_out.write(row[0:0])
    return output_file
