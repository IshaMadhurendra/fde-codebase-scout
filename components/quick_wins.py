import streamlit as st


def render_quick_wins(quick_wins: list):
    """Render prioritized quick wins with impact/effort badges."""
    # Sort by impact
    impact_order = {"Critical": 0, "High": 1, "Medium": 2}
    sorted_wins = sorted(quick_wins, key=lambda x: impact_order.get(x.get("impact", "Medium"), 2))

    total_sp = sum(w.get("effort_sp", 0) for w in sorted_wins)
    critical_count = sum(1 for w in sorted_wins if w.get("impact") == "Critical")
    high_count = sum(1 for w in sorted_wins if w.get("impact") == "High")

    # Summary stats
    cols = st.columns(4)
    stats = [
        ("ITEMS", len(sorted_wins), "#FF8C42"),
        ("TOTAL SP", total_sp, "#FFB020"),
        ("CRITICAL", critical_count, "#FF4D4D"),
        ("HIGH", high_count, "#FFCF44"),
    ]
    for col, (label, value, color) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.1); border-radius: 12px; padding: 22px; text-align: center;">
                <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.1em; margin-bottom: 10px;">{label}</div>
                <div style="color: {color}; font-size: 28px; font-weight: 600; font-family: 'DM Mono', monospace;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 22px'></div>", unsafe_allow_html=True)

    # Render each quick win
    for win in sorted_wins:
        impact = win.get("impact", "Medium")
        if impact == "Critical":
            impact_color = "#FF4D4D"
        elif impact == "High":
            impact_color = "#FFB020"
        else:
            impact_color = "#FF8C42"

        risk = win.get("risk", "Low")
        if risk == "High":
            risk_color = "#FF4D4D"
        elif risk == "Medium":
            risk_color = "#FFB020"
        else:
            risk_color = "#4ADE80"

        category = win.get("category", "general")

        with st.expander(f"{win['title']}"):
            st.markdown(f"""
            <div style="display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;">
                <span style="background: {impact_color}30; color: {impact_color}; padding: 5px 12px; border-radius: 6px; font-size: 10px; font-weight: 700; font-family: 'DM Mono', monospace; letter-spacing: 0.03em; border: 1px solid {impact_color}40;">{impact}</span>
                <span style="background: rgba(255, 176, 32, 0.15); color: #FFB020; padding: 5px 12px; border-radius: 6px; font-size: 10px; font-weight: 700; font-family: 'DM Mono', monospace; border: 1px solid rgba(255, 176, 32, 0.3);">{win.get('effort_sp', '?')} SP</span>
                <span style="background: {risk_color}30; color: {risk_color}; padding: 5px 12px; border-radius: 6px; font-size: 10px; font-weight: 700; font-family: 'DM Mono', monospace; border: 1px solid {risk_color}40;">{risk} risk</span>
                <span style="background: rgba(207, 173, 153, 0.12); color: #CFAD99; padding: 5px 12px; border-radius: 6px; font-size: 10px; font-weight: 500; font-family: 'DM Mono', monospace; border: 1px solid rgba(207, 173, 153, 0.2);">{category}</span>
            </div>
            <p style="color: #9C9488; font-family: 'DM Sans', sans-serif; font-size: 13px; line-height: 1.7; margin: 0;">{win.get('description', '')}</p>
            """, unsafe_allow_html=True)
