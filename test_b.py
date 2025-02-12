from news import get_random_joke
from currency import format_exchange

test_data = [
    {"ccy": "USD", "base_ccy": "UAH", "buy": "41.25000", "sale": "41.85000"},
    {"ccy": "EUR", "base_ccy": "UAH", "buy": "42.55000", "sale": "43.55000"},
]

def cur_load_exchange():
    return test_data

def cur_load_exchange_error():
    return "😱 ой щось пішло не так: Помилка з'єднання"


def test_format_exchange(monkeypatch):
    monkeypatch.setattr("currency.load_exchange", cur_load_exchange)
    result = format_exchange()

    assert "USD/UAH" in result
    assert "EUR/UAH" in result
    assert "📉 Покупка: 41.25000" in result
    assert "📈 Продажа: 41.85000" in result


def test_format_exchange_error(monkeypatch):
    monkeypatch.setattr("currency.load_exchange", cur_load_exchange_error)
    result = format_exchange()
    assert "😱 ой щось пішло не так" in result

def test_get_random_joke():

    joke = get_random_joke()
    assert isinstance(joke, str)
    assert len(joke) > 0