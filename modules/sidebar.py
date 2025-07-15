# modules/sidebar.py

import streamlit as st

def render_sidebar():
    # === Custom Sidebar Style ===
    custom_style = """
        <style>
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            [data-testid="stSidebar"] {
                background-color: #111827;
                padding: 1rem;
                width: 220px;
            }
        </style>
    """
    st.markdown(custom_style, unsafe_allow_html=True)

    # === Sidebar Content ===
    with st.sidebar:
        st.markdown("<h2 style='color:#f72585;'>📁 BollyAI 2.0</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        if st.button("🏠 Home"):
            st.switch_page("app.py")
        if st.button("📄 1. Data Cleaning"):
            st.switch_page("pages/page_1_data_cleaning.py")
        if st.button("🧠 2. Classification"):
            st.switch_page("pages/page_2_Classification.py")
        if st.button("📊 3. Visualization"):
            st.switch_page("pages/page_3_Visualization.py")
        if st.button("✍️ 4. Rewriting"):
            st.switch_page("pages/page_4_Rewrite.py")
        if st.button("📁 5. Reports"):
            st.switch_page("pages/page_5_Reports.py")
        if st.button("🖼️ 6. Poster Bias"):
            st.switch_page("pages/page_6_Poster_Analysis.py")
        if st.button("🎞️ 7. Trailer Trends"):
            st.switch_page("pages/page_7_Trailer_Visualization.py")
        if st.button("📚 8. Wiki Analysis"):
            st.switch_page("pages/page_8_Wiki_Analysis.py")

        st.markdown("---")
        st.markdown("<p style='font-size:13px; color:#aaa;'>Made with ❤️ by Aldrin</p>", unsafe_allow_html=True)
