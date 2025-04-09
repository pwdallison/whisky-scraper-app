import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

SCRAPER_API_KEY = "c60c11ec758bf09739d6adaba094b889"  # Your ScraperAPI key

st.title("🥃 Whisky Price Scraper – with ScraperAPI")

url = st.text_input("Paste The Whisky Exchange or Master of Malt URL here:")

if st.button("Scrape"):
    if url:
        # Use ScraperAPI with stronger config
        params = {
            "api_key": SCRAPER_API_KEY,
            "url": url,
            "country_code": "uk",
            "keep_headers": "true",
            "render": "false"
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get("http://api.scraperapi.com", headers=headers, params=params)
        soup = BeautifulSoup(response.content, "html.parser")

        # Debug: Show the actual page we got (in case of redirects)
        st.code(response.url)

        # Try The Whisky Exchange selectors
        name_tag = soup.find("h1", class_="product-card-details__title")
        price_tag = soup.find("p", class_="product-action__price")

        # Fallback to Master of Malt selectors
        if not name_tag:
            name_tag = soup.find("h1")
        if not price_tag:
            price_tag = soup.find("meta", {"property": "product:price:amount"})

        # Parse data
        product_name = name_tag.text.strip() if name_tag else "Name not found"
        price = (
            price_tag["content"] if price_tag and price_tag.name == "meta"
            else price_tag.text.strip() if price_tag
            else "Price not found"
        )

        data = {
            "Name": product_name,
            "Price": price,
            "Reviews": "Not available (blocked or not visible)"
        }

        df = pd.DataFrame([data])
        st.write(df)

        st.download_button("Download CSV", df.to_csv(index=False), "whisky.csv", "text/csv")
    else:
        st.warning("Please enter a valid URL.")
