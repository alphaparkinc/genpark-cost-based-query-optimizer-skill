"""Cost-Based Relational Query Optimizer (CBO)
100% Python Standard Library.
"""

class CostBasedQueryOptimizer:
    """Relational join cost evaluation and plan selection."""
    def estimate_cost(self, join_type, table_a_rows, table_b_rows):
        if join_type == "nested_loop":
            return table_a_rows * table_b_rows
        elif join_type == "hash_join":
            return 3 * (table_a_rows + table_b_rows)
        elif join_type == "sort_merge":
            return (table_a_rows * (1 + (table_a_rows).bit_length()) +
                    table_b_rows * (1 + (table_b_rows).bit_length()) +
                    (table_a_rows + table_b_rows))
        return float('inf')

    def choose_optimal_join(self, table_a_rows, table_b_rows):
        joins = ["nested_loop", "hash_join", "sort_merge"]
        costs = {j: self.estimate_cost(j, table_a_rows, table_b_rows) for j in joins}
        best = min(costs, key=costs.get)
        return {
            "optimal_join": best,
            "cost": costs[best],
            "all_costs": costs
        }
