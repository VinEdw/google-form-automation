import urllib.request, urllib.parse
from get_form_structure import form_info_from_url, summarize_form_info

def prompt_options(options: list[str], description: str = None) -> int:
    """
    Print the list of options for the user, each preceded by a number.
    Then, prompt the user for a number.
    If the number is out of range, keep asking for the number until they input one.
    Return their input number.
    If they give a blank response, None is returned.
    Optionally precede the option list with a description.
    """
    if description:
        print(description)
    for i, option in enumerate(options):
        print(f"({i}) {option}")
    while True:
        num = input(">>> ")
        if num == "":
            num = None
            print("Skipping")
            break
        try:
            num = int(num)
        except ValueError:
            print("Invalid Input")
            continue
        if 0 <= num < len(options):
            break
        print("Invalid Input")
    return num

def prompt_y_n(question: str = "") -> bool:
    """
    Prompt the user with the yes-or-no question, followed by, '(Y/N)'.
    Return True if they input Y, False if they input N, and prompt them again if they input neither.
    """
    if question:
        print(f"{question} (Y/N)")
    else:
        print("(Y/N)")
    while True:
        choice = input(">>> ").strip().upper()
        if choice in ("Y", "N"):
            break
        print("Invalid Input")
    return choice == "Y"

def prompt_between(low: int, high: int, description: str = None) -> int:
    """
    Prompt the user to pick an integer within a certain range (between the low and high inclusive).
    Return the integer they pick. Optionally add a description to show before the input message.
    If they give a blank response, None is returned.
    """
    if description != None:
        print(f"{description} ({low} to {high})")
    else:
        print(f"({low} to {high})")
    while True:
        num = input(">>> ")
        if num == "":
            num = None
            print("Skipping")
            break
        try:
            num = int(num)
            if low <= num <= high:
                break
        except ValueError:
            pass
        print("Invalid Input")
    return num

def print_if_truthy(text, fallback: str = None) -> None:
    """
    If the input is truthy, print it. If the fallback is set, print that if the input is falsy.
    Otherwise, do nothing.
    """
    if text:
        print(text)
    elif fallback != None:
        print(fallback)

def prompt_for_url():
    """
    Prompt the user, asking them for the url of the Google Form.
    Return the form_info.
    """
    url = input("Please input the url for the Google Form.\n")
    return form_info_from_url(url)

def fill_form(form_info) -> list[tuple[str, str]]:
    """
    Prompt the user for what they would like to put for as an answer for each question in the form.
    Return a list of tuples with the answer data that would get sent in a POST request.
    This data can also be used to create a filled link.
    """
    data = []
    double_line = "<" + 50 * "=" + ">"
    single_line = "<" + 50 * "-" + ">"
    print(form_info["title"])
    print_if_truthy(form_info["description"])
    print(form_info["view_url"])
    print(double_line)
    if form_info["collect_email_addresses"]:
        print("This form collects email addresses. Please enter your email.")
        email = input(">>> ")
        data.append(("emailAddress", email))
    for question in form_info["questions"]:
        print(f"Type: {question['type']}")
        print_if_truthy(question["title"], "Untitled")
        print_if_truthy(question["description"])
        if "required" in question:
            print("Required" if question["required"] else "Optional")
        match question["type"]:
            case "short_answer" | "paragraph":
                text = input(">>> ")
                if text != "":
                    data.append((f"entry.{question['entry_id']}", text))
            case "multiple_choice" | "dropdown":
                choice_index = prompt_options(question["choices"], "Choose one of the following:")
                if choice_index != None:
                    data.append((f"entry.{question['entry_id']}", question["choices"][choice_index]))
            case "checkboxes":
                print(question["choices"])
                print("Select the checkboxes you wish to keep.")
                for option in question["choices"]:
                    keeping = prompt_y_n(option or "Other...")
                    if keeping:
                        if option != "":
                            data.append((f"entry.{question['entry_id']}", option))
                        else:
                            text = input("Input Other Option\n>>> ")
                            data.append((f"entry.{question['entry_id']}.other_option_response", text))
                            data.append((f"entry.{question['entry_id']}", "__other_option__"))
            case "linear_scale":
                print_if_truthy(question["low_label"])
                print_if_truthy(question["high_label"])
                low = int(question["choices"][0])
                high = int(question["choices"][-1])
                num = prompt_between(low, high, "Pick a number within the bounds.")
                if num != None:
                    data.append((f"entry.{question['entry_id']}", num))
            case "section":
                print(single_line)
            case "time":
                hour = prompt_between(0, 23, "Input the hour in 24-hour format.")
                if hour != None:
                    data.append((f"entry.{question['entry_id']}_hour", hour))
                minute = prompt_between(0, 59, "Input the minute.")
                if minute != None:
                    data.append((f"entry.{question['entry_id']}_minute", minute))
            case "date":
                year = prompt_between(1, 9999, "Input the year.")
                if year != None:
                    data.append((f"entry.{question['entry_id']}_year", year))
                month = prompt_between(1, 12, "Input the month.")
                if month != None:
                    data.append((f"entry.{question['entry_id']}_month", month))
                day = prompt_between(1, 31, "Input the day.")
                if day != None:
                    data.append((f"entry.{question['entry_id']}_day", day))
            case "multiple_choice_grid":
                if question["one_per_column"]:
                    print("One per column")
                for i, row in enumerate(question["rows"]):
                    print(row)
                    choice_index = prompt_options(question["columns"], "Choose one of the following for this row:")
                    if choice_index != None:
                        data.append((f"entry.{question['entry_ids'][i]}", question["columns"][choice_index]))
            case "checkbox_grid":
                if question["one_per_column"]:
                    print("One per column")
                print("Rows:", question["rows"])
                print("Colums:", question["columns"])
                for i, row in enumerate(question["rows"]):
                    print(20 * "-")
                    print(row)
                    for column in question["columns"]:
                        keeping = prompt_y_n(column)
                        if keeping:
                            data.append((f"entry.{question['entry_ids'][i]}", column))
        print()
    return data

def get_filled_form_link(form_info, form_data: list[tuple[str, str]]):
    """Get a link to the form prefilled with the input data."""
    url = form_info["view_url"]
    encoded_data = urllib.parse.urlencode(form_data)
    return f"{url}?{encoded_data}"

def post_to_form(form_info, form_data: list[tuple[str, str]]):
    """Send the form data to the Google form."""
    url = form_info["post_url"]
    encoded_data = urllib.parse.urlencode(form_data).encode()
    headers = {
        "referer": form_info["view_url"],
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url, encoded_data, headers, method="POST")
    with urllib.request.urlopen(request) as f:
        return f.status


if __name__ == "__main__":
    try:
        print("Press <Ctrl-C> to exit at any time.")
        form_info = prompt_for_url()
        match prompt_options(["Get a summary of the form", "Fill out the form"], "What would you like to do?"):
            case 0:
                print(summarize_form_info(form_info))
            case 1:
                form_data = fill_form(form_info)
                print("Filled URL:", get_filled_form_link(form_info, form_data))
                if prompt_y_n("Would you like to try submitting this data to the form?"):
                    post_to_form(form_info, form_data)
    except KeyboardInterrupt:
        print("Keyboard Interruput")
    # except Exception as e:
    #     print(e)
    print("Exiting")
