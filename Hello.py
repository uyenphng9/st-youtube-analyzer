"""
This streamlit application allows users to analyse and visualise 
youtube channels data. 
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title('The Youtube Channels Analysis 🎬')
SIDEBAR_TITLE = 'Navigation'
MENU_MSG = 'Choose your action'
MENU_CHOICES = ['Data explorer', 'Data analysis']


@st.cache_data
def get_category(data):
    """Get a list of unique categories from the dataset."""
    category_list = data['category'].unique().tolist()
    sort_category = sorted(map(str, category_list))
    return sort_category[:10]


@st.cache_data
def get_channel(data):
    """Get a count of YouTubers for each category."""
    return data.groupby('category').count()['Youtuber'].reset_index()


@st.cache_data
def load_data():
    """Load and preprocess the YouTube data from the CSV file."""
    df_youtube = pd.read_csv('most_subscribed_youtube_channels.csv')

    # Change the data type
    df_youtube["subscribers"] = [
        value.replace(",", "") for value in df_youtube["subscribers"]]
    df_youtube["video views"] = [
        value.replace(",", "") for value in df_youtube["video views"]]
    df_youtube["subscribers"] = df_youtube["subscribers"].astype("float")
    df_youtube["video views"] = df_youtube["video views"].astype("float")

    return df_youtube


def data_explorer(data):
    """Explore and visualize the YouTube data."""
    st.header('Data Explorer')
    category_list = ['All'] + get_category(data)
    selected_category = st.selectbox('Select the category', category_list)

    # Show filtered data
    if selected_category == 'All':
        st.write('The data you want to see')
        st.write(data.head())
        filtered_data = data
    else:
        st.write(f'You have selected {selected_category}')
        filtered_data = data[data['category'] == selected_category]
        st.write(filtered_data)

    # Create a download button for the filtered data
    if st.button("Download the data"):
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='filtered_data.csv',
            mime='text/csv',
        )

    # Create a bar plot for the number of YouTubers in each category
    st.header('Category Distribution')
    st.subheader('You can see the most popular category here')
    category_counts = data['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    fig = px.bar(category_counts, x='Category', y='Count',
                 title='Number of YouTubers in Each Category')
    st.plotly_chart(fig)


def plot_ranking(data, ranking_by):
    fig2, _ = plt.subplots()

    # Sort the data based on the selected ranking metric
    data = data.sort_values(by=ranking_by, ascending=False)

    # Create a bar plot, presents top 10
    sns.barplot(data=data[:10], x='Youtuber', y=ranking_by)
    plt.xlabel('Youtuber')
    plt.ylabel(f"Number of {ranking_by}")
    plt.title(f"Top 10 YouTubers ranking by {ranking_by}")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)


def data_analysis(data):
    st.header('Data Analysis')
    col1, col2 = st.columns(2)

    # Column 1: based on ranking metrics
    with col1:
        st.subheader(
            'See the most popular YouTuber based on different ranking metrics')
        ranking_metric = st.selectbox('Select a ranking metric', [
            'subscribers', 'video views'])
        st.write(f"Ranking based on: {ranking_metric}")
        sorted_data = data.sort_values(by=ranking_metric, ascending=False)
        st.write(
            sorted_data[['Youtuber', ranking_metric]].reset_index(drop=True))

    # Column 2: ranking plot
    with col2:
        plot_ranking(data, ranking_metric)

    # Scatter plot
    st.subheader('Scatter Plot: Subscribers vs. Video Views')
    fig, ax = plt.subplots()
    ax.scatter(data['subscribers'], data['video views'], alpha=0.5)
    ax.set_xlabel('Subscribers')
    ax.set_ylabel('Video Views')
    st.pyplot(fig)


def main():
    df_youtube = load_data()

    st.sidebar.title(SIDEBAR_TITLE)

    menu = st.sidebar.selectbox(MENU_MSG, MENU_CHOICES)

    if menu == 'Data explorer':
        data_explorer(df_youtube)
    elif menu == 'Data analysis':
        data_analysis(df_youtube)
    else:
        st.write('Error: Invalid selection')


if __name__ == '__main__':
    main()
