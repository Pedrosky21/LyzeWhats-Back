import re
import regex


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002500-\U00002BEF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+"
)

def extract_emojis(text: str):
    return EMOJI_PATTERN.findall(text)


def split_emojis(s):
    if not s:
        return []
    return regex.findall(r'\X', s)  # detecta cada emoji correctamente
