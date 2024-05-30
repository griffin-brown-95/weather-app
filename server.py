from flask import Flask, render_template, request
from weather import get_coord, get_baseline, get_forecast, plot_temperature_trends, show_weather_details_table
from waitress import serve
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET'])
def get_forecast_view():
    zip_code = request.args.get('zip_code')
    if not zip_code:
        return render_template('index.html', error="Please enter a ZIP code.")
    
    try:
        lat, lon = get_coord(zip_code)
        forecast_url = get_baseline(lat, lon)
        if forecast_url:
            weather_df = get_forecast(forecast_url)
            if not weather_df.empty:
                temp_trend_img = plot_temperature_trends(weather_df)
                temp_trend_table = show_weather_details_table(weather_df)
                return render_template('results.html', 
                                       zip_code=zip_code,
                                       weather_df=weather_df.to_html(classes='table table-striped', index=False), 
                                       temp_trend_img=temp_trend_img, 
                                       temp_trend_table=temp_trend_table)
            else:
                error = "No forecast data available."
        else:
            error = "Unable to retrieve the forecast URL."
    except ValueError as e:
        error = str(e)
    
    return render_template('index.html', error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    serve(app, host="0.0.0.0", port=port)
