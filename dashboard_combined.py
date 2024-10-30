from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd

app = Dash(__name__, server=True)

app.layout = html.Div([
    html.H1("Fraud and Credit Card Fraud Detection Dashboard"),

    # Summary boxes
    html.Div(id='fraud-summary', style={'display': 'inline-block', 'width': '45%', 'margin': '10px'}),
    html.Div(id='credit-summary', style={'display': 'inline-block', 'width': '45%', 'margin': '10px'}),

    # Trends over time
    html.H2("Fraud Trends Over Time"),
    dcc.Graph(id='fraud-trend-chart'),
    dcc.Graph(id='credit-trend-chart'),

    # Geographic and device/browser analysis
    html.H2("Device and Browser Analysis for Fraud Cases"),
    dcc.Graph(id='fraud-device-chart'),
    dcc.Graph(id='fraud-browser-chart'),

    # Auto-refresh interval
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0)
])

# Summary Boxes for Fraud Data
@app.callback(Output('fraud-summary', 'children'), Input('interval-component', 'n_intervals'))
def update_fraud_summary(n):
    data = requests.get("http://192.168.0.100:5000/fraud_summary").json()
    return [
        html.H3("Fraud Detection Summary"),
        html.P(f"Total Transactions: {data['total_transactions']}"),
        html.P(f"Fraud Cases: {data['fraud_cases']}"),
        html.P(f"Fraud Percentage: {data['fraud_percentage']:.2f}%")
    ]

# Summary Boxes for Credit Card Data
@app.callback(Output('credit-summary', 'children'), Input('interval-component', 'n_intervals'))
def update_credit_summary(n):
    data = requests.get("http://192.168.0.100:5000/credit_summary").json()
    return [
        html.H3("Credit Card Fraud Detection Summary"),
        html.P(f"Total Transactions: {data['total_transactions']}"),
        html.P(f"Fraud Cases: {data['fraud_cases']}"),
        html.P(f"Fraud Percentage: {data['fraud_percentage']:.2f}%")
    ]

# Trend Chart for Fraud Data
@app.callback(Output('fraud-trend-chart', 'figure'), Input('interval-component', 'n_intervals'))
def update_fraud_trends(n):
    data = requests.get("http://192.168.0.100:5000/fraud_trends").json()
    return {
        'data': [{'x': list(data.keys()), 'y': list(data.values()), 'type': 'line', 'name': 'Fraud Cases'}],
        'layout': {'title': 'Fraud Cases Over Time'}
    }

# Trend Chart for Credit Card Data
@app.callback(Output('credit-trend-chart', 'figure'), Input('interval-component', 'n_intervals'))
def update_credit_trends(n):
    data = requests.get("http://192.168.0.100:5000/credit_trends").json()
    return {
        'data': [{'x': list(data.keys()), 'y': list(data.values()), 'type': 'line', 'name': 'Credit Fraud Cases'}],
        'layout': {'title': 'Credit Fraud Cases Over Time'}
    }

# Device Analysis Chart
@app.callback(Output('fraud-device-chart', 'figure'), Input('interval-component', 'n_intervals'))
def update_fraud_device_chart(n):
    data = requests.get("http://192.168.0.100:5000/fraud_device_browser").json()
    return {
        'data': [{'x': list(data['device_counts'].keys()), 'y': list(data['device_counts'].values()), 'type': 'bar', 'name': 'Device Fraud Cases'}],
        'layout': {'title': 'Fraud Cases by Device'}
    }

# Browser Analysis Chart
@app.callback(Output('fraud-browser-chart', 'figure'), Input('interval-component', 'n_intervals'))
def update_fraud_browser_chart(n):
    data = requests.get("http://192.168.0.100:5000/fraud_device_browser").json()
    return {
        'data': [{'x': list(data['browser_counts'].keys()), 'y': list(data['browser_counts'].values()), 'type': 'bar', 'name': 'Browser Fraud Cases'}],
        'layout': {'title': 'Fraud Cases by Browser'}
    }

if __name__ == "__main__":
    app.run_server(debug=True)
