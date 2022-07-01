import urllib.request
from bs4 import BeautifulSoup
import json

def get_form_json(url: str):
    """
    Get the JSON like information from the Google Form at the input url.
    A certain script element in the form HTML has a "var FB_PUBLIC_LOAD_DATA_ = ..." statement with the desired information.
    That information will be extracted, parsed into JSON, and returned.
    """
    with urllib.request.urlopen(url) as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if "var FB_PUBLIC_LOAD_DATA_ = " in script.text:
            break
    else:
        raise ValueError("'var FB_PUBLIC_LOAD_DATA_ = ' could not be found in a script element of the HTML at the given url")
    info = script.text[27:-1]
    return json.loads(info)

def question_type_id_to_string(id):
    """
    Each question is given a number to identify its type.
    This function takes in that id and translates it to a string representing that type.
    """
    match id:
        case 0:
            return "short_answer"
        case 1:
            return "paragraph"
        case 2:
            return "multiple_choice"
        case 3:
            return "dropdown"
        case 4:
            return "checkboxes"
        case 5:
            return "linear_scale"
        case 6:
            return "title_and_description"
        case 7:
            return "grid"
        case 8:
            return "section"
        case 9:
            return "date"
        case 10:
            return "time"
        case _:
            return "unknown"

def parse_form_json(form_json):
    """
    Turn the extracted JSON from the Google Form into a more readable form.
    The data stored in the Form HTML, while structured, is undocumented and it is unclear what setting each item corresponds to.
    This function can be updated as those utilities are inferred.
    """
    form_info = {}
    form_info["title"] = form_json[3]
    form_info["description"] = form_json[1][0]
    form_info["id"] = form_json[14]
    form_info["view_url"] = f"https://docs.google.com/forms/d/{form_info['id']}/viewform"
    form_info["post_url"] = f"https://docs.google.com/forms/d/{form_info['id']}/formResponse"

    form_info["questions"] = []
    questions = form_json[1][1]
    for question in questions:
        question_info = {}
        question_info["title"] = question[1]
        question_info["description"] = question[2]
        question_info["type"] = question_type_id_to_string(question[3])
        match question_info["type"]:
            case "short_answer" | "paragraph" | "date" | "time":
                question_info["entry_id"] = question[4][0][0]
                question_info["required"] = bool(question[4][0][2])
            case "multiple_choice" | "dropdown" | "checkboxes" | "linear_scale":
                question_info["entry_id"] = question[4][0][0]
                question_info["choices"] = [choice[0] for choice in question[4][0][1]]
                question_info["required"] = bool(question[4][0][2])
            case "grid":
                question_info["entry_ids"] = [row[0] for row in question[4]]
                question_info["rows"] = [row[3][0] for row in question[4]]
                question_info["columns"] = [column[0] for column in question[4][0][1]]
                question_info["type"] = "checkbox_grid" if question[4][0][11][0] else "multiple_choice_grid"
                question_info["shuffle_row_order"] = bool(question[7])
                question_info["one_per_column"] = (question[8][0] == [8, 205] if question[8] else False)
                question_info["required"] = bool(question[4][0][2])

        form_info["questions"].append(question_info)

    return form_info

def form_info_from_url(url: str):
    """
    Get the structural information about the Form at the input url.
    """
    form_json = get_form_json(url)
    form_info = parse_form_json(form_json)
    return form_info

if __name__ == "__main__":
    url = "https://docs.google.com/forms/d/e/1FAIpQLScykTPZxLRtTXHAxxVN8l8RVPxzcfokD_HMkc5Hbio4sq3p_g/viewform"
    # url = input("Please input the url for the Google Form.\n")
    form_info = form_info_from_url(url)
    print(form_info)
    for question in form_info["questions"]:
        print(question)