import pandas as pd

def messages_to_dataframe(messages):
    df = pd.DataFrame([{
        "timestamp": m.timestamp,
        "sender": m.sender,
        "text": m.text,
        "emojis": m.emojis
    } for m in messages])

    return df
