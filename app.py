import streamlit as st
from weather import get_coord, get_baseline, get_forecast, plot_temperature_trends, show_weather_details_table

st.title("Weather Forecast")

zip_code = st.text_input("Enter your ZIP code (XXXXX):")

if st.button("Get Forecast"):
    if zip_code:
        try:
            lat, lon = get_coord(zip_code)
            forecast_url = get_baseline(lat, lon)
            if forecast_url:
                weather_df = get_forecast(forecast_url)
                if not weather_df.empty:
                    st.write("## Temperature Trends")
                    plot_temperature_trends(weather_df)

                    st.write('## Weather Details')
                    weather_details = show_weather_details_table(weather_df)
                    st.dataframe(weather_details)
                else:
                    st.error("No forecast data available.")
            else:
                st.error("Unable to retrieve the forecast URL.")
        except ValueError as e:
            st.error(str(e))
    else:
        st.error("Please enter a ZIP code.")
