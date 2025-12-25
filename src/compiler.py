"""
OmniGuard Runtime Compiler
==========================
Translates semantic instructions (JSON) into formal Z3 constraints.
"""
from z3 import *
from src.grammar import ConstraintLibrary

class OmniGuardCompiler:
    def __init__(self):
        self.library = ConstraintLibrary()
        self.solver = Solver()

    def verify_action(self, instruction_json, context):
        self.solver.reset()
        
        # 1. Load Context
        z3_ctx = context 
        
        # 2. Get Template
        template_id = instruction_json.get('template_id')
        params = instruction_json.get('params')
        
        template = self.library.get_template(template_id)
        if not template:
            return False, f"CRITICAL ERROR: Unknown Template ID '{template_id}'"
            
        try:
            # 3. Apply Logic
            constraint = template['logic'](z3_ctx, params)
            
            # --- THE PROVEN LOGIC ---
            # We look for a counter-example (VIOLATION)
            self.solver.add(Not(constraint))
            
            if self.solver.check() == sat:
                return False, f"VIOLATION: Action breaches '{template_id}' with params {params}"
            else:
                return True, f"VERIFIED: Action adheres to '{template_id}'"

        except Exception as e:
            return False, f"COMPILER CRASH: {str(e)}"