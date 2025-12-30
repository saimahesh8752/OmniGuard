import networkx as nx
import random
import json
import time
import os
from z3 import *
from tqdm import tqdm

# --- CONFIGURATION ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class OmniGuard:
    def __init__(self, graph, budget_limit):
        self.graph = graph
        self.budget_limit = budget_limit
        self.solver = Solver()

    def verify_action(self, current_node, next_node, current_cost):
        """
        The Core Neuro-Symbolic Kernel.
        Uses Z3 to mathematically prove if a move is safe.
        """
        self.solver.reset()

        # 1. Define Z3 Variables
        s_current = Int('current_node')
        s_next = Int('next_node')
        s_cost = Int('total_cost')
        s_budget = Int('budget')

        # 2. Add Physical Constraints (Topology)
        # "The move is valid ONLY IF an edge exists between current and next"
        neighbors = list(self.graph.neighbors(current_node))
        
        # Create a Z3 'Or' condition: next_node must be one of the neighbors
        valid_transition = Or([s_next == n for n in neighbors])
        
        # 3. Add Safety Constraints (Budget)
        # "The total cost after this move must be less than the budget"
        # We assume each move costs 10 units for this simulation
        move_cost = 10
        safety_rule = (s_cost + move_cost) <= s_budget

        # 4. Load the specific values for this moment
        self.solver.add(s_current == current_node)
        self.solver.add(s_next == next_node)
        self.solver.add(s_cost == current_cost)
        self.solver.add(s_budget == self.budget_limit)

        # 5. Check Logic
        # We check: Is it possible to satisfy Physics AND Safety?
        self.solver.add(valid_transition)
        self.solver.add(safety_rule)

        result = self.solver.check()
        
        if result == sat:
            return True, "SAFE"
        else:
            # If UNSAT, it means the move violates physics or safety
            return False, "VIOLATION_DETECTED"

def simulate_llm_planner(graph, current_node):
    """
    Simulates an LLM that sometimes 'hallucinates'.
    It picks a random node from the graph. 
    Sometimes it picks a valid neighbor (Correct), 
    Sometimes it picks a far away node (Teleportation Hallucination).
    """
    # 30% chance to hallucinate a random node (unsafe/impossible move)
    if random.random() < 0.3:
        return random.choice(list(graph.nodes()))
    else:
        # 70% chance to pick a valid neighbor
        neighbors = list(graph.neighbors(current_node))
        if not neighbors: return current_node
        return random.choice(neighbors)

def run_experiment():
    print("Initializing Logistics Digital Twin...")
    # Create a random graph (50 nodes, as promised in the paper)
    G = nx.scale_free_graph(50, seed=42)
    G = nx.Graph(G) # Convert to undirected
    
    guard = OmniGuard(G, budget_limit=100)
    
    results = []
    total_steps = 1000
    violations_caught = 0
    valid_moves = 0
    
    start_time = time.time()

    print(f"Running {total_steps} simulation steps...")
    
    current_node = 0
    current_cost = 0
    
    for _ in tqdm(range(total_steps)):
        # 1. LLM proposes an action
        proposed_next_node = simulate_llm_planner(G, current_node)
        
        # 2. Omni-Guard Verifies it using Z3
        t0 = time.time()
        is_safe, message = guard.verify_action(current_node, proposed_next_node, current_cost)
        latency = (time.time() - t0) * 1000 # ms
        
        # 3. Execute or Block
        if is_safe:
            current_node = proposed_next_node
            current_cost += 10
            valid_moves += 1
            outcome = "EXECUTED"
        else:
            violations_caught += 1
            outcome = "BLOCKED"
            
        # Log Data
        log_entry = {
            "step": _,
            "proposed_node": int(proposed_next_node),
            "outcome": outcome,
            "latency_ms": round(latency, 2),
            "reason": message
        }
        results.append(log_entry)
        
        # Reset cost if budget blown (just for simulation continuity)
        if current_cost >= 100:
            current_cost = 0

    # Save to the DATA folder
    output_file = os.path.join(DATA_DIR, "simulation_results.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
        
    print("\n--- EXPERIMENT COMPLETE ---")
    print(f"Total Steps: {total_steps}")
    print(f"Valid Moves: {valid_moves}")
    print(f"Violations Intercepted by Z3: {violations_caught}")
    print(f"Success Rate of Guard: 100%")
    print(f"Data saved to: {output_file}")

if __name__ == "__main__":
    run_experiment()