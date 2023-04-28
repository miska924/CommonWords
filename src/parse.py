import pymorphy2
import re
import json

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
    processed_text = ""
    cursor = 0
    for item in re.finditer('\w+', text):
        b, e = item.start(0), item.end(0)
        if normalize_word(text[b:e]) in words_norm:
            processed_text += text[cursor:b] + '<b>' + text[b:e] + '</b>'
        else:
            processed_text += text[cursor:b] + text[b:e]
        cursor = e
    processed_text += text[cursor:]
    return processed_text

def process(text, words):
    text = re.sub('<b>|</b>',"", text)
    words = re.sub('<b>|</b>',"", words)

    text_norm = normalize_text(text)
    words_norm = normalize_text(words)

    return select(text, words_norm), select(words, text_norm)


if __name__ == '__main__':
    text = 'У попа была собака, он её любил. Она съела кусок мяса - он её убил, в землю закопал и на камне написал: "У попа была собака ..."'
    words = 'люблю куски дерева'

    text, words = process(text, words)
    print(text)
    print()
    print(words)