
import re, collections


with open('key.txt', 'r') as f:
    word = f.read()
    words = word.split('\n')
word_counts = collections.Counter(words)


def correct_text_generic(text):
    return re.sub('[a-zA-Z]+', correct_match, text)


def correct_match(match):
    word = match.group()

    return correct(word)


def correct(word):

    candidates = (known(edits0(word)) or
                  known(edits1(word)) or
                  {word})
    return max(candidates, key=word_counts.get)


def known(words):
    return {w for w in words if w in word_counts}


def edits0(word):
    return {word}


def edits1(word):
    alphabet = ''.join([chr(ord('a') + i) for i in range(26)])

    def splits(word):
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

    pairs = splits(word)

    deletes = [a + b[1:] for (a, b) in pairs if b]
    transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
    replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
    inserts = [a + c + b for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}

if __name__ == '__main__':
    original_word = 'fianlly helloa cta'
    correct_word = correct_text_generic(original_word)
    print('Original word:%s\nCorrect word:%s' % (original_word, correct_word))
