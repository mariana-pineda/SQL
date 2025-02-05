import random

# Function to generate test data
def generate_test_data():
    test_data = []

    # Happy Path Test Data
    # Test Case 1: Condition 1 - ref_txn_qty > 0 and cumulative_txn_qty >= cumulative_ref_ord_sched_qty
    test_data.append({
        "txn_id": 1,
        "ref_txn_qty": 50,
        "cumulative_txn_qty": 100,
        "cumulative_ref_ord_sched_qty": 90,
        "ref_ord_sched_qty": 50,
        "prior_cumulative_txn_qty": 40,
        "prior_cumulative_ref_ord_sched_qty": 30,
        "expected_apl_qty": 40  # Expected apl_qty based on Condition 1
    })

    # Test Case 2: Condition 2 - ref_txn_qty > 0 and cumulative_ref_ord_sched_qty >= cumulative_txn_qty
    test_data.append({
        "txn_id": 2,
        "ref_txn_qty": 20,
        "cumulative_txn_qty": 60,
        "cumulative_ref_ord_sched_qty": 100,
        "ref_ord_sched_qty": 30,
        "prior_cumulative_txn_qty": 30,
        "prior_cumulative_ref_ord_sched_qty": 25,
        "expected_apl_qty": 20  # Expected apl_qty based on Condition 2
    })

    # Test Case 3: Condition 3 - ref_txn_qty < 0, cumulative_txn_qty != 0, cumulative_ref_ord_sched_qty > 0
    test_data.append({
        "txn_id": 3,
        "ref_txn_qty": -10,
        "cumulative_txn_qty": 80,
        "cumulative_ref_ord_sched_qty": 70,
        "ref_ord_sched_qty": 40,
        "prior_cumulative_txn_qty": 50,
        "prior_cumulative_ref_ord_sched_qty": 45,
        "expected_apl_qty": -10  # Expected apl_qty based on Condition 3
    })

    # Edge Case Test Data
    # Test Case 4: Edge case where ref_txn_qty is zero
    test_data.append({
        "txn_id": 4,
        "ref_txn_qty": 0,
        "cumulative_txn_qty": 50,
        "cumulative_ref_ord_sched_qty": 50,
        "ref_ord_sched_qty": 20,
        "prior_cumulative_txn_qty": 20,
        "prior_cumulative_ref_ord_sched_qty": 20,
        "expected_apl_qty": None  # Default condition, apl_qty should be NULL
    })

    # Test Case 5: Edge case where cumulative_txn_qty equals cumulative_ref_ord_sched_qty
    test_data.append({
        "txn_id": 5,
        "ref_txn_qty": 10,
        "cumulative_txn_qty": 100,
        "cumulative_ref_ord_sched_qty": 100,
        "ref_ord_sched_qty": 10,
        "prior_cumulative_txn_qty": 50,
        "prior_cumulative_ref_ord_sched_qty": 50,
        "expected_apl_qty": 10  # Expected apl_qty based on Condition 2
    })

    # Error Case Test Data
    # Test Case 6: Invalid input where ref_txn_qty is a string
    test_data.append({
        "txn_id": 6,
        "ref_txn_qty": "invalid",
        "cumulative_txn_qty": 100,
        "cumulative_ref_ord_sched_qty": 90,
        "ref_ord_sched_qty": 50,
        "prior_cumulative_txn_qty": 40,
        "prior_cumulative_ref_ord_sched_qty": 30,
        "expected_apl_qty": None  # Invalid input, apl_qty should be NULL
    })

    # Test Case 7: Invalid input where cumulative_txn_qty is negative
    test_data.append({
        "txn_id": 7,
        "ref_txn_qty": 20,
        "cumulative_txn_qty": -50,
        "cumulative_ref_ord_sched_qty": 100,
        "ref_ord_sched_qty": 30,
        "prior_cumulative_txn_qty": 30,
        "prior_cumulative_ref_ord_sched_qty": 25,
        "expected_apl_qty": None  # Invalid input, apl_qty should be NULL
    })

    # Special Character and Format Test Data
    # Test Case 8: Special characters in ref_ord_sched_qty
    test_data.append({
        "txn_id": 8,
        "ref_txn_qty": 20,
        "cumulative_txn_qty": 60,
        "cumulative_ref_ord_sched_qty": 100,
        "ref_ord_sched_qty": "@30",
        "prior_cumulative_txn_qty": 30,
        "prior_cumulative_ref_ord_sched_qty": 25,
        "expected_apl_qty": None  # Invalid input, apl_qty should be NULL
    })

    # Test Case 9: Format test with large numbers
    test_data.append({
        "txn_id": 9,
        "ref_txn_qty": 1000000,
        "cumulative_txn_qty": 2000000,
        "cumulative_ref_ord_sched_qty": 1500000,
        "ref_ord_sched_qty": 1000000,
        "prior_cumulative_txn_qty": 500000,
        "prior_cumulative_ref_ord_sched_qty": 400000,
        "expected_apl_qty": 900000  # Expected apl_qty based on Condition 1
    })

    # Generate additional random test data to reach 20-30 records
    for i in range(10, 31):
        ref_txn_qty = random.choice([random.randint(-100, 100), "invalid"])
        cumulative_txn_qty = random.randint(0, 200)
        cumulative_ref_ord_sched_qty = random.randint(0, 200)
        ref_ord_sched_qty = random.randint(0, 100)
        prior_cumulative_txn_qty = random.randint(0, 100)
        prior_cumulative_ref_ord_sched_qty = random.randint(0, 100)

        # Determine expected_apl_qty based on conditions
        if isinstance(ref_txn_qty, int):
            if ref_txn_qty > 0:
                if cumulative_txn_qty >= cumulative_ref_ord_sched_qty:
                    expected_apl_qty = ref_ord_sched_qty
                elif cumulative_ref_ord_sched_qty >= cumulative_txn_qty:
                    expected_apl_qty = ref_txn_qty
                else:
                    expected_apl_qty = None
            elif ref_txn_qty < 0 and cumulative_txn_qty != 0 and cumulative_ref_ord_sched_qty > 0:
                expected_apl_qty = ref_txn_qty
            else:
                expected_apl_qty = None
        else:
            expected_apl_qty = None

        test_data.append({
            "txn_id": i,
            "ref_txn_qty": ref_txn_qty,
            "cumulative_txn_qty": cumulative_txn_qty,
            "cumulative_ref_ord_sched_qty": cumulative_ref_ord_sched_qty,
            "ref_ord_sched_qty": ref_ord_sched_qty,
            "prior_cumulative_txn_qty": prior_cumulative_txn_qty,
            "prior_cumulative_ref_ord_sched_qty": prior_cumulative_ref_ord_sched_qty,
            "expected_apl_qty": expected_apl_qty
        })

    return test_data

# Generate and print the test data
test_data = generate_test_data()
for record in test_data:
    print(record)
