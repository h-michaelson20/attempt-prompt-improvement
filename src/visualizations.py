import plotly.express as px
import plotly.graph_objects as go

def create_histogram(df, column):
    """Create histogram for numeric data"""
    fig = px.histogram(df, x=column, title=f"Distribution of {column}")
    return fig

def create_bar_chart(df, x_col, y_col):
    """Create bar chart"""
    fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
    return fig

def create_scatter_plot(df, x_col, y_col):
    """Create scatter plot"""
    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    return fig 