# GATEWAYS 2025 Fest Analysis

This project is a **Streamlit Web Application** designed to analyze and visualize data from the GATEWAYS-2025 National Level Fest. It provides an interactive dashboard to explore participation metrics, event popularity, revenue, and participant feedback.

## Features

The application is divided into three main pages:

1. **🏠 Dashboard**
   - High-level overview metrics (Total Participants, Top Event, Average Rating, Total Revenue).
   - Visualizations of participants per event and state-wise participant share.
   - Rating distribution and Revenue by event type.
   - A complete preview of the underlying dataset.

2. **👥 Participation Analysis**
   - Detailed breakdowns of participant counts by Event, College, and State.
   - Bar charts and data tables for deep dives into participation stats.
   - **Interactive India Map** (using GeoPandas) to visually display the geographic distribution of participants.

3. **💬 Feedback Analysis**
   - Participant rating analysis with bar charts.
   - Text processing of feedback comments to extract the most common words and themes.
   - Average rating comparison across different events.
   - A basic rule-based Sentiment Analysis (Positive, Neutral, Negative) applied to the text feedback.

## Project Structure

```
├── app.py                  # Main Streamlit application file
├── requirements.txt        # Python dependencies
├── assets/
│   ├── favicon.ico         # App favicon
│   └── logo.png            # App logo
└── data/
    ├── fest_dataset.csv    # The primary dataset of fest participants and feedback
    └── india_states.geojson # GeoJSON file for plotting the state-wise map
```

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mani2815/fest_analytics.git
   cd fest_analytics
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed. It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the Streamlit application, run the following command in your terminal:

```bash
streamlit run app.py
```

The application will launch in your default web browser (typically at `http://localhost:8501`).

## Technologies Used

- **[Streamlit](https://streamlit.io/):** For building the interactive web application.
- **[Pandas](https://pandas.pydata.org/):** For data manipulation and analysis.
- **[Matplotlib](https://matplotlib.org/):** For rendering charts and graphs.
- **[GeoPandas](https://geopandas.org/):** For geographical plotting (India map).
- **[Scikit-Learn](https://scikit-learn.org/):** Included in dependencies for potential machine learning/advanced analysis tasks.
