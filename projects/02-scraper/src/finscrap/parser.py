from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup, Tag


@dataclass
class Quote:
    """Represent a single stock quote sraped from Yahoo Finance."""
    symbol: str
    name: str
    price: float
    change: float
    change_pct: float
    volume: str
    market_cap: str
    scraped_at: datetime


class ParseError(Exception):
    """Raised when required data cannot be extracted from the HTML."""


def _get_streamer_value(soup: BeautifulSoup, field: str) -> str:
    """Extract the data-value attribute from a fin-streamer tag.

    Args:
        soup: The parsed HTML content.
        field: The data-field attribute to look for.

    Returns:
        The raw string value from the data-value attribute.

    Raises:
        ParseError: If the tag or attribute is not found.
    """
    result = soup.find("fin-streamer", {"data-field": field})
    if not isinstance(result, Tag):
        raise ParseError(f"Could not find fin-streamer tag with data-field='{field}'")
    value = result.get("data-value")
    if not isinstance(value, str) or not value.strip():
        raise ParseError(f"Empty or missing data-value for field='{field}'")
    return value.strip()


def _get_company_name(soup: BeautifulSoup) -> str:
    """Extract the company name from the page title.

    Args:
        soup: The parsed HTML content.

    Returns:
        The company name as a string.

    Raises:
        ParseError: If the company name cannot be found.
    """
    from bs4 import Tag

    tag_result = soup.find("h1", class_=lambda c: isinstance(c, str) and "yf-" in c)
    if not isinstance(tag_result, Tag):
        raise ParseError("Could not find company name h1 tag")
    text = tag_result.get_text(strip=True)
    if not text:
        raise ParseError("Company name h1 is empty")
    return text

def parse_quote(symbol: str, html: str) -> Quote:
    """Parse a yahoo Finance quote page and extract stock data.

    Args:
        symbol: The stock ticker symbol (e.g. "AAPL").
        html: The raw HTML content of the yahoo Finance quote page.

    Returns:
        A Quote dataclass will all extracted fields.

    Raises:
        ParseError: If any required data cannot be extracted or parsed.
    """
    soup = BeautifulSoup(html, "lxml")

    try:
        price = float(_get_streamer_value(soup, "regularMarketPrice"))
        change = float(_get_streamer_value(soup, "regularMarketChange"))
        change_pct = float(_get_streamer_value(soup, "regularMarketChangePercent"))
    except ValueError as e:
        raise ParseError(f"Could not convert price data to float: {e}") from e

    volume = _get_streamer_value(soup, "regularMarketVolume")
    market_cap = _get_streamer_value(soup, "marketCap")
    name = _get_company_name(soup)

    return Quote(
        symbol=symbol,
        name=name,
        price=price,
        change=change,
        change_pct=change_pct,
        volume=volume,
        market_cap=market_cap,
        scraped_at=datetime.now(),
    )
