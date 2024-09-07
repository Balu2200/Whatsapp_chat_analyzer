import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import emoji


def fetch_stats(selected_user, df):
    if selected_user == "Overall":
        num_messages = df.shape[0]
        num_words = df['message'].str.split().str.len().sum()
        num_media = df[df['message'] == "<Media omitted>"].shape[0]
        num_links = df[df['message'].str.contains("http")].shape[0]
        return num_messages, num_words, num_media, num_links
    else:
        num_messages = df[df['user'] == selected_user].shape[0]
        num_words = df[df['user'] == selected_user]['message'].str.split().str.len().sum()
        num_media = df[(df['user'] == selected_user) & (df['message'] == "<Media omitted>")].shape[0]
        num_links = df[(df['user'] == selected_user) & (df['message'].str.contains("http"))].shape[0]
        return num_messages, num_words, num_media, num_links

def most_busy_users(df):
    x = df['user'].value_counts()
    dataframe = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'Percent'})
    return x, dataframe

def create_cloud(selected_user, df):
    if selected_user == "Overall":
        text = ' '.join(df['message'].dropna().astype(str).tolist())
    else:
        text = ' '.join(df[df['user'] == selected_user]['message'].dropna().astype(str).tolist())
    wc = WordCloud(width=800, height=400, max_words=200, background_color='white').generate(text)
    return wc

def emoji_helper(selected_user, df):
    emojis = []
    if selected_user == "Overall":
        messages = df['message']
    else:
        messages = df[df['user'] == selected_user]['message']
    
    for message in messages:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.columns = ['emoji', 'count']
    emoji_df = emoji_df.sort_values(by='count', ascending=False)
    return emoji_df

def message_timeline(selected_user, df, period='month'):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    df['dates'] = pd.to_datetime(df['dates'])

    if period == 'month':
        df['period'] = df['dates'].dt.to_period('M')
        timeline_df = df.groupby('period').size().reset_index(name='message_count')
    elif period == 'day':
        df['period'] = df['dates'].dt.to_period('D')
        timeline_df = df.groupby('period').size().reset_index(name='message_count')

    df['day_of_week'] = df['dates'].dt.day_name()
    df['time_of_day'] = df['dates'].dt.hour

    busiest_day = df['day_of_week'].value_counts().idxmax()
    busiest_hour = df['time_of_day'].value_counts().idxmax()

    busiest_day_count = df['day_of_week'].value_counts().max()
    busiest_hour_count = df['time_of_day'].value_counts().max()

    day_count_df = df['day_of_week'].value_counts().reset_index()
    day_count_df.columns = ['day_of_week', 'message_count']

    hour_count_df = df['time_of_day'].value_counts().sort_index().reset_index()
    hour_count_df.columns = ['time_of_day', 'message_count']

    return timeline_df, busiest_day, busiest_day_count, busiest_hour, busiest_hour_count, day_count_df, hour_count_df


