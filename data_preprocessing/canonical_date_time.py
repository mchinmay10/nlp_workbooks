import re


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
