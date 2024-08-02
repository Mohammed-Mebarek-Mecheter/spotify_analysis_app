# src/trend_analysis.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def trend_analysis(data):
    st.header("Trend Analysis")

    # Time Series Chart using Plotly
    st.subheader("Song Releases Over Time")
    monthly_releases = data['Release Date'].dt.to_period('M').value_counts().sort_index().reset_index()
    monthly_releases.columns = ['Month', 'Count']
    monthly_releases['Month'] = monthly_releases['Month'].dt.strftime('%Y-%m')

    fig = go.Figure(data=go.Scatter(
        x=monthly_releases['Month'],
        y=monthly_releases['Count'],
        mode='lines',
        hovertext=monthly_releases['Count'],
        hovertemplate='Month: %{x}<br>Count: %{y}',
        line=dict(width=3, color='#1DB954')
    ))
    fig.update_layout(
        title='Song Releases Over Time',
        xaxis_title='Month',
        yaxis_title='Count'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap by Month and Day of Week using Plotly
    st.subheader("Heatmap of Song Releases")
    data['Month'] = data['Release Date'].dt.month
    data['Day of Week'] = data['Release Date'].dt.dayofweek

    heatmap_data = data.groupby(['Month', 'Day of Week']).size().reset_index(name='Count')
    heatmap_data = heatmap_data.pivot(index='Month', columns='Day of Week', values='Count')

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        hovertext=heatmap_data.values,
        hovertemplate='Month: %{y}<br>Day of Week: %{x}<br>Count: %{z}'
    ))
    fig.update_layout(
        title='Heatmap of Song Releases',
        xaxis_title='Day of Week',
        yaxis_title='Month'
    )
    st.plotly_chart(fig, use_container_width=True)
