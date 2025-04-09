import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("🥃 Whisky Price Scraper")

url = st.text_input("Paste Master of Malt Whisky URL here:")

if st.button("Scrape"):
    if url:
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

product_name = soup.find("h1").text.strip()

# Use alternative method to get the price — based on inspection of MoM HTML
price_tag = soup.find("meta", {"property": "product:price:amount"})
price = price_tag["content"] if price_tag else "Price not found"

# Try to get reviews
review_tag = soup.find("span", class_="review-count")
reviews = review_tag.text.strip() if review_tag else "No reviews"

data = {
    "Name": product_name,
    "Price": price,
    "Reviews": reviews,
}

        df = pd.DataFrame([data])
        st.write(df)
        st.download_button("Download CSV", df.to_csv(index=False), "whisky.csv", "text/csv")
    else:
        st.warning("Enter a URL first!")
