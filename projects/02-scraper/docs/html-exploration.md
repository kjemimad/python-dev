# Yahoo Finance HTML Exploration

Before writing the parser, we explored the HTML structure of Yahoo Finance
to identify exactly where the financial data is located.

## Method

We fetched the raw HTML of a Yahoo Finance quote page using requests
and saved it locally for inspection :

```python
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}
response = requests.get(
    "https://finance.yahoo.com/quote/AAPL",
    headers=headers,
    timeout=10,
)
with open("/tmp/yahoo_aapl.html", "w", encoding="utf-8") as f:
    f.write(response.text)
```

## Findings

Yahoo Finance uses custom `<fin-streamer>` tags with a `data-field` attribute
to identify each data point, and a `data-value` attribute containing the raw
numeric value.

### Price data

```python
tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
# <fin-streamer data-field="regularMarketPrice" data-value="207.43">207.43</fin-streamer>

tag = soup.find("fin-streamer", {"data-field": "regularMarketChange"})
# <fin-streamer data-field="regularMarketChange" data-value="1.23">+1.23</fin-streamer>

tag = soup.find("fin-streamer", {"data-field": "regularMarketChangePercent"})
# <fin-streamer data-field="regularMarketChangePercent" data-value="0.597">+0.60%</fin-streamer>
```

### Volume and market cap

```python
tag = soup.find("fin-streamer", {"data-field": "regularMarketVolume"})
# <fin-streamer data-field="regularMarketVolume" data-value="38,033,227">38,033,227</fin-streamer>

tag = soup.find("fin-streamer", {"data-field": "marketCap"})
# <fin-streamer data-field="marketCap" data-value="3.979T">3.979T</fin-streamer>
```

### Company name

```python
tag = soup.find("h1", class_=lambda c: isinstance(c, str) and "yf-" in c)
# <h1 class="yf-18s5v3y">Apple Inc. (AAPL)</h1>
```

## Why `data-value` and not the displayed text

The displayed text contains formatting — commas, symbols, percentage signs.
`data-value` contains the raw numeric value which is directly convertible
to float. We always use `data-value` for numeric fields.

## Why a lambda for the h1 class

Yahoo Finance generates dynamic class names like `yf-18s5v3y` that change
with each deployment. We search for any h1 whose class contains `"yf-"`
to make the parser robust to these changes.

## Note on stability

Yahoo Finance can change its HTML structure at any time without notice.
If the parser breaks, this document is the starting point for debugging —
re-fetch the HTML and compare the new structure to what is documented here.