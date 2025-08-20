from canonical_date_time import (
    date_to_canonical,
    time_to_canonical,
    extract_canonical_dates,
    extract_canonical_times,
    remove_canonical_date_time,
)
from inter_cleanup import clean_up_files
from html_tag_removal import remove_tags
from word_new_line import word_new_line
from url_handler import (
    extract_urls,
    remove_urls,
)
from usermention_handler import (
    extract_usermentions,
    remove_usermentions,
)
from hashtag_handler import (
    extract_hashtags,
    remove_hashtags,
)


# Complete pipeline for tokenization
def tokenize():
    inter_files = []
    std_files = []
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
    std_out_dates = extract_canonical_dates(split_words)
    print(f"Canonical date format extracted into: {std_out_dates}")
    std_files.append(std_out_dates)
    # Stage 5b: Extract time as a single token into a seperate file
    std_out_times = extract_canonical_times(split_words)
    print(f"Canonical time format extracted into: {std_out_times}")
    std_files.append(std_out_times)
    # Stage 5c: Remove these canonical formats from the original file
    no_date_time = remove_canonical_date_time(split_words)
    print("Removed canonical formats of date and time")
    print(f"File generated: {no_date_time}")
    inter_files.append(no_date_time)
    # Stage 6a: Extract urls as a single token
    std_out_urls = extract_urls(no_date_time)
    print(f"URLs extracted into: {std_out_urls}")
    std_files.append(std_out_urls)
    # Stage 6b: Remove urls from original file
    no_urls = remove_urls(no_date_time)
    print(f"File generated: {no_urls}")
    inter_files.append(no_urls)
    # Stage 7a: Extract usermentions as a single token
    std_out_usermentions = extract_usermentions(no_urls)
    print(f"Extracted usermentions into: {std_out_usermentions}")
    std_files.append(std_out_usermentions)
    # Stage 7b: Remove usermentions from original file
    no_usermentions = remove_usermentions(no_urls)
    print(f"File generated: {no_usermentions}")
    inter_files.append(no_usermentions)
    # Stage 8a: Extract hashtags as a single token
    std_out_hashtags = extract_hashtags(no_usermentions)
    print(f"Hashtags extracted into: {std_out_hashtags}")
    std_files.append(std_out_hashtags)
    # Stage 8b: Remove hashtags from original file
    no_hashtags = remove_hashtags(no_usermentions)
    print(f"File generated: {no_hashtags}")
    inter_files.append(no_hashtags)
    # Clean up stage to save memory in case of large corpus
    inter_clean = input(
        "Tokenization complete. Do you want to delete the intermediate files? [y/n]: "
    )
    if inter_clean == "y":
        clean_up_files(inter_files)
