import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def filter_dates(df, period):
    today = datetime.today()
    if period == '1 week':
        past_date = today - timedelta(weeks=1)
    elif period == '1 month':
        past_date = today - timedelta(weeks=4)
    elif period == '3 months':
        past_date = today - timedelta(weeks=13)
    elif period == '6 months':
        past_date = today - timedelta(weeks=26)
    elif period == '1 year':
        past_date = today - timedelta(weeks=52)
    elif period == '3 years':
        past_date = today - timedelta(weeks=156)
    else: # All time
        past_date = df['date'].min()

    return df[df['date'] >= past_date]

def app():
    st.title('Data visualization app')
    file = st.file_uploader('Upload your csv file', type=['csv'])

    if file is not None:
        data = pd.read_csv(file)
        data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
        data = data.sort_values(by='date')
        period = st.selectbox(
            'Select period',
            ['1 week', '1 month', '3 months', '6 months', '1 year', '3 years', 'All time']
        )
        filtered_data = filter_dates(data, period)
        
        # Create a line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['kg'], 
                                 mode='lines+markers', 
                                 name='lines+markers',
                                 line=dict(color='limegreen'),
                                 marker=dict(color='limegreen'),
                                 fill='tozeroy',
                                 fillcolor='rgba(50, 205, 50, 0.5)'))  # Limegreen with 50% transparency
        
        # Add 7-day moving average line if selected
        show_moving_average = st.checkbox('Show 7-day moving average')
        if show_moving_average:
            data['7_day_avg'] = data['kg'].rolling(window=7).mean()
            filtered_average_data = filter_dates(data, period)
            fig.add_trace(go.Scatter(x=filtered_average_data['date'], y=filtered_average_data['7_day_avg'], 
                                     mode='lines', 
                                     name='7-day moving average',
                                     line=dict(color='red')))
        
        # Set y-axis range
        ymin, ymax = st.slider('Set y-axis range', min_value=0, max_value=100, value=(60,80))
        fig.update_yaxes(range=[ymin, ymax])
        
        # Update layout
        fig.update_layout(
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="black"
            ),
            plot_bgcolor='white',
            xaxis_showgrid=True, 
            yaxis_showgrid=True, 
            xaxis_ticks="inside", 
            yaxis_ticks="inside",
            xaxis_linecolor='black',
            yaxis_linecolor='black',
            xaxis_title="Date",
            yaxis_title="Weight (kg)"
        )
        
        st.plotly_chart(fig)

if __name__ == '__main__':
    app()
