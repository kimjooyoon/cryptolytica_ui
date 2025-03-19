import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Union, Tuple

def create_line_chart(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    title: str = "",
    height: int = 400,
    color_discrete_map: Dict[str, str] = None
) -> go.Figure:
    """
    선 차트를 생성합니다.
    
    Args:
        df: 데이터프레임
        x_column: X축 컬럼명 
        y_columns: Y축 컬럼명 목록
        title: 차트 제목
        height: 차트 높이
        color_discrete_map: 시리즈별 색상 맵
        
    Returns:
        go.Figure: Plotly 차트 객체
    """
    fig = go.Figure()
    
    for y_column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=df[x_column],
                y=df[y_column],
                mode='lines',
                name=y_column
            )
        )
    
    fig.update_layout(
        title=title,
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )
    
    return fig

def create_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "",
    height: int = 400,
    color: str = None
) -> go.Figure:
    """
    막대 차트를 생성합니다.
    
    Args:
        df: 데이터프레임
        x_column: X축 컬럼명
        y_column: Y축 컬럼명
        title: 차트 제목
        height: 차트 높이
        color: 막대 색상
        
    Returns:
        go.Figure: Plotly 차트 객체
    """
    fig = px.bar(
        df,
        x=x_column,
        y=y_column,
        title=title,
        height=height,
        color_discrete_sequence=[color] if color else None
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )
    
    return fig

def create_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    size_column: str = None,
    color_column: str = None,
    title: str = "",
    height: int = 400
) -> go.Figure:
    """
    산점도를 생성합니다.
    
    Args:
        df: 데이터프레임
        x_column: X축 컬럼명
        y_column: Y축 컬럼명
        size_column: 점 크기 컬럼명
        color_column: 점 색상 컬럼명
        title: 차트 제목
        height: 차트 높이
        
    Returns:
        go.Figure: Plotly 차트 객체
    """
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        size=size_column,
        color=color_column,
        title=title,
        height=height
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="closest"
    )
    
    return fig

def create_heatmap(
    df: pd.DataFrame,
    title: str = "",
    height: int = 400,
    color_scale: str = "Viridis"
) -> go.Figure:
    """
    히트맵을 생성합니다.
    
    Args:
        df: 데이터프레임 (행과 열의 인덱스가 축으로 사용됨)
        title: 차트 제목
        height: 차트 높이
        color_scale: 색상 스케일
        
    Returns:
        go.Figure: Plotly 차트 객체
    """
    fig = px.imshow(
        df,
        title=title,
        height=height,
        color_continuous_scale=color_scale
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_pie_chart(
    df: pd.DataFrame,
    names_column: str,
    values_column: str,
    title: str = "",
    height: int = 400
) -> go.Figure:
    """
    파이 차트를 생성합니다.
    
    Args:
        df: 데이터프레임
        names_column: 레이블 컬럼명
        values_column: 값 컬럼명
        title: 차트 제목
        height: 차트 높이
        
    Returns:
        go.Figure: Plotly 차트 객체
    """
    fig = px.pie(
        df,
        names=names_column,
        values=values_column,
        title=title,
        height=height
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_candlestick_chart(
    df: pd.DataFrame,
    x_column: str,
    open_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    title: str = "",
    height: int = 500
) -> go.Figure:
    """
    캔들스틱 차트를 생성합니다.
    
    Args:
        df: 데이터프레임
        x_column: X축 컬럼명 (날짜/시간)
        open_column: 시가 컬럼명
        high_column: 고가 컬럼명
        low_column: 저가 컬럼명
        close_column: 종가 컬럼명
        title: 차트 제목
        height: 차트 높이
        
    Returns:
        go.Figure: Plotly 차트 객체
    """
    fig = go.Figure(data=[go.Candlestick(
        x=df[x_column],
        open=df[open_column],
        high=df[high_column],
        low=df[low_column],
        close=df[close_column]
    )])
    
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_rangeslider_visible=False
    )
    
    return fig

def create_multi_chart(
    charts: List[go.Figure],
    rows: int = None,
    cols: int = None,
    title: str = "",
    height: int = 800
) -> go.Figure:
    """
    여러 차트를 하나의 그림으로 결합합니다.
    
    Args:
        charts: 차트 객체 목록
        rows: 행 수 (None이면 자동 계산)
        cols: 열 수 (None이면 자동 계산)
        title: 차트 제목
        height: 차트 높이
        
    Returns:
        go.Figure: Plotly 차트 객체
    """
    from plotly.subplots import make_subplots
    
    n_charts = len(charts)
    
    if rows is None and cols is None:
        # 행과 열 수 자동 계산
        import math
        cols = min(3, n_charts)  # 최대 3열
        rows = math.ceil(n_charts / cols)
    elif rows is None:
        # 행 수 자동 계산
        rows = math.ceil(n_charts / cols)
    elif cols is None:
        # 열 수 자동 계산
        cols = math.ceil(n_charts / rows)
    
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[chart.layout.title.text for chart in charts]
    )
    
    for i, chart in enumerate(charts):
        row = i // cols + 1
        col = i % cols + 1
        
        for trace in chart.data:
            fig.add_trace(trace, row=row, col=col)
    
    fig.update_layout(
        title=title,
        height=height,
        showlegend=False
    )
    
    return fig 