import re


def parse_deep_seek(s):
    """
    Parse a string containing '<think>' ... '</think>' sections.

    Args:
        s (str): Input string.

    Returns:
        dict: A dictionary where keys are 'answer' and values are the rest 
              of the input string,
              and key 'think' with value is the content within '<think> 
              ... '</think>' sections.
    """
    # Regular expression pattern to match '<think>' ... '</think>' sections
    pattern = r'<think>(.*?)</think>'
    think_content = re.findall(pattern, s)
    answer = re.sub(pattern, '', s)
    return {'answer': answer.strip(), 'think': think_content[0] if think_content else ''}


def speech_fix(t):
    new = t.cleaned.replace(" I'm ", ' I am ')
    new = new.cleaned.replace(" Im ", ' I am ')
    new = new.cleaned.replace(" im ", ' i am ')
    new = new.cleaned.replace("I'm ", 'I am ')
    new = new.cleaned.replace("Hey ", 'Hello ')
    new = new.cleaned.replace("hey ", 'hello ')
    return new

def add_space_after_punctuation(text):
    # Regex pattern: match any of . ? ! : not followed by a space or end of string
    return re.sub(r'([.?!:])(?![\s]|$)', r'\1 ', text)

def remove_hashtags(text):
    """
    Removes all hashtags (words starting with '#') from the input string.
    """
    return re.sub(r'#\w+', '', text).strip()

def clean_string(input_string):
#     allowed_chars = r"[^a-zA-Z0-9.,!?;:'\"()\-\s]"
    allowed_chars = r"[^a-zA-Z0-9.,?!': \n]"
    cleaned = re.sub(allowed_chars, '', input_string)
    return add_space_after_punctuation(remove_hashtags(cleaned))



def split_stream_into_speech_chunks(stream_generator, punctuation_chars={".", "!", "?", ":"}):
    """
    Splits a stream of words into speech chunks based on a set of punctuation characters.
    Yields complete chunks ending in a punctuation character.
    """
    buffer = ""
    # Escape punctuation for regex
    punctuation_regex = "|".join(re.escape(p) for p in punctuation_chars)

    # Regex pattern for sentence-ending punctuation
    sentence_end_pattern = re.compile(rf'(.*?[{punctuation_regex}])(\s|$)')

    for word in stream_generator:
        buffer += word

        # Look for any complete chunk
        while True:
            match = sentence_end_pattern.search(buffer)
            if match:
                chunk = match.group(1).strip()
                yield clean_string(chunk)
                buffer = buffer[match.end():]
            else:
                break

    # Yield any leftover buffer as a final chunk
    if buffer.strip():
        yield buffer.strip()








# def split_stream_into_speech_chunks(stream_generator, punctuation_chars={".", "!", "?", ":", "\n"}):
#     """
#     Splits a stream of words into speech chunks based on punctuation and non-alphanumeric characters.
#     Yields complete chunks ending in punctuation or encountering a symbol/emoji.
#     """
#     buffer = ""
#     escaped_punct = "".join(re.escape(p) for p in punctuation_chars)
#     sentence_end_pattern = re.compile(
#         rf'(.*?[{escaped_punct}|\W&&[^\s{escaped_punct}]])(\s|$)',
#         re.UNICODE
#     )
#     sentence_end_pattern = re.compile(
#         rf'(.*?[{escaped_punct}])(\s|$)|(.+?)([^\w\s{escaped_punct}])',
#         re.UNICODE
#     )
#     for word in stream_generator:
#         buffer += word
#         while True:
#             match = sentence_end_pattern.search(buffer)
#             if not match:
#                 break
#             if match.group(1):  # Matched punctuation-based end
#                 chunk = match.group(1).strip()
#                 buffer = buffer[match.end():]
#             else:  # Matched emoji or symbol-based split
#                 chunk = (match.group(3) + match.group(4)).strip()
#                 buffer = buffer[match.end():]
#             yield clean_string(chunk)
#     if buffer.strip():
#         yield buffer.strip()











# def split_stream_into_speech_chunks(stream_generator, punctuation_chars={".", "!", "?", ":", "\n"}):
#     """
#     Splits a stream of text into chunks based on:
#     - Ending in a punctuation character, or
#     - Containing a non-alphanumeric, non-whitespace, non-allowed-punctuation character (e.g., emojis/symbols).
# 
#     It avoids breaking on quotes or other common grammatical marks.
#     """
#     buffer = ""
#     allowed_punct = "".join(re.escape(p) for p in punctuation_chars)
# 
#     # Pattern explanation:
#     # 1. Match a chunk ending in a punctuation character
#     # 2. Or match a chunk ending in a disallowed symbol (not alphanumeric, not whitespace, not allowed punctuation)
#     sentence_end_pattern = re.compile(
#         rf"""
#         (.*?[{allowed_punct}])(?=\s|$) |     # Group 1: ends in punctuation
#         (.*?[^a-zA-Z0-9\s{allowed_punct}])   # Group 2: ends in disallowed symbol
#         """,
#         re.UNICODE | re.VERBOSE
#     )
# 
#     for word in stream_generator:
#         buffer += word
# 
#         while True:
#             match = sentence_end_pattern.search(buffer)
#             if not match:
#                 break
# 
#             chunk = (match.group(1) or match.group(2)).strip()
#             yield chunk
#             buffer = buffer[match.end():]
# 
#     if buffer.strip():
#         yield buffer.strip()
# 
# 




