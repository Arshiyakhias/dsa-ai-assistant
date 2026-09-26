import streamlit as st
from scraper import analyze_page

# --------------------------------
# Page configuration
# --------------------------------
st.set_page_config(
    page_title="Web Page Analyzer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------
# Custom CSS
# --------------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0e1117;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Hero section */
    .hero {
        padding: 2rem 0 1.5rem 0;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #9ca3af;
        margin-bottom: 1.5rem;
    }

    /* Section headings */
    .section-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #ffffff;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* Page information card */
    .info-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.5rem;
    }

    .info-label {
        color: #8b949e;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }

    .info-value {
        color: #ffffff;
        font-size: 1rem;
        word-break: break-word;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 1rem;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #8b949e;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 2.7rem;
    }

    /* Text input */
    div[data-baseweb="input"] {
        background: #161b22;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #161b22;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Code blocks */
    code {
        font-size: 0.9rem;
    }

    /* Divider */
    hr {
        border-color: #30363d;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------
# Hero
# --------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">🌐 Web Page Analyzer</div>
    <div class="hero-subtitle">
        Fetch a webpage and explore its HTML content, links, images and tables.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------
# URL input
# --------------------------------
url = st.text_input(
    "🔗 Webpage URL",
    placeholder="https://example.com",
    label_visibility="visible"
)

analyze_clicked = st.button(
    "🔍 Analyze Page",
    use_container_width=True,
    type="primary"
)


# --------------------------------
# Analyze Page
# --------------------------------
if analyze_clicked:

    if not url:
        st.warning("Please enter a URL.")

    else:
        with st.spinner("Fetching and analyzing webpage..."):
            try:
                result = analyze_page(url)

                st.session_state["current_result"] = result

            except Exception as e:
                st.error(f"Something went wrong: {e}")


# --------------------------------
# Display result
# --------------------------------
if "current_result" in st.session_state:

    result = st.session_state["current_result"]

    st.divider()

    # --------------------------------
    # PAGE INFORMATION
    # --------------------------------
    st.markdown(
        '<div class="section-title">📄 Page Information</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        st.metric(
            "HTTP Status",
            result["status_code"]
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">PAGE TITLE</div>
                <div class="info-value">{result["title"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">URL</div>
                <div class="info-value">{result["url"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------
    # HTML STATISTICS
    # --------------------------------
    st.markdown(
        '<div class="section-title">📊 HTML Statistics</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "🏷️ Headings",
        len(result["headings"])
    )

    col2.metric(
        "📝 Paragraphs",
        len(result["paragraphs"])
    )

    col3.metric(
        "🔗 Links",
        len(result["links"])
    )

    col4.metric(
        "🖼️ Images",
        len(result["images"])
    )

    col5.metric(
        "📊 Tables",
        len(result["tables"])
    )


    # --------------------------------
    # CONTENT
    # --------------------------------
    st.markdown(
        '<div class="section-title">🔎 Extracted Content</div>',
        unsafe_allow_html=True
    )


    # --------------------------------
    # HEADINGS
    # --------------------------------
    with st.expander(
        f"🏷️ Headings  ·  {len(result['headings'])}"
    ):

        if result["headings"]:

            for heading in result["headings"]:

                st.markdown(
                    f"**`{heading['tag']}`**  {heading['text']}"
                )

        else:
            st.info("No headings found.")


    # --------------------------------
    # PARAGRAPHS
    # --------------------------------
    with st.expander(
        f"📝 Paragraphs  ·  {len(result['paragraphs'])}"
    ):

        if result["paragraphs"]:

            for number, paragraph in enumerate(
                result["paragraphs"],
                start=1
            ):

                st.markdown(
                    f"**{number}.** {paragraph}"
                )

        else:
            st.info("No paragraphs found.")


    # --------------------------------
    # LINKS
    # --------------------------------
    with st.expander(
        f"🔗 Links  ·  {len(result['links'])}"
    ):

        if result["links"]:

            for number, link in enumerate(
                result["links"],
                start=1
            ):

                link_text = link["text"] or "(no text)"

                st.markdown(
                    f"**{number}. {link_text}**"
                )

                st.code(
                    link["url"],
                    language="text"
                )

        else:
            st.info("No links found.")


    # --------------------------------
    # IMAGES
    # --------------------------------
    with st.expander(
        f"🖼️ Images  ·  {len(result['images'])}"
    ):

        if result["images"]:

            for number, image in enumerate(
                result["images"],
                start=1
            ):

                alt = image["alt"] or "No alt text"

                st.markdown(
                    f"**{number}. {alt}**"
                )

                st.code(
                    image["url"],
                    language="text"
                )

        else:
            st.info("No images found.")


    # --------------------------------
    # TABLES
    # --------------------------------
    with st.expander(
        f"📊 Tables  ·  {len(result['tables'])}"
    ):

        if result["tables"]:

            for number, table in enumerate(
                result["tables"],
                start=1
            ):

                st.markdown(f"#### Table {number}")

                if len(table) > 1:

                    headers = table[0]
                    rows = table[1:]

                    table_data = []

                    for row in rows:

                        row = row[:len(headers)]

                        while len(row) < len(headers):
                            row.append("")

                        table_data.append(row)

                    st.dataframe(
                        table_data,
                        column_config={
                            str(i): headers[i]
                            for i in range(len(headers))
                        },
                        use_container_width=True,
                        hide_index=True
                    )

                else:
                    st.write(table)

        else:
            st.info("No tables found.")


    # --------------------------------
    # LINK EXPLORER
    # --------------------------------
    st.divider()

    st.markdown(
        '<div class="section-title">🚀 Explore Another Page</div>',
        unsafe_allow_html=True
    )

    links = result["links"]

    if links:

        # Remove empty link names
        link_options = [
            link["text"] or "(Unnamed link)"
            for link in links
        ]

        selected_index = st.selectbox(
            "Choose a link from this webpage",
            range(len(link_options)),
            format_func=lambda x: link_options[x]
        )

        selected_url = links[selected_index]["url"]

        st.code(
            selected_url,
            language="text"
        )

        if st.button(
            "🚀 Explore Selected Link",
            use_container_width=True
        ):

            with st.spinner("Analyzing selected page..."):

                try:

                    new_result = analyze_page(
                        selected_url
                    )

                    st.session_state[
                        "current_result"
                    ] = new_result

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Could not analyze page: {e}"
                    )

    else:

        st.info("No links found on this page.")