def create_master_std_out(std_files, output_file):
    total_tokens = 0
    all_tokens = []

    for file in std_files:
        with open(file, "r") as f_in:
            int_line = f_in.readline().strip()
            if int_line.isdigit():
                total_tokens += int(int_line)
            else:
                print(f"Warning: Skipping non-integer count in {file}")

            tokens_from_file = [line.strip() for line in f_in if line.strip()]
            all_tokens.extend(tokens_from_file)

    with open(output_file, "w") as f_out:
        f_out.write(f"{total_tokens}" + "\n")
        for token in all_tokens:
            f_out.write(token + "\n")
    return output_file
