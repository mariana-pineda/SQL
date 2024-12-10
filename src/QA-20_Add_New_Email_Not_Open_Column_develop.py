import pandas as pd

# Function to add NOT_OPENED_EMAIL column
def add_not_opened_email_column(dataframe):
    dataframe['NOT_OPENED_EMAIL'] = dataframe.apply(lambda row: row['IS_CLICKED'] and not row['IS_OPENED'], axis=1)
    return dataframe

# Example usage
data = {
    "IS_CLICKED": [True, True, False],
    "IS_OPENED": [False, True, False]
}

df = pd.DataFrame(data)
df = add_not_opened_email_column(df)
print(df)
