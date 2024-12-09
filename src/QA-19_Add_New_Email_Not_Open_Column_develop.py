import pandas as pd

# Function to add and update the NOT_OPENED_EMAIL column
def add_not_opened_email_column(df):
    # Add the NOT_OPENED_EMAIL column with default value None
    df['NOT_OPENED_EMAIL'] = None

    # Update the NOT_OPENED_EMAIL column based on conditions
    df.loc[(df['IS_CLICKED'] == True) & (df['IS_OPENED'] == False), 'NOT_OPENED_EMAIL'] = True
    df.loc[(df['IS_CLICKED'] == True) & (df['IS_OPENED'] == True), 'NOT_OPENED_EMAIL'] = False

    return df

# Example usage with test data
test_data = generate_test_data()
updated_data = add_not_opened_email_column(test_data)
print(updated_data)
