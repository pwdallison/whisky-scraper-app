import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

SCRAPER_API_KEY = "c60c11ec758bf09739d6adaba094b889"  # Your live key

st.title("🥃 Whisky Price Scraper – with ScraperAPI")

url = st.text_input("Paste The Whisky Exchange or Master of Malt URL here:")

if st.button("Scrape"):
    if url:
        # ScraperAPI proxy
        proxy_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(proxy_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # The Whisky Exchange selectors
        name_tag = soup.find("h1", class_="product-card-details__title")
        price_tag = soup.find("p", class_="product-action__price")

        # Master of Malt fallback selectors
        if not name_tag:
            name_tag = soup.find("h1")
        if not price_tag:
            price_tag = soup.find("meta", {"property": "product:price:amount"})

        product_name = name_tag.text.strip() if name_tag else "Name not found"
        price = (
            price_tag["content"] if price_tag and price_tag.name == "meta"
            else price_tag.text.strip() if price_tag
            else "Price not found"
        )

        data = {
            "Name": product_name,
            "Price": price,
            "Reviews": "Not available (blocked or not shown)"
        }

        df = pd.DataFrame([data])
        st.write(df)

        st.download_button("Download CSV", df.to_csv(index=False), "whisky.csv", "text/csv")
    else:
        st.warning("Please enter a valid URL.")
