
import re
import pandas as pd
import numpy as np
import datetime
def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm)\s-\s"


    messages = re.split(pattern, data)[1:]
    dates=re.findall(pattern,data)

    df = pd.DataFrame({'user_messages': messages, 'message_dates': dates})
    df['message_dates'] = df['message_dates'].str.strip(' -')
    df['message_dates'] = df['message_dates'].str.replace(',', '')
    df['message_dates'] = pd.to_datetime(df['message_dates'], format="%d/%m/%y %I:%M %p")
    df.rename(columns={'message_dates': 'dates'}, inplace=True)



    user = []
    messages = []

    for message in df['user_messages']:
        entry = re.split(r"([\w\s]+?):\s", message, maxsplit=1)
        
        if len(entry) > 1:
            user.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:
            user.append('Balu')
            messages.append(entry[0].strip())

    df['user'] = user
    df['message'] = messages


    df.drop(columns=['user_messages'], inplace=True)


    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['time']=df['dates'].dt.hour
    df['minute']=df['dates'].dt.minute


    return df



