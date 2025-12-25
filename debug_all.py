from z3 import *

print("--- 🔍 STARTING DIAGNOSTIC TEST ---")

# 1. DEFINE THE GRAMMAR DIRECTLY
def budget_rule(ctx, params):
    # Rule: cost <= limit
    # We print what's happening to debug
    print(f"   [Logic Trace] Checking: {ctx['total_cost']} <= {params['limit']}")
    return ctx['total_cost'] <= params['limit']

# 2. DEFINE THE COMPILER LOGIC DIRECTLY
def verify_action(instruction, context):
    s = Solver()
    
    # Get the rule logic
    constraint = budget_rule(context, instruction['params'])
    
    # We want to find a VIOLATION.
    # So we tell Z3: "Assume the Rule is NOT True."
    s.add(Not(constraint))
    
    # If Z3 can find a solution (SAT), it means the Rule CAN be broken -> Violation.
    result = s.check()
    
    if result == sat:
        return False, "🛑 VIOLATION (Z3 found a counter-example)"
    else:
        return True, "✅ VERIFIED (Z3 proved it is impossible to break)"

# 3. RUN THE TESTS
instruction = {"params": {"limit": 1000}}

# --- TEST 1: SAFE (500) ---
print("\n--- TEST 1: SAFE (Cost 500) ---")
ctx_safe = {'total_cost': IntVal(500)}
is_safe_1, msg_1 = verify_action(instruction, ctx_safe)
print(f"RESULT: {msg_1}")

# --- TEST 2: UNSAFE (1500) ---
print("\n--- TEST 2: UNSAFE (Cost 1500) ---")
ctx_unsafe = {'total_cost': IntVal(1500)}
is_safe_2, msg_2 = verify_action(instruction, ctx_unsafe)
print(f"RESULT: {msg_2}")