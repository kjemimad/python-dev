import pytest

from finscrap.parser import ParseError, Quote, parse_quote

# Extrait HTML minimal qui reproduit la structure réelle de Yahoo Finance
VALID_HTML = """
<html>
<body>
  <h1 class="yf-18s5v3y">Apple Inc. (AAPL)</h1>
  <fin-streamer data-field="regularMarketPrice" data-value="207.43">207.43</fin-streamer>
  <fin-streamer data-field="regularMarketChange" data-value="1.23">+1.23</fin-streamer>
  <fin-streamer data-field="regularMarketChangePercent" data-value="0.597">+0.60%</fin-streamer>
  <fin-streamer data-field="regularMarketVolume" data-value="38,033,227">38,033,227</fin-streamer>
  <fin-streamer data-field="marketCap" data-value="3.979T">3.979T</fin-streamer>
</body>
</html>
"""

MISSING_PRICE_HTML = """
<html>
<body>
  <h1 class="yf-18s5v3y">Apple Inc. (AAPL)</h1>
  <fin-streamer data-field="regularMarketChange" data-value="1.23">+1.23</fin-streamer>
  <fin-streamer data-field="regularMarketChangePercent" data-value="0.597">+0.60%</fin-streamer>
  <fin-streamer data-field="regularMarketVolume" data-value="38,033,227">38,033,227</fin-streamer>
  <fin-streamer data-field="marketCap" data-value="3.979T">3.979T</fin-streamer>
</body>
</html>
"""

INVALID_PRICE_HTML = """
<html>
<body>
  <h1 class="yf-18s5v3y">Apple Inc. (AAPL)</h1>
  <fin-streamer data-field="regularMarketPrice" data-value="N/A">N/A</fin-streamer>
  <fin-streamer data-field="regularMarketChange" data-value="1.23">+1.23</fin-streamer>
  <fin-streamer data-field="regularMarketChangePercent" data-value="0.597">+0.60%</fin-streamer>
  <fin-streamer data-field="regularMarketVolume" data-value="38,033,227">38,033,227</fin-streamer>
  <fin-streamer data-field="marketCap" data-value="3.979T">3.979T</fin-streamer>
</body>
</html>
"""

MISSING_NAME_HTML = """
<html>
<body>
  <fin-streamer data-field="regularMarketPrice" data-value="207.43">207.43</fin-streamer>
  <fin-streamer data-field="regularMarketChange" data-value="1.23">+1.23</fin-streamer>
  <fin-streamer data-field="regularMarketChangePercent" data-value="0.597">+0.60%</fin-streamer>
  <fin-streamer data-field="regularMarketVolume" data-value="38,033,227">38,033,227</fin-streamer>
  <fin-streamer data-field="marketCap" data-value="3.979T">3.979T</fin-streamer>
</body>
</html>
"""


def test_parse_quote_returns_quote_instance() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert isinstance(result, Quote)


def test_parse_quote_symbol() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.symbol == "AAPL"


def test_parse_quote_name() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.name == "Apple Inc. (AAPL)"


def test_parse_quote_price() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.price == 207.43


def test_parse_quote_change() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.change == 1.23


def test_parse_quote_change_pct() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.change_pct == 0.597


def test_parse_quote_volume() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.volume == "38,033,227"


def test_parse_quote_market_cap() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.market_cap == "3.979T"


def test_parse_quote_scraped_at_is_set() -> None:
    result = parse_quote("AAPL", VALID_HTML)
    assert result.scraped_at is not None


def test_parse_quote_raises_on_missing_price() -> None:
    with pytest.raises(ParseError, match="regularMarketPrice"):
        parse_quote("AAPL", MISSING_PRICE_HTML)


def test_parse_quote_raises_on_invalid_price() -> None:
    with pytest.raises(ParseError, match="float"):
        parse_quote("AAPL", INVALID_PRICE_HTML)


def test_parse_quote_raises_on_missing_name() -> None:
    with pytest.raises(ParseError, match="company name"):
        parse_quote("AAPL", MISSING_NAME_HTML)


def test_parse_quote_raises_on_empty_html() -> None:
    with pytest.raises(ParseError):
        parse_quote("AAPL", "<html></html>")


def test_parse_quote_different_symbol() -> None:
    result = parse_quote("MSFT", VALID_HTML)
    assert result.symbol == "MSFT"
