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

if __name__ == "__main__":
    url = "https://docs.google.com/forms/d/e/1FAIpQLScykTPZxLRtTXHAxxVN8l8RVPxzcfokD_HMkc5Hbio4sq3p_g/viewform"
    # url = input("Please input the url for the Google Form.\n")
    form_json = get_form_json(url)
    print(form_json)