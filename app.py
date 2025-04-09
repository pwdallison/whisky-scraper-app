import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("🥃 Whisky Price Scraper – The Whisky Exchange Edition")

url = st.text_input("Paste The Whisky Exchange Whisky URL here:")

if st.button("Scrape"):
    if url:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Product Name
        product_name_tag = soup.find("h1", class_="product-card-details__title")
        product_name = product_name_tag.text.strip() if product_name_tag else "Name not found"

        # Price
        price_tag = soup.find("p", class_="product-action__price")
        price = price_tag.text.strip() if price_tag else "Price not found"

        # Reviews (TWE doesn't expose review counts publicly)
        reviews = "Not available"

        # Output Data
        data = {
            "Name": product_name,
            "Price": price,
            "Reviews": reviews,
        }

        df = pd.DataFrame([data])
        st.write(df)

        st.download_button("Download CSV", df.to_csv(index=False), "whisky.csv", "text/csv")
    else:
        st.warning("Please enter a valid URL.")
