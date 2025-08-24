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
from clitic_handler import (
    process_clitics,
    remove_clitics,
)
from emoji_handler import (
    extract_emoticons,
    remove_emoticons,
)
from hyphen_handler import (
    process_hyphen_words,
    remove_hyphen_words,
)
from abbreviation_handler import (
    extract_abbreviations,
    remove_abbreviations,
)
from punctuation_handler import (
    extract_puncts,
    remove_puncts,
)
from remaining_handler import (
    extract_remaining,
    remove_remaining,
)
from create_std_out import (
    create_master_std_out,
)
from stanford_ner import (
    ner_tagging,
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
    # Stage 9a: Extract clitics and then process them as two tokens
    std_out_clitics = process_clitics(no_hashtags)
    print(f"Clitics extracted into: {std_out_clitics}")
    std_files.append(std_out_clitics)
    # Stage 9b: Remove clitics from the original file
    no_clitics = remove_clitics(no_hashtags)
    print(f"File generated: {no_clitics}")
    inter_files.append(no_clitics)
    # Stage 10a: Extract emoticons as a single token
    std_out_emotes = extract_emoticons(no_clitics)
    print(f"Emoticons extracted into: {std_out_emotes}")
    std_files.append(std_out_emotes)
    # Stage 10b: Remove emoticons from file for further processing
    no_emotes = remove_emoticons(no_clitics)
    print(f"File generated: {no_emotes}")
    inter_files.append(no_emotes)
    # Stage 11a: Extract hyphenated words as a single token and process them
    std_out_hyphen_words = process_hyphen_words(no_emotes)
    print(f"Hyphenated words extracted into: {std_out_hyphen_words}")
    std_files.append(std_out_hyphen_words)
    # Stage 11b: Remove hyphenated words from the file for further processing
    no_hyphen_words = remove_hyphen_words(no_emotes)
    print(f"File generated: {no_hyphen_words}")
    inter_files.append(no_hyphen_words)
    # Stage 12a: Extract abbreviations as a single token
    std_out_abbr = extract_abbreviations(no_hyphen_words)
    print(f"Abbreviations extracted into: {std_out_abbr}")
    std_files.append(std_out_abbr)
    # Stage 12b: Remove abbreviations from the file for further processing
    no_abbr = remove_abbreviations(no_hyphen_words)
    print(f"File generated: {no_abbr}")
    inter_files.append(no_abbr)
    # Stage 13a: Extract punctuations as a single token
    std_out_puncts = extract_puncts(no_abbr)
    print(f"Punctuations extracted into: {std_out_puncts}")
    std_files.append(std_out_puncts)
    # Stage 13b: Remove punctuations from the file for further processing
    no_puncts = remove_puncts(no_abbr)
    print(f"File generated: {no_puncts}")
    inter_files.append(no_puncts)
    # Stage 14a: Extract all the remaining token
    std_out_remaining = extract_remaining(no_puncts)
    print(f"All the remaining tokens extracted into: {std_out_remaining}")
    std_files.append(std_out_remaining)
    # Stage 14b: Remove all the remaining tokens
    no_remaining = remove_remaining(no_puncts)
    print(f"File generated: {no_remaining}")
    inter_files.append(no_remaining)
    # Create the master output file
    master_output = create_master_std_out(std_files, "612203120_assign2_output.txt")
    print(f"Final Tokenization result in: {master_output}")
    # Stanford NER Stage
    ner_tags = ner_tagging(master_output)
    print(f"NER output in: {ner_tags}")
    # Clean up stage to save memory in case of large corpus
    inter_clean = input(
        "Tokenization complete. Do you want to delete the intermediate files? [y/n]: "
    )
    if inter_clean == "y":
        clean_up_files(inter_files)
