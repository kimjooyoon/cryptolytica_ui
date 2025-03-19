import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

def create_candlestick_chart(data: pd.DataFrame, title: str = "가격 차트") -> go.Figure:
    """
    캔들스틱 차트를 생성합니다.
    
    Args:
        data: timestamp, open, high, low, close, volume 컬럼이 있는 DataFrame
        title: 차트 제목
    
    Returns:
        plotly Figure 객체
    """
    fig = go.Figure()
    
    # 캔들스틱 차트 추가
    fig.add_trace(
        go.Candlestick(
            x=data['timestamp'],
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            name="가격"
        )
    )
    
    # 거래량 차트 추가
    fig.add_trace(
        go.Bar(
            x=data['timestamp'],
            y=data['volume'],
            name="거래량",
            marker_color='rgba(128, 128, 128, 0.5)',
            yaxis="y2"
        )
    )
    
    # 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_title="시간",
        yaxis_title="가격",
        yaxis2=dict(
            title="거래량",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=600,
        template="plotly_white"
    )
    
    return fig

def create_line_chart(data: pd.DataFrame, x_column: str, y_columns: List[str], 
                      title: str = "라인 차트", colors: Optional[List[str]] = None) -> go.Figure:
    """
    여러 시계열 데이터를 라인 차트로 시각화합니다.
    
    Args:
        data: 데이터가 포함된 DataFrame
        x_column: x축에 사용할 컬럼 이름
        y_columns: y축에 표시할 컬럼 이름 목록
        title: 차트 제목
        colors: 각 라인의 색상 목록 (옵션)
    
    Returns:
        plotly Figure 객체
    """
    fig = go.Figure()
    
    if colors is None:
        colors = px.colors.qualitative.Plotly
    
    for i, column in enumerate(y_columns):
        color = colors[i % len(colors)]
        fig.add_trace(
            go.Scatter(
                x=data[x_column],
                y=data[column],
                mode='lines',
                name=column,
                line=dict(color=color)
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title=x_column,
        yaxis_title="값",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
        template="plotly_white"
    )
    
    return fig

def create_pie_chart(labels: List[str], values: List[float], title: str = "파이 차트") -> go.Figure:
    """
    파이 차트를 생성합니다.
    
    Args:
        labels: 각 섹션의 레이블
        values: 각 섹션의 값
        title: 차트 제목
    
    Returns:
        plotly Figure 객체
    """
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo='percent+label',
                insidetextorientation='radial'
            )
        ]
    )
    
    fig.update_layout(
        title=title,
        height=400,
        template="plotly_white"
    )
    
    return fig

def create_bar_chart(data: pd.DataFrame, x_column: str, y_column: str, 
                     title: str = "막대 차트", color: Optional[str] = None) -> go.Figure:
    """
    막대 차트를 생성합니다.
    
    Args:
        data: 데이터가 포함된 DataFrame
        x_column: x축에 사용할 컬럼 이름
        y_column: y축에 표시할 컬럼 이름
        title: 차트 제목
        color: 막대 색상 (옵션)
    
    Returns:
        plotly Figure 객체
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=data[x_column],
            y=data[y_column],
            marker_color=color or 'rgb(55, 83, 109)'
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=x_column,
        yaxis_title=y_column,
        height=500,
        template="plotly_white"
    )
    
    return fig

def create_heatmap(data: pd.DataFrame, x_labels: List[str], y_labels: List[str],
                   title: str = "히트맵") -> go.Figure:
    """
    히트맵을 생성합니다.
    
    Args:
        data: 히트맵 데이터 (2D 배열)
        x_labels: x축 레이블
        y_labels: y축 레이블
        title: 차트 제목
    
    Returns:
        plotly Figure 객체
    """
    fig = go.Figure(
        data=go.Heatmap(
            z=data.values,
            x=x_labels,
            y=y_labels,
            colorscale='Viridis',
            hoverongaps=False
        )
    )
    
    fig.update_layout(
        title=title,
        height=500,
        template="plotly_white"
    )
    
    return fig

def create_scatter_plot(data: pd.DataFrame, x_column: str, y_column: str, 
                        color_column: Optional[str] = None, size_column: Optional[str] = None,
                        title: str = "산점도") -> go.Figure:
    """
    산점도를 생성합니다.
    
    Args:
        data: 데이터가 포함된 DataFrame
        x_column: x축에 사용할 컬럼 이름
        y_column: y축에 표시할 컬럼 이름
        color_column: 색상에 사용할 컬럼 이름 (옵션)
        size_column: 크기에 사용할 컬럼 이름 (옵션)
        title: 차트 제목
    
    Returns:
        plotly Figure 객체
    """
    fig = px.scatter(
        data,
        x=x_column,
        y=y_column,
        color=color_column,
        size=size_column,
        title=title,
        height=500,
        template="plotly_white"
    )
    
    return fig

def create_correlation_matrix(data: pd.DataFrame, title: str = "상관관계 매트릭스") -> go.Figure:
    """
    상관관계 매트릭스를 생성합니다.
    
    Args:
        data: 수치형 데이터가 포함된 DataFrame
        title: 차트 제목
    
    Returns:
        plotly Figure 객체
    """
    # 수치형 컬럼만 선택
    numeric_data = data.select_dtypes(include=[np.number])
    
    # 상관관계 계산
    corr = numeric_data.corr()
    
    # 히트맵 생성
    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            hoverongaps=False
        )
    )
    
    # 레이아웃 설정
    fig.update_layout(
        title=title,
        height=600,
        template="plotly_white"
    )
    
    return fig

def create_gauge_chart(value: float, min_value: float, max_value: float, 
                       title: str = "게이지 차트", threshold_values: Optional[List[float]] = None) -> go.Figure:
    """
    게이지 차트를 생성합니다.
    
    Args:
        value: 표시할 값
        min_value: 최소값
        max_value: 최대값
        title: 차트 제목
        threshold_values: 임계값 목록 (옵션)
    
    Returns:
        plotly Figure 객체
    """
    if threshold_values is None:
        threshold_values = [0.3, 0.7]  # 기본 임계값
    
    # 임계값에 따른 색상 구간 설정
    colors = ['red', 'yellow', 'green', 'yellow', 'red']
    thresholds = [min_value] + threshold_values + [max_value]
    
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            gauge={
                'axis': {'range': [min_value, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [thresholds[i], thresholds[i+1]], 'color': colors[i]} 
                    for i in range(len(thresholds)-1)
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9  # 경고 임계값
                }
            }
        )
    )
    
    fig.update_layout(
        height=300,
        template="plotly_white"
    )
    
    return fig 