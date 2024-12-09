import pandas as pd
import random

# Generate test data
def generate_test_data(num_records=30):
    data = []
    for _ in range(num_records):
        is_clicked = random.choice([True, False, None])
        is_opened = random.choice([True, False, None])
        
        # Condition: Mark NOT_OPENED_EMAIL as TRUE for unopened emails
        if is_clicked is True and is_opened is False:
            not_opened_email = True
        # Condition: Do not mark NOT_OPENED_EMAIL as TRUE for opened emails
        elif is_clicked is True and is_opened is True:
            not_opened_email = False
        # Condition: Handle rows with missing IS_CLICKED or IS_OPENED values
        # Condition: Handle rows with unknown email status
        else:
            not_opened_email = None  # or set to a default value like False

        data.append({
            'IS_CLICKED': is_clicked,
            'IS_OPENED': is_opened,
            'NOT_OPENED_EMAIL': not_opened_email
        })
    
    return pd.DataFrame(data)

# Generate and print the test data
test_data = generate_test_data()
print(test_data)
