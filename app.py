import streamlit as st
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.subheader("Upload your chat file")
uploaded_file = st.sidebar.file_uploader("Choose a file", key="file_uploader")

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    if df.empty:
        st.error("The DataFrame is empty. Please check the uploaded file.")
    else:
        st.dataframe(df)

        users = df['user'].unique().tolist()
        users.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", users, key="user_selectbox")
        timeline_period = st.sidebar.selectbox("Timeline Period", ['month', 'day'], key="timeline_selectbox")

        if st.sidebar.button("Show analysis", key="show_analysis"):
            num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(num_words)
            with col3:
                st.header("Total Media")
                st.title(num_media)
            with col4:
                st.header("Total Links")
                st.title(num_links)

            wc = helper.create_cloud(selected_user, df)
            st.write("Word Cloud")
            st.image(wc.to_array(), use_column_width=True)

            emoji_df = helper.emoji_helper(selected_user, df)
            st.write("Emoji Analysis")

            top_10_emoji_df = emoji_df.head(10)

            col1, col2 = st.columns(2)
            with col1:
                st.write("Top 10 Most Used Emojis")
                st.dataframe(top_10_emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.bar(top_10_emoji_df['emoji'], top_10_emoji_df['count'], color='blue')
                ax.set_xlabel('Emoji')
                ax.set_ylabel('Count')
                ax.set_title('Top 10 Most Used Emojis')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            timeline_df, busiest_day, busiest_day_count, busiest_hour, busiest_hour_count, day_count_df, hour_count_df = helper.message_timeline(selected_user, df, period=timeline_period)
            st.write(f"Message Timeline ({timeline_period.capitalize()})")

            fig, ax = plt.subplots()
            ax.plot(timeline_df['period'].astype(str), timeline_df['message_count'], marker='o', color='b')
            ax.set_xlabel(timeline_period.capitalize())
            ax.set_ylabel('Number of Messages')
            ax.set_title(f'Messages Over Time ({timeline_period.capitalize()})')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            st.write(f"Busiest Day of the Week: {busiest_day} with {busiest_day_count} messages")
            st.write(f"Busiest Hour of the Day: {busiest_hour}:00 with {busiest_hour_count} messages")

            fig, ax = plt.subplots()
            ax.bar(day_count_df['day_of_week'], day_count_df['message_count'], color='orange')
            ax.set_xlabel('Day of the Week')
            ax.set_ylabel('Message Count')
            ax.set_title('Messages by Day of the Week')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            fig, ax = plt.subplots()
            ax.bar(hour_count_df['time_of_day'], hour_count_df['message_count'], color='green')
            ax.set_xlabel('Hour of the Day')
            ax.set_ylabel('Message Count')
            ax.set_title('Messages by Hour of the Day')
            plt.xticks(rotation=45)
            st.pyplot(fig)
