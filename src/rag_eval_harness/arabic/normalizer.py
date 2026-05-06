from __future__ import annotations

import re
from typing import Iterable, List

ARABIC_DIACRITICS_RE = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
TATWEEL = "\u0640"
ARABIC_LETTER_RE = re.compile(r"[\u0600-\u06FF]")
NON_WORD_RE = re.compile(r"[^\w\s\u0600-\u06FF]+", flags=re.UNICODE)
ARABIC_PUNCTUATION_RE = re.compile(r"[،؛؟«»…ـ]")

ALEF_VARIANTS = str.maketrans({
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ٱ": "ا",
    "ى": "ي",
    "ئ": "ي",
    "ؤ": "و",
    "ة": "ه",
})

STOPWORDS = {
    "في", "من", "على", "عن", "الى", "إلى", "ما", "ماذا", "هل", "كم", "او", "أو",
    "هذا", "هذه", "ذلك", "تلك", "مع", "لا", "نعم", "هو", "هي", "كان", "كانت",
}


def strip_diacritics(text: str) -> str:
    return ARABIC_DIACRITICS_RE.sub("", text)


def normalize_arabic(text: str) -> str:
    """Normalize Arabic for lexical evaluation and retrieval diagnostics.

    This intentionally avoids aggressive stemming so that metrics remain explainable.
    """
    if not text:
        return ""
    text = text.replace(TATWEEL, "")
    text = strip_diacritics(text)
    text = text.translate(ALEF_VARIANTS)
    text = ARABIC_PUNCTUATION_RE.sub(" ", text)
    text = NON_WORD_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def arabic_ratio(text: str) -> float:
    if not text:
        return 0.0
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    arabic = sum(1 for c in letters if ARABIC_LETTER_RE.match(c))
    return arabic / len(letters)


def tokenize(text: str, remove_stopwords: bool = True) -> List[str]:
    normalized = normalize_arabic(text)
    toks = [t for t in normalized.split() if t]
    # Light normalization for the definite article to improve Arabic lexical matching.
    toks = [t[2:] if t.startswith("ال") and len(t) > 4 else t for t in toks]
    if remove_stopwords:
        toks = [t for t in toks if t not in STOPWORDS]
    return toks


def token_overlap(a: str, b: str) -> float:
    ta, tb = set(tokenize(a)), set(tokenize(b))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def contains_any(text: str, patterns: Iterable[str]) -> bool:
    n = normalize_arabic(text)
    return any(normalize_arabic(p) in n for p in patterns)


def coverage(text: str, required_terms: Iterable[str]) -> float:
    terms = list(required_terms)
    if not terms:
        return 1.0
    n = normalize_arabic(text)
    hits = sum(1 for term in terms if normalize_arabic(term) in n)
    return hits / len(terms)
