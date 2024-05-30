def show_weather_details(weather_df):
    weather_df['Day/Night'] = weather_df['Day Time'].apply(lambda x: 'Day' if x else 'Night')
    weather_df['Date'] = pd.to_datetime(weather_df['Date']).dt.strftime('%m/%d/%Y')

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(weather_df[['Date', 'Day/Night', 'Short Forecast', 'Detailed Forecast']].columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[weather_df['Date'], weather_df['Day/Night'], weather_df['Short Forecast'], weather_df['Detailed Forecast']],
                fill_color='lightblue',
                align='left'))
    ])
    fig.update_layout(title='Weather Forecast', title_x=0.5)
    fig.show()