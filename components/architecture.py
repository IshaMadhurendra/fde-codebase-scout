import streamlit as st
import base64


def render_architecture(architecture: list, mermaid_diagram: str):
    """Render architecture breakdown cards and mermaid diagram."""
    st.markdown("""
    <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 20px;">Architecture Layers</div>
    """, unsafe_allow_html=True)

    cols = st.columns(min(len(architecture), 3))
    for i, layer in enumerate(architecture):
        col = cols[i % 3]
        with col:
            status = layer.get("status", "ok")
            if status == "ok":
                status_color = "#4ADE80"
                status_label = "HEALTHY"
            elif status == "warn":
                status_color = "#FFB020"
                status_label = "WARNING"
            else:
                status_color = "#FF4D4D"
                status_label = "CRITICAL"

            st.markdown(f"""
            <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.1); border-radius: 12px; padding: 22px; margin-bottom: 14px; min-height: 180px; transition: all 0.2s ease;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                    <span style="color: #F5F0EB; font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 14px;">{layer['layer']}</span>
                    <span style="color: {status_color}; font-family: 'DM Mono', monospace; font-size: 9px; font-weight: 700; letter-spacing: 0.05em; background: {status_color}25; padding: 5px 10px; border-radius: 5px; border: 1px solid {status_color}40;">{status_label}</span>
                </div>
                <div style="background: rgba(207, 173, 153, 0.05); border-radius: 7px; padding: 9px 13px; margin-bottom: 14px; border: 1px solid rgba(207, 173, 153, 0.06);">
                    <span style="color: #CFAD99; font-size: 12px; font-family: 'DM Mono', monospace;">{layer['tech']}</span>
                </div>
                <p style="color: #9C9488; font-family: 'DM Sans', sans-serif; font-size: 12px; margin: 0; line-height: 1.6;">{layer['notes']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Mermaid diagram
    st.markdown("""
    <div style="height: 36px;"></div>
    <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 20px;">System Diagram</div>
    """, unsafe_allow_html=True)

    if mermaid_diagram:
        try:
            from streamlit_mermaid import st_mermaid
            st_mermaid(mermaid_diagram)
        except ImportError:
            # Fallback: render via mermaid.ink
            diagram_encoded = base64.urlsafe_b64encode(mermaid_diagram.encode("utf-8")).decode("utf-8")
            img_url = f"https://mermaid.ink/img/{diagram_encoded}"
            st.image(img_url, use_container_width=True)
            with st.expander("Mermaid Source"):
                st.code(mermaid_diagram, language="mermaid")
