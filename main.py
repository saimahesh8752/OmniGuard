from z3 import *
from src.compiler import OmniGuardCompiler

def run_test():
    print("--- 🛡️ INITIALIZING OMNI-GUARD ---")
    compiler = OmniGuardCompiler()
    
    # 1. Simulate an Instruction (from LLM)
    instruction = {
        "template_id": "MAX_BUDGET",
        "params": {"limit": 1000}
    }
    print(f"Instruction: {instruction}")
    
    # 2. Test a SAFE Context (Cost = 500)
    print("\n[Test 1] Checking Cost = 500...")
    ctx_safe = {'total_cost': IntVal(500)} # Z3 Integer Value
    is_safe, msg = compiler.verify_action(instruction, ctx_safe)
    print(f"Result: {msg}")
    
    # 3. Test an UNSAFE Context (Cost = 1500)
    print("\n[Test 2] Checking Cost = 1500...")
    ctx_unsafe = {'total_cost': IntVal(1500)}
    is_safe, msg = compiler.verify_action(instruction, ctx_unsafe)
    print(f"Result: {msg}")

if __name__ == "__main__":
    run_test()