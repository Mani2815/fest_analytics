"""
GATEWAYS-2025 National Level Fest Analysis
Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import geopandas as gpd
import re
from collections import Counter

# ─────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="GATEWAYS 2025 - Fest Analysis",
    page_icon="🎓",
    layout="wide"
)

# ─────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/fest_dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ─────────────────────────────────────────
# Load India GeoJSON (states in dataset only)
# ─────────────────────────────────────────
@st.cache_data
def load_geo():
    gdf = gpd.read_file("data/india_states.geojson")
    return gdf

india_gdf = load_geo()

# ─────────────────────────────────────────
# Sidebar Navigation
# ─────────────────────────────────────────
st.sidebar.image("assets/logo.png", width="stretch")

col1, col2 = st.sidebar.columns([0.2, 0.8], vertical_alignment="center")
with col1:
    st.image("assets/favicon.ico", width="stretch")
with col2:
    st.markdown("<h1 style='margin: 0; padding: 0;'>GATEWAYS 2025</h1>", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📌 Navigate to",
    ["🏠 Dashboard", "👥 Participation Analysis", "💬 Feedback Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Records:** {len(df)}")
st.sidebar.markdown(f"**Events:** {df['Event Name'].nunique()}")
st.sidebar.markdown(f"**States:** {df['State'].nunique()}")
st.sidebar.markdown(f"**Colleges:** {df['College'].nunique()}")


# ══════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ══════════════════════════════════════════
if page == "🏠 Dashboard":
    st.title("🎓 GATEWAYS-2025 | National Level Fest")
    st.markdown("### Overview Dashboard")
    st.markdown("---")

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Participants", len(df))

    with col2:
        top_event = df['Event Name'].value_counts().idxmax()
        st.metric("🏆 Top Event", top_event)

    with col3:
        avg_rating = round(df['Rating'].mean(), 2)
        st.metric("⭐ Avg Rating", f"{avg_rating} / 5")

    with col4:
        total_revenue = df['Amount Paid'].sum()
        st.metric("💰 Total Revenue", f"₹{total_revenue:,}")

    st.markdown("---")

    # Row 2 — Event distribution + State distribution
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📊 Event-wise Participants")
        event_counts = df['Event Name'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = plt.cm.Set2.colors[:len(event_counts)]
        bars = ax.barh(event_counts.index, event_counts.values, color=colors)
        ax.set_xlabel("Number of Participants")
        ax.bar_label(bars, padding=3)
        ax.set_title("Participants per Event")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("🗺️ State-wise Distribution")
        state_counts = df['State'].value_counts()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax2.pie(
            state_counts.values,
            labels=state_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Pastel1.colors[:len(state_counts)]
        )
        ax2.set_title("State-wise Participant Share")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    st.markdown("---")

    # Row 3 — Rating breakdown + Revenue by Event Type
    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("⭐ Rating Distribution")
        rating_counts = df['Rating'].value_counts().sort_index()
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        ax3.bar(
            rating_counts.index.astype(str),
            rating_counts.values,
            color=['#ef5350', '#ffa726', '#66bb6a'],
            edgecolor='black'
        )
        ax3.set_xlabel("Rating")
        ax3.set_ylabel("Count")
        ax3.set_title("Rating Distribution")
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    with col_d:
        st.subheader("💵 Revenue by Event Type")
        rev_by_type = df.groupby('Event Type')['Amount Paid'].sum()
        fig4, ax4 = plt.subplots(figsize=(5, 3))
        bars4 = ax4.bar(rev_by_type.index, rev_by_type.values,
                        color=['#42a5f5', '#ab47bc'], edgecolor='black')
        ax4.bar_label(bars4, fmt='₹%.0f', padding=3)
        ax4.set_xlabel("Event Type")
        ax4.set_ylabel("Revenue (₹)")
        ax4.set_title("Revenue by Event Type")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    st.markdown("---")
    st.subheader("📋 Full Dataset Preview")
    st.dataframe(df, width="stretch")


# ══════════════════════════════════════════
# PAGE 2 — PARTICIPATION ANALYSIS
# ══════════════════════════════════════════
elif page == "👥 Participation Analysis":
    st.title("👥 Participation Analysis")
    st.markdown("Detailed breakdown of participants across events, colleges, and states.")
    st.markdown("---")

    # --- Section 1: Event-wise ---
    st.subheader("🏅 Event-wise Participant Count")

    event_counts = df['Event Name'].value_counts().reset_index()
    event_counts.columns = ['Event Name', 'Count']

    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = plt.cm.tab10.colors[:len(event_counts)]
        bars = ax.bar(event_counts['Event Name'], event_counts['Count'],
                      color=colors, edgecolor='black')
        ax.bar_label(bars, padding=3)
        ax.set_xlabel("Event")
        ax.set_ylabel("Participants")
        ax.set_title("Event-wise Participation")
        plt.xticks(rotation=20, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("**Event Summary Table**")
        st.dataframe(event_counts, width='stretch', hide_index=True)

    st.markdown("---")

    # --- Section 2: College-wise ---
    st.subheader("🏫 College-wise Participant Count")

    college_counts = df['College'].value_counts().reset_index()
    college_counts.columns = ['College', 'Count']

    col3, col4 = st.columns([2, 1])
    with col3:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ccolors = plt.cm.Set3.colors[:len(college_counts)]
        bars2 = ax2.barh(college_counts['College'], college_counts['Count'],
                         color=ccolors, edgecolor='black')
        ax2.bar_label(bars2, padding=3)
        ax2.set_xlabel("Participants")
        ax2.set_title("College-wise Participation")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    with col4:
        st.markdown("**College Summary Table**")
        st.dataframe(college_counts, width="stretch", hide_index=True)

    st.markdown("---")

    # --- Section 3: State-wise Table + Bar ---
    st.subheader("🗺️ State-wise Participant Count")

    state_counts = df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']

    col5, col6 = st.columns([2, 1])
    with col5:
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        scolors = plt.cm.Accent.colors[:len(state_counts)]
        bars3 = ax3.bar(state_counts['State'], state_counts['Count'],
                        color=scolors, edgecolor='black')
        ax3.bar_label(bars3, padding=3)
        ax3.set_xlabel("State")
        ax3.set_ylabel("Participants")
        ax3.set_title("State-wise Participation")
        plt.xticks(rotation=20, ha='right')
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    with col6:
        st.markdown("**State Summary Table**")
        st.dataframe(state_counts, width="stretch", hide_index=True)

    st.markdown("---")

    # --- Section 4: India Map using GeoPandas ---
    st.subheader("🇮🇳 India Map — State-wise Participants")
    st.caption("Showing states present in the GATEWAYS-2025 dataset")

    # Merge participant counts with GeoDataFrame
    state_series = df['State'].value_counts().reset_index()
    state_series.columns = ['NAME_1', 'Participants']
    merged_gdf = india_gdf.merge(state_series, on='NAME_1', how='left')
    merged_gdf['Participants'] = merged_gdf['Participants'].fillna(0)

    fig_map, ax_map = plt.subplots(figsize=(10, 8))
    merged_gdf.plot(
        column='Participants',
        ax=ax_map,
        legend=True,
        cmap='YlOrRd',
        edgecolor='black',
        linewidth=0.8,
        legend_kwds={'label': "Number of Participants", 'orientation': "vertical"}
    )

    # Add state name labels
    for _, row in merged_gdf.iterrows():
        centroid = row.geometry.centroid
        count = int(row['Participants'])
        ax_map.annotate(
            f"{row['NAME_1']}\n({count})",
            xy=(centroid.x, centroid.y),
            ha='center', va='center',
            fontsize=7, fontweight='bold',
            color='black'
        )

    ax_map.set_title("GATEWAYS-2025: Participants by State", fontsize=14, fontweight='bold')
    ax_map.set_axis_off()
    plt.tight_layout()
    st.pyplot(fig_map)
    plt.close()


# ══════════════════════════════════════════
# PAGE 3 — FEEDBACK ANALYSIS
# ══════════════════════════════════════════
elif page == "💬 Feedback Analysis":
    st.title("💬 Feedback Analysis")
    st.markdown("Analyze participant ratings and text feedback.")
    st.markdown("---")

    # --- Section 1: Rating Bar Chart ---
    st.subheader("⭐ Participant Ratings")

    rating_counts = df['Rating'].value_counts().sort_index()
    rating_labels = {3: "Average (3)", 4: "Good (4)", 5: "Excellent (5)"}
    bar_colors = ['#ef5350', '#ffa726', '#66bb6a']

    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(
            [rating_labels.get(r, str(r)) for r in rating_counts.index],
            rating_counts.values,
            color=bar_colors[:len(rating_counts)],
            edgecolor='black'
        )
        ax.bar_label(bars, padding=3)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Number of Participants")
        ax.set_title("Feedback Ratings Distribution")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("**Rating Summary**")
        rating_df = pd.DataFrame({
            'Rating': rating_counts.index,
            'Count': rating_counts.values,
            'Percentage': (rating_counts.values / len(df) * 100).round(1)
        })
        st.dataframe(rating_df, width="stretch", hide_index=True)
        st.markdown(f"**Average Rating:** ⭐ {df['Rating'].mean():.2f} / 5")

    st.markdown("---")

    # --- Section 2: Text Preprocessing & Display ---
    st.subheader("📝 Text Feedback Processing")

    # Basic text cleaning function
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)  # remove non-alpha chars
        tokens = text.split()
        return tokens

    # Common stopwords (basic list)
    STOPWORDS = {
        'and', 'the', 'is', 'in', 'it', 'to', 'a', 'of', 'for',
        'on', 'was', 'that', 'this', 'with', 'very', 'an', 'are'
    }

    # Collect all tokens from feedback
    all_tokens = []
    for feedback in df['Feedback on Fest'].dropna():
        tokens = clean_text(feedback)
        filtered = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
        all_tokens.extend(filtered)

    word_freq = Counter(all_tokens)
    top_words = word_freq.most_common(15)

    col3, col4 = st.columns([2, 1])
    with col3:
        st.markdown("**Top 15 Most Common Words in Feedback**")
        words, freqs = zip(*top_words)
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        colors2 = plt.cm.tab20.colors[:len(words)]
        bars2 = ax2.barh(list(words), list(freqs), color=colors2, edgecolor='black')
        ax2.bar_label(bars2, padding=3)
        ax2.set_xlabel("Frequency")
        ax2.set_title("Most Common Words in Feedback")
        ax2.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    with col4:
        st.markdown("**Word Frequency Table**")
        wf_df = pd.DataFrame(top_words, columns=['Word', 'Count'])
        st.dataframe(wf_df, width="stretch", hide_index=True)

    st.markdown("---")

    # --- Section 3: Feedback by Event ---
    st.subheader("📊 Average Rating by Event")

    avg_by_event = df.groupby('Event Name')['Rating'].mean().round(2).sort_values(ascending=False)

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    bar_colors3 = plt.cm.RdYlGn(
        [(r - avg_by_event.min()) / (avg_by_event.max() - avg_by_event.min())
         for r in avg_by_event.values]
    )
    bars3 = ax3.bar(avg_by_event.index, avg_by_event.values,
                    color=bar_colors3, edgecolor='black')
    ax3.bar_label(bars3, fmt='%.2f', padding=3)
    ax3.set_xlabel("Event")
    ax3.set_ylabel("Average Rating")
    ax3.set_ylim(0, 5.5)
    ax3.set_title("Average Rating per Event")
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

    st.markdown("---")

    # --- Section 4: Sentiment Idea ---
    st.subheader("💡 Simple Sentiment Insight")

    # Simple rule-based sentiment
    positive_words = {'excellent', 'great', 'good', 'amazing', 'wonderful',
                      'fantastic', 'engaging', 'interesting', 'fun', 'creative',
                      'practical', 'informative', 'well', 'useful', 'inspiring'}
    negative_words = {'bad', 'poor', 'boring', 'terrible', 'worst',
                      'disappointing', 'slow', 'confusing'}

    def get_sentiment(text):
        tokens = set(clean_text(text))
        pos_hits = tokens & positive_words
        neg_hits = tokens & negative_words
        if len(pos_hits) > len(neg_hits):
            return "Positive"
        elif len(neg_hits) > len(pos_hits):
            return "Negative"
        else:
            return "Neutral"

    df['Sentiment'] = df['Feedback on Fest'].apply(get_sentiment)
    sentiment_counts = df['Sentiment'].value_counts()

    col5, col6 = st.columns([1, 2])
    with col5:
        st.markdown("**Sentiment Breakdown**")
        sent_colors = {'Positive': '#66bb6a', 'Neutral': '#ffa726', 'Negative': '#ef5350'}
        s_colors = [sent_colors.get(s, '#90a4ae') for s in sentiment_counts.index]

        fig4, ax4 = plt.subplots(figsize=(4, 4))
        ax4.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            colors=s_colors,
            startangle=90
        )
        ax4.set_title("Feedback Sentiment")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    with col6:
        st.markdown("**Sample Feedback Records**")
        sample_df = df[['Student Name', 'Event Name', 'Rating', 'Feedback on Fest', 'Sentiment']].sample(10)
        st.dataframe(sample_df, width="stretch", hide_index=True)
