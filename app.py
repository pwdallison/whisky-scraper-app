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
        price = soup.find("span", class_="price").text.strip()
        reviews = soup.find("span", class_="review-count").text.strip()

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
