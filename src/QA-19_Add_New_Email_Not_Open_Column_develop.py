import pandas as pd

def add_not_opened_email_column(df):
    df['NOT_OPENED_EMAIL'] = df.apply(
        lambda row: True if row['IS_CLICKED'] is True and row['IS_OPENED'] is False else None, axis=1
    )
    return df

# Example usage
data = {
    'IS_CLICKED': [True, True, False, None, True],
    'IS_OPENED': [False, True, None, True, None]
}

df = pd.DataFrame(data)
df = add_not_opened_email_column(df)
print(df)
