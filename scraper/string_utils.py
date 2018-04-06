"""Defines common string utils."""

def normalize(s):
    """Trim the string to a standard format."""
    # Remove leading/trailing whitespace
    s = s.strip()
    # Remove trailing comma
    if s.endswith(","):
        s = s[:-1]

    return s

def htmlify_list(l):
    """Turn a list into an html ordered list."""
    r = "<ol>"
    for i in l:
        r += "<li>{}</li>".format(str(i))
    r += "</ol>"
    return r
