import re
import os


# Function to convert date into a canonical format given as -> CF:D:yyyy-mm-dd
def date_to_canonical(input_file):
    month_mapping = {
        "january": "01",
        "february": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12",
    }
    regex = r"(\d{1,2})[/\s]+(January|February|March|April|May|June|July|August|September|October|November|December|\d{1,2})[/\s]+(\d{2,4})"
    output_file = "canonical_dates.txt"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            match = re.search(
                regex,
                row,
                re.IGNORECASE,
            )
            if match:
                day, month, year = match.groups()
                month_lower = month.lower()
                if month_lower in month_mapping:
                    month = month_mapping[month_lower]
                else:
                    month = f"{int(month):02d}"

                canonical_date = f"CF:D:{year}-{month}-{day} "
            else:
                canonical_date = ""

            f_out.write(
                re.sub(
                    regex,
                    canonical_date,
                    row,
                )
            )
    return output_file


# Function to convert time into a canonical format given as -> CF:T:19:00:IST (if time zone mention add otherwise don't)
def time_to_canonical(input_file):
    output_file = "canonical_times.txt"
    regex = r"(?<!CF:D:)\b(\d{1,2})[.:]?(\d{2})\s*(?:(a|p).?m.?)?\s*(IST|PST)?\b"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            match = re.search(
                regex,
                row,
                re.IGNORECASE,
            )
            if match:
                hour, minute, am_pm, timezone = match.groups()

                hour = int(hour)

                # Convert if 12 hour format is mentioned
                if am_pm:
                    am_pm = am_pm.lower()
                    if am_pm == "p" and hour != 12:
                        hour += 12
                    elif am_pm == "a" and hour == 12:
                        hour = 0

                # Default time zone setting
                if not timezone:
                    timezone = "IST"
                else:
                    timezone = timezone.upper()
                canonical_time = f"CF:T:{hour:02d}:{minute}:{timezone} "
            else:
                canonical_time = ""

            f_out.write(
                re.sub(
                    regex,
                    canonical_time,
                    row,
                )
            )

    return output_file


# Extraction functions for creating standard outputs
# A function that extracts canonical dates into a seperate file as a list
def extract_canonical_dates(input_file):
    output_file = "std_outs/std_out_dates.txt"
    regex = r"CF:D:\d{4}-\d{2}-\d{2}"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            extracted_dates = re.findall(regex, f_in.read())
        f_out.write(f"{len(extracted_dates)}" + "\n")
        for date in extracted_dates:
            f_out.write(date + "\n")
    return output_file


# Extracts canonical times into a seperate file as a list
def extract_canonical_times(input_file):
    output_file = "std_outs/std_out_times.txt"
    regex = r"CF:T:\d{2}:\d{2}:[A-Z]{3}"
    with open(output_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            extracted_times = re.findall(regex, f_in.read())
        f_out.write(f"{len(extracted_times)}" + "\n")
        for time in extracted_times:
            f_out.write(time + "\n")
    return output_file


# Removing these canonical formats from the file
def remove_canonical_date_time(input_file):
    inter_file = "no_date.txt"
    output_file = "inter_files/no_date_time.txt"
    regex_date = r"CF:D:\d{4}-\d{2}-\d{2}"
    regex_time = r"CF:T:\d{2}:\d{2}:[A-Z]{3}"
    with open(inter_file, "w") as f_out:
        with open(input_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex_date, "", row)
            f_out.write(mod_content)
    f_out.close()
    f_in.close()
    with open(output_file, "w") as f_out:
        with open(inter_file, "r") as f_in:
            row = f_in.read()
            mod_content = re.sub(regex_time, "", row)
            f_out.write(mod_content)
    os.remove(inter_file)
    return output_file
