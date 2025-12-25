import sys
import os

# Fix path to import 'src' modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.environment import LogisticsNetwork
from src.compiler import OmniGuardCompiler
from z3 import IntVal
import random

def run_experiment():
    print("--- 🚀 LAUNCHING OMNI-GUARD STRESS TEST ---")
    
    # 1. Initialize Digital Twin
    env = LogisticsNetwork(num_nodes=50)
    compiler = OmniGuardCompiler()
    
    # 2. Define Rule: "Budget <= 600"
    instruction = {"template_id": "MAX_BUDGET", "params": {"limit": 600}}
    
    stats = {"safe_plans": 0, "blocked_plans": 0}
    
    print(f"\nRule Active: MAX_BUDGET <= $600")
    print("-" * 60)
    print(f"{'EPISODE':<10} | {'COST':<10} | {'DECISION':<20}")
    print("-" * 60)
    
    for i in range(1, 21):
        # Agent picks random route
        path = env.find_random_route()
        if not path: continue
        
        # Get Physics
        context_values = env.get_route_context(path)
        z3_context = {
            'total_cost': IntVal(context_values['total_cost']),
            'quantity': IntVal(100),
            'node_in_path': lambda x: BoolVal(False) # Dummy for budget check
        }
        
        # Check Z3
        is_safe, msg = compiler.verify_action(instruction, z3_context)
        
        status = "✅ APPROVED" if is_safe else "🛑 BLOCKED"
        if is_safe: stats["safe_plans"] += 1
        else: stats["blocked_plans"] += 1
        
        print(f"Ep {i:<7} | ${context_values['total_cost']:<9} | {status}")

    print("-" * 60)
    print(f"RESULTS: {stats['safe_plans']} Safe, {stats['blocked_plans']} Dangerous Plans Caught.")

if __name__ == "__main__":
    run_experiment()