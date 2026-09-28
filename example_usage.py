from client import CostBasedQueryOptimizer

def main():
    cbo = CostBasedQueryOptimizer()
    plan = cbo.choose_optimal_join(1000, 5000)
    print("Cost-Based Query Optimizer Verification:")
    print(f"Optimal Plan: {plan['optimal_join']}")
    print(f"Evaluated Costs: {plan['all_costs']}")

if __name__ == "__main__":
    main()
