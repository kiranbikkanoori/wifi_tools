import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import pandas as pd
from plotly_resampler import FigureResampler
# Read the CSV file into a DataFrame
df = pd.read_csv('GPIO_relative_time.csv')
# Access columns by their names
Timestamp = df['Timestamp']
RelativeTS = df['RelativeTS']
LogicData = df['LogicData']
Width_in_us = df['Width_in_us']

# Create traces for the first chart
data1 = []
for i, start_time in enumerate(RelativeTS):
    data1.append(go.Bar(
        x=[start_time + Width_in_us[i]/2],  # Set the relative start time in us for each bar
        y=[LogicData[i]*20 + 0.5],
        width=Width_in_us[i],  # Convert width to milliseconds
        hoverinfo='y+text',  # Display y value and text on hover
        text=f'Value: {Width_in_us[i]} {i}',
        marker=dict(color='steelblue', opacity=0.8),  # Bar color
        showlegend=False  # Remove legend for this trace
    ))

# Create traces for the second chart
data2 = []
for i, start_time in enumerate(RelativeTS):
    data2.append(go.Bar(
        x=[start_time + Width_in_us[i]/2],  # Set the relative start time in us for each bar
        y=[LogicData[i]*20 + 0.5],
        width=Width_in_us[i],  # Convert width to milliseconds
        hoverinfo='y+text',  # Display y value and text on hover
        text=f'Value: {Width_in_us[i]} {i}',
        marker=dict(color='steelblue', opacity=0.8),  # Bar color
        showlegend=False  # Remove legend for this trace
    ))

# Create subplot with shared x-axis
# fig = FigureResampler(make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Data 1", "Data 2")))
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Data 1", "Data 2"))


# Add traces to the subplot
for trace in data1:
    fig.add_trace(trace, row=1, col=1)

for trace in data2:
    fig.add_trace(trace, row=2, col=1)

# Update layout
fig.update_layout(
    title='Variable Width Bar Charts with Hover Data on Timeline',
    xaxis=dict(
        title='Time',
        # type='data',
        # rangeselector=dict(
        #     buttons=list([
        #         dict(count=1, label="1m", step="month", stepmode="backward"),
        #         dict(count=6, label="6m", step="month", stepmode="backward"),
        #         dict(count=1, label="YTD", step="year", stepmode="todate"),
        #         dict(count=1, label="1y", step="year", stepmode="backward"),
        #         dict(step="all")
        #     ])
        # ),
    ),
    yaxis=dict(
        title='Values',
        fixedrange=True  # Fix y-axis range
    ),
    xaxis2=dict(  # X-axis for the second subplot
        title='Time',
        # type='date',
        rangeslider=dict(  # Add range slider for x-axis
            visible=True
        ),
        # tickformat='%Y-%m-%d %H:%M:%S.%f',  # Display milliseconds
        # dtick=1000,  # Set x-axis tick interval to 1
    ),
    # Configure click event handler
    clickmode='event+select',
    # Define JavaScript function to handle click events
    # Add custom button to mode bar
    modebar=dict(
        add=[
            dict(
                name='Click Handler',
                icon='circle',
                click='function(gd) { console.log(gd); alert("Clicked on a bar!"); }'
            )
        ]
    ),
)

# Show plot
# fig.show_dash(mode='inline')
fig.show()