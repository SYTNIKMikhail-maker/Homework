"""Sentence container and iterator implementation."""

import re


class SentenceIterator:
    """Iterates over words of a Sentence one by one."""

    def __init__(self, words: list):
        """Store words and set starting index."""
        self.words = words
        self.index = 0

    def __iter__(self):
        """Return self."""
        return self

    def __next__(self):
        """Return next word or raise StopIteration."""
        if self.index >= len(self.words):
            raise StopIteration
        word = self.words[self.index]
        self.index += 1
        return word


class Sentence:
    """Parses and validates a sentence string."""

    def __init__(self, text: str):
        """Accept only a string ending with . ! or ?"""
        if not isinstance(text, str):
            raise TypeError(f"Expected a string, got {type(text).__name__}")
        if not text.strip().endswith(('.', '!', '?')):
            raise ValueError("Sentence must end with . ! or ?")
        self.text = text

    def __repr__(self):
        """Show word and non-word character counts."""
        return f"<Sentence(words={len(self.words)}, other_chars={len(self.other_chars)})>"

    def __iter__(self):
        """Return SentenceIterator over words."""
        return SentenceIterator(self.words)

    def __getitem__(self, index):
        """Return word or slice by index."""
        return self.words[index]

    def _words(self):
        """Yield words one by one (lazy generator)."""
        for word in re.findall(r'[a-zA-Z]+', self.text):
            yield word

    @property
    def words(self):
        """Return list of all words (computed on the fly)."""
        return list(self._words())

    @property
    def other_chars(self):
        """Return list of all non-word characters."""
        return re.findall(r'[^a-zA-Z\s]', self.text)


s = Sentence('Hello !')
print(repr(s))
print(s._words())
print(next(s._words()))
print(s.words)
print(s.other_chars)
print(s[0])
print(s[0:2])

for word in s:
    print(word)

print(isinstance(iter(s), SentenceIterator))