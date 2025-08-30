import streamlit as st

def render_ui(dataframe, fig):
    """
    Custom UI rendering for hackathon presentation.
    """
    st.markdown("## ✨ Dashboard Overview")

    # --- Chart Section ---
    if fig:
        st.markdown("### 📊 Chart View")
        st.plotly_chart(fig, use_container_width=True, key="main_chart")

    # --- Data Section ---
    with st.expander("📑 View Data Table", expanded=False):
        st.dataframe(dataframe, use_container_width=True)

    # --- Insights Section ---
    st.markdown("### 🔍 Quick Insights")
    if not dataframe.empty:
        st.write(f"Total Countries: **{dataframe['country'].nunique()}**")
        st.write(f"Year Displayed: **{dataframe['year'].iloc[0]}**")
        if dataframe['continent'].nunique() == 1:
            st.write(f"Region: **{dataframe['continent'].iloc[0]}**")
        else:
            st.write("Region: **All**")
    else:
        st.warning("⚠️ No data available for this filter.")

    # --- Footer ---
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit, Whisper & Plotly for Hackathon 2025 🚀")
