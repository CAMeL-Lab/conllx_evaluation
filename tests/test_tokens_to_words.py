

import pytest

from utils.tokens_to_words import get_unsegmented_words


@pytest.fixture
def test_cases():
    return [
        {'input': ['a+', 'b', 'c+', 'd'], 'expected': ['ab', 'cd']},
        {'input': ['a+', 'b+', 'c', 'd'], 'expected': ['abc', 'd']},
        {'input': ['a', '+b'], 'expected': ['ab']},
        {'input': ['a', 'b+', 'c'], 'expected': ['a', 'bc']},
        {'input': ['a', 'b'], 'expected': ['a', 'b']},
        {'input': ['a', '+b', '+c'], 'expected': ['abc']},
        {'input': ['a', '+b', 'c+', 'd'], 'expected': ['ab', 'cd']},
        {'input': ['a', '+b', 'c'], 'expected': ['ab', 'c']},
        {'input': ['a', '++'], 'expected': ['a', '++']},
        {'input': ['+', 'b+', 'c'], 'expected': ['+', 'bc']},
    ]

def test_get_unsegmented_words(test_cases):
    for test_case in test_cases:
        assert get_unsegmented_words(test_case['input']) == test_case['expected']

def test_get_unsegmented_words_enc_after_pro():
    with pytest.raises(AssertionError) as AE:
        get_unsegmented_words(['a+', '+d'])
    assert AE.type == AssertionError
    assert 'enclitic after proclitic' in str(AE.value)

def test_get_unsegmented_words_pro_last_token():
    with pytest.raises(AssertionError) as AE:
        get_unsegmented_words(['a', 'b+'])
    assert AE.type == AssertionError
    assert 'It should not be the last token in the sentence' in str(AE.value)

def test_get_unsegmented_words_enc_first_token():
    with pytest.raises(AssertionError) as AE:
        get_unsegmented_words(['+a', 'b'])
    assert AE.type == AssertionError
    assert 'First token is an enclitic' in str(AE.value)
    
    
    