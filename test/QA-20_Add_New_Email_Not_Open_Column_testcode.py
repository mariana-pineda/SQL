import pandas as pd

# Function to validate the NOT_OPENED_EMAIL column
def validate_not_opened_email(dataframe):
    # Iterate over each row and validate the NOT_OPENED_EMAIL column
    for index, row in dataframe.iterrows():
        expected_value = row['IS_CLICKED'] and not row['IS_OPENED']
        actual_value = row['NOT_OPENED_EMAIL']
        assert expected_value == actual_value, f"Validation failed at index {index}: expected {expected_value}, got {actual_value}"

# Generate test data
test_data = generate_test_data(30)

# Validate the test data
validate_not_opened_email(test_data)

# If no assertion error is raised, print success message
print("All validations passed successfully.")
