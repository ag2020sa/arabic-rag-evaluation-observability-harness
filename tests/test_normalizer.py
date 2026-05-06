from rag_eval_harness.arabic.normalizer import arabic_ratio, coverage, normalize_arabic, tokenize


def test_normalize_arabic_removes_diacritics_and_variants():
    assert normalize_arabic("إِجَازَةٌ سَنَوِيَّة") == "اجازه سنويه"


def test_arabic_ratio():
    assert arabic_ratio("مرحبا hello") > 0.0
    assert arabic_ratio("12345") == 0.0


def test_coverage():
    assert coverage("يستحق العامل 21 يوم و 30 يوم", ["21", "30"]) == 1.0


def test_tokenize():
    assert "اجازه" in tokenize("كم مدة الإجازة السنوية؟")
