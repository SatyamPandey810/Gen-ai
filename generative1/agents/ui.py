import streamlit as st

from agents import get_weather, get_news


st.set_page_config(
    page_title="AI City Assistant",
    page_icon="🌍",
    layout="centered"
)


st.title("🌍 AI City Assistant")

st.write(
    "Get current weather and latest news for any city."
)


city = st.text_input(
    "Enter city name",
    placeholder="e.g. Noida"
)


if st.button("Search", type="primary"):

    if not city.strip():

        st.warning("Please enter a city.")

    else:

        with st.spinner("Fetching information..."):

            weather = get_weather.invoke({
                "city": city
            })

            news = get_news.invoke({
                "city": city
            })


        st.subheader("🌤️ Current Weather")

        st.info(weather)


        st.subheader("📰 Latest News")

        st.markdown(news)