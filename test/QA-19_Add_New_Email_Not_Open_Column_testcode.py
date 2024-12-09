import pandas as pd

# Function to validate the NOT_OPENED_EMAIL column
def validate_not_opened_email(df):
    for index, row in df.iterrows():
        expected_value = None
        if row['IS_CLICKED'] is True and row['IS_OPENED'] is False:
            expected_value = True
        elif row['IS_CLICKED'] is True and row['IS_OPENED'] is True:
            expected_value = False
        # For rows with missing IS_CLICKED or IS_OPENED values, expected_value remains None

        actual_value = row['NOT_OPENED_EMAIL']
        assert actual_value == expected_value, f"Row {index} failed: Expected {expected_value}, got {actual_value}"

# Generate test data
test_data = generate_test_data()

# Validate the test data
validate_not_opened_email(test_data)
