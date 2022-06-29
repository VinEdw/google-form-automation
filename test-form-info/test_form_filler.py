import urllib.request, urllib.parse

url = "https://docs.google.com/forms/d/e/1FAIpQLScykTPZxLRtTXHAxxVN8l8RVPxzcfokD_HMkc5Hbio4sq3p_g/formResponse"

data = [
    # Multiple choice
    ("entry.1180240828", "Option 1"),
    # Checkboxes
    ("entry.862456411", "Option 1"),
    ("entry.862456411", "Option 3"),
    ("entry.862456411.other_option_response", "Other option"),
    ("entry.862456411", "__other_option__"),
    # Dropdown
    ("entry.608154294", "Option 2"),
    # Short answer
    ("entry.289639374", "This is my short answer."),
    # Long answer
    ("entry.1739314886", "This is my long answer."),
    # Linear scale
    ("entry.212265809", 8),
    # Date
    ("entry.663558137_year", 2022),
    ("entry.663558137_month", 6),
    ("entry.663558137_day", 29),
    # Time
    ("entry.280136681_hour", 22),
    ("entry.280136681_minute", 32),
    # Multiple choice grid
    ("entry.1735764173", "Column 1"),
    ("entry.1227466292", "Column 2"),
    ("entry.952095125", "Column 3"),
    ("entry.1236505173", "Column 4"),
    ("entry.393649146", "Column 3"),
    # Checkbox grid
    ("entry.780191199", "Column 1"),
    ("entry.849015232", "Column 2"),
    ("entry.849015232", "Column 3"),
    ("entry.1041749011", "Column 1"),
    ("entry.1041749011", "Column 2"),
    ("entry.1041749011", "Column 3"),
    ("entry.768381174", "Column 2"),
    ("entry.768381174", "Column 4"),
    ("entry.1031444894", "Column 1"),
    ("entry.1031444894", "Column 2"),
    ("entry.1031444894", "Column 3"),
    ("entry.1031444894", "Column 4"),
]
encoded_data = urllib.parse.urlencode(data).encode()
headers = {
    "referer": "https://docs.google.com/forms/d/e/1FAIpQLScykTPZxLRtTXHAxxVN8l8RVPxzcfokD_HMkc5Hbio4sq3p_g/viewform",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

request = urllib.request.Request(url, encoded_data, headers, method="POST")

with urllib.request.urlopen(request) as f:
    print(f.status)