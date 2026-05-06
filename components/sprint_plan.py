import plotly.graph_objects as go
import streamlit as st


def render_sprint_plan(onboarding_plan: list):
    """Render sprint plan cards and velocity chart."""
    st.markdown("""
    <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 20px;">Onboarding Sprint Plan</div>
    """, unsafe_allow_html=True)

    # Week cards
    for i, week in enumerate(onboarding_plan):
        # Warm accent shades
        accents = ["#CFAD99", "#B8977F", "#A68B76", "#8D7566"]
        accent = accents[i % len(accents)]

        st.markdown(f"""
        <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.1); border-left: 3px solid {accent}; border-radius: 10px; padding: 20px 22px; margin-bottom: 12px; transition: all 0.2s ease;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="color: #F5F0EB; font-family: 'DM Mono', monospace; font-weight: 500; font-size: 13px;">{week['week']}</span>
                <span style="color: #FFB020; font-family: 'DM Mono', monospace; font-size: 11px; font-weight: 700; background: rgba(255, 176, 32, 0.15); padding: 5px 12px; border-radius: 6px; border: 1px solid rgba(255, 176, 32, 0.3);">{week['story_points']} SP</span>
            </div>
            <div style="color: #D4CBC2; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; margin-bottom: 8px;">{week['focus']}</div>
            <p style="color: #6B6560; font-family: 'DM Sans', sans-serif; font-size: 12px; margin: 0; line-height: 1.6;">{week['tasks']}</p>
        </div>
        """, unsafe_allow_html=True)

    total_sp = sum(w.get("story_points", 0) for w in onboarding_plan)
    st.markdown(f"""
    <div style="background: rgba(207, 173, 153, 0.05); border: 1px solid rgba(207, 173, 153, 0.15); border-radius: 10px; padding: 16px 22px; margin: 22px 0; text-align: center;">
        <span style="color: #9C9488; font-family: 'DM Sans', sans-serif; font-size: 12px;">Total Commitment: </span>
        <span style="color: #CFAD99; font-size: 18px; font-weight: 600; font-family: 'DM Mono', monospace;">{total_sp} SP</span>
    </div>
    """, unsafe_allow_html=True)

    # Velocity chart
    st.markdown("""
    <div style="height: 28px;"></div>
    <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 20px;">Velocity Chart</div>
    """, unsafe_allow_html=True)

    weeks = [w["week"] for w in onboarding_plan]
    sps = [w["story_points"] for w in onboarding_plan]
    cumulative = []
    running = 0
    for sp in sps:
        running += sp
        cumulative.append(running)

    # Warm gradient from cream to deeper tan
    colors = []
    n = len(weeks)
    for i in range(n):
        ratio = i / max(n - 1, 1)
        r = int(207 + ratio * (141 - 207))
        g = int(173 + ratio * (117 - 173))
        b = int(153 + ratio * (102 - 153))
        colors.append(f"rgb({r}, {g}, {b})")

    fig = go.Figure()

    # Bar chart
    fig.add_trace(go.Bar(
        x=weeks,
        y=sps,
        marker_color=colors,
        marker_line_width=0,
        name="Story Points",
        text=sps,
        textposition="outside",
        textfont={"color": "#9C9488", "size": 12, "family": "DM Mono, monospace"},
    ))

    # Cumulative line
    fig.add_trace(go.Scatter(
        x=weeks,
        y=cumulative,
        mode="lines+markers",
        name="Cumulative",
        line={"color": "#D4A84B", "width": 2},
        marker={"size": 6, "color": "#D4A84B"},
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=40, r=20, t=20, b=40),
        xaxis={
            "color": "#6B6560",
            "gridcolor": "rgba(207, 173, 153, 0.06)",
            "tickfont": {"family": "DM Mono, monospace", "size": 11},
        },
        yaxis={
            "color": "#6B6560",
            "gridcolor": "rgba(207, 173, 153, 0.06)",
            "title": {"text": "SP", "font": {"family": "DM Mono, monospace", "size": 11, "color": "#6B6560"}},
            "tickfont": {"family": "DM Mono, monospace", "size": 10},
        },
        legend={
            "font": {"color": "#9C9488", "family": "DM Sans, sans-serif", "size": 11},
            "bgcolor": "rgba(0,0,0,0)",
        },
        showlegend=True,
        bargap=0.35,
    )

    st.plotly_chart(fig, use_container_width=True)
