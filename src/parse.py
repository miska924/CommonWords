import pymorphy2
import re
import html2text

morph = pymorphy2.MorphAnalyzer()


def normalize_word(word):
    return morph.parse(word)[0].normal_form


def normalize_text(text):
    match = re.findall('\w+', text)

    res = list()
    for word in match:
        res.append(normalize_word(word))

    return res


def select(text, words_norm):
    words_norm_set = set(words_norm)
    processed_text = ""
    cursor = 0
    words = set()

    text_words = set()
    for item in re.finditer('\w+', text):
        b, e = item.start(0), item.end(0)
        normalized = normalize_word(text[b:e])

        text_words.add(normalized)

        if normalized in words_norm_set:
            words.add(normalized)
            processed_text += text[cursor:b] + '<b>' + text[b:e] + '</b>'
        else:
            processed_text += text[cursor:e]
        cursor = e
    processed_text += text[cursor:]
    return processed_text, words, 100 * len(words) // len(text_words) if len(text_words) else 100

def process(text, words):

    text = re.sub(r"\<\/?b\>", r"", text)
    words = re.sub(r"\<\/?b\>", r"", words)

    text = html2text.html2text(text, bodywidth=1e18)
    words = html2text.html2text(words, bodywidth=1e18)

    text = re.sub(r"\*\*", r"", text)
    words = re.sub(r"\*\*", r"", words)

    text = re.sub(r"\\", r"", text)
    words = re.sub(r"\\", r"", words)

    text = re.sub(r"[^\S^\n]+", r" ", text)
    words = re.sub(r"[^\S^\n]+", r" ", words)

    text_norm = normalize_text(text)
    words_norm = normalize_text(words)

    if text_norm > words_norm:
        processed_text, used_words, text_coverage = select(text, words_norm)
        processed_words, _, words_coverage = select(words, used_words)
    else:
        processed_words, used_words, text_coverage = select(words, text_norm)
        processed_text, _, words_coverage = select(text, used_words)

    processed_text = re.sub(r"[^\S^\n]*(\n[^\S^\n]*)+", r"<br><br>", processed_text)
    processed_words = re.sub(r"[^\S^\n]*(\n[^\S^\n]*)+", r"<br><br>", processed_words)

    processed_text = re.sub(r"([^\S^\n]*\n[^\S^\n]*)", r"<br>", processed_text)
    processed_words = re.sub(r"([^\S^\n]*\n[^\S^\n]*)", r"<br>", processed_words)

    return processed_text, processed_words, text_coverage, words_coverage
