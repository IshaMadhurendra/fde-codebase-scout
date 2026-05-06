import plotly.graph_objects as go
import streamlit as st


def render_health_gauge(score: int):
    """Render a Plotly gauge chart for the health score."""
    if score >= 70:
        bar_color = "#4ADE80"
    elif score >= 40:
        bar_color = "#FFB020"
    else:
        bar_color = "#FF4D4D"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 46, "color": "#F5F0EB", "family": "DM Mono, monospace"}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(207, 173, 153, 0.1)",
                "tickfont": {"color": "#6B6560", "family": "DM Mono, monospace", "size": 10},
            },
            "bar": {"color": bar_color, "thickness": 0.22},
            "bgcolor": "rgba(207, 173, 153, 0.04)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(255, 77, 77, 0.06)"},
                {"range": [40, 70], "color": "rgba(255, 176, 32, 0.06)"},
                {"range": [70, 100], "color": "rgba(74, 222, 128, 0.06)"},
            ],
            "threshold": {
                "line": {"color": bar_color, "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
        title={"text": "HEALTH SCORE", "font": {"size": 10, "color": "#6B6560", "family": "DM Mono, monospace"}},
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=240,
        margin=dict(l=20, r=20, t=50, b=10),
        font={"family": "DM Mono, monospace"},
    )

    st.plotly_chart(fig, use_container_width=True)
