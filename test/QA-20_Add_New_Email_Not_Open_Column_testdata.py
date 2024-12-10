import random
import pandas as pd

# Generate test data
def generate_test_data(num_records=30):
    data = []
    for _ in range(num_records):
        is_clicked = random.choice([True, False])
        is_opened = random.choice([True, False])
        
        # Condition: Mark NOT_OPENED_EMAIL as TRUE when IS_CLICKED is TRUE and IS_OPENED is FALSE
        not_opened_email = is_clicked and not is_opened
        
        data.append({
            "IS_CLICKED": is_clicked,
            "IS_OPENED": is_opened,
            "NOT_OPENED_EMAIL": not_opened_email
        })
    
    return pd.DataFrame(data)

# Generate 20-30 records
test_data = generate_test_data(30)

# Display the generated test data
print(test_data)
