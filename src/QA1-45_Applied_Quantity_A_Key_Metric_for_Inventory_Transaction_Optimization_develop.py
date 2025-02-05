import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InventoryTransaction:
    def __init__(self, txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty):
        self.txn_id = txn_id
        self.ref_txn_qty = ref_txn_qty
        self.cumulative_txn_qty = cumulative_txn_qty
        self.cumulative_ref_ord_sched_qty = cumulative_ref_ord_sched_qty
        self.ref_ord_sched_qty = ref_ord_sched_qty
        self.prior_cumulative_txn_qty = prior_cumulative_txn_qty
        self.prior_cumulative_ref_ord_sched_qty = prior_cumulative_ref_ord_sched_qty

    def calculate_apl_qty(self):
        try:
            if not isinstance(self.ref_txn_qty, (int, float)) or not isinstance(self.cumulative_txn_qty, (int, float)) or not isinstance(self.cumulative_ref_ord_sched_qty, (int, float)):
                logging.error(f"Invalid input types for transaction {self.txn_id}")
                return None

            if self.ref_txn_qty > 0:
                if self.cumulative_txn_qty >= self.cumulative_ref_ord_sched_qty:
                    if self.prior_cumulative_ref_ord_sched_qty < self.prior_cumulative_txn_qty:
                        return self.ref_ord_sched_qty - (self.prior_cumulative_txn_qty - self.prior_cumulative_ref_ord_sched_qty)
                    else:
                        return self.ref_ord_sched_qty
                elif self.cumulative_ref_ord_sched_qty >= self.cumulative_txn_qty:
                    if self.prior_cumulative_ref_ord_sched_qty > self.prior_cumulative_txn_qty:
                        return self.ref_txn_qty - (self.prior_cumulative_ref_ord_sched_qty - self.prior_cumulative_txn_qty)
                    else:
                        return self.ref_txn_qty
            elif self.ref_txn_qty < 0 and self.cumulative_txn_qty != 0 and self.cumulative_ref_ord_sched_qty > 0:
                return self.ref_txn_qty

            return None
        except Exception as e:
            logging.error(f"Error calculating apl_qty for transaction {self.txn_id}: {e}")
            return None

# Example usage
transactions = [
    InventoryTransaction(1, 50, 100, 90, 50, 40, 30),
    InventoryTransaction(2, -10, 80, 70, 40, 50, 45),
    InventoryTransaction(3, 20, 60, 100, 30, 30, 25),
    InventoryTransaction(4, 0, 50, 50, 20, 20, 20),
    InventoryTransaction(5, 10, 100, 100, 10, 50, 50),
    InventoryTransaction(6, "invalid", 100, 90, 50, 40, 30),
    InventoryTransaction(7, 20, -50, 100, 30, 30, 25),
    InventoryTransaction(8, 20, 60, 100, "@30", 30, 25),
    InventoryTransaction(9, 1000000, 2000000, 1500000, 1000000, 500000, 400000)
]

for txn in transactions:
    apl_qty = txn.calculate_apl_qty()
    logging.info(f"Transaction ID {txn.txn_id}: Calculated apl_qty = {apl_qty}")

