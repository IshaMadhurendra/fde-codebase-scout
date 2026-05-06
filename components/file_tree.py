import streamlit as st


def _count_files(tree: dict) -> int:
    """Count total files in a tree dict."""
    count = 0
    for value in tree.values():
        if value is None:
            count += 1
        elif isinstance(value, dict):
            count += _count_files(value)
    return count


def _render_tree_text(tree: dict, prefix: str = "") -> str:
    """Render tree as text with tree characters."""
    lines = []
    items = list(tree.items())
    for i, (key, value) in enumerate(items):
        is_last = i == len(items) - 1
        connector = "&#9492;&#9472;&#9472; " if is_last else "&#9500;&#9472;&#9472; "
        extension = "    " if is_last else "&#9474;   "

        if value is None:
            lines.append(f'<span style="color: #3D3833;">{prefix}{connector}</span><span style="color: #9C9488;">{key}</span>')
        elif isinstance(value, dict):
            file_count = _count_files(value)
            lines.append(f'<span style="color: #3D3833;">{prefix}{connector}</span><span style="color: #CFAD99; font-weight: 500;">{key}</span> <span style="color: #3D3833;">({file_count})</span>')
            sub = _render_tree_text(value, prefix + extension)
            if sub:
                lines.append(sub)
        else:
            lines.append(f'<span style="color: #3D3833;">{prefix}{connector}</span><span style="color: #9C9488;">{key}</span>')

    return "\n".join(lines)


def render_file_tree(file_tree: dict):
    """Render file tree visualization."""
    total_files = _count_files(file_tree)

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 18px;">
        <span style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;">File Structure</span>
        <span style="color: #3D3833;">&#183;</span>
        <span style="color: #CFAD99; font-family: 'DM Mono', monospace; font-size: 11px; font-weight: 500;">{total_files} files</span>
    </div>
    """, unsafe_allow_html=True)

    tree_text = _render_tree_text(file_tree)
    st.markdown(f"""
    <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.08); border-radius: 12px; padding: 22px; font-family: 'DM Mono', monospace; font-size: 12px; line-height: 1.9; white-space: pre; overflow-x: auto;">
{tree_text}
    </div>
    """, unsafe_allow_html=True)
