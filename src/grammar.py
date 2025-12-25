"""
OmniGuard Constraint Grammar
============================
This module defines the library of valid safety templates.
It acts as the "Type System" for the LLM, ensuring that
any generated constraint maps to a valid Z3 logical expression.
"""

from z3 import *

class ConstraintLibrary:
    """
    A registry of formally verified safety templates.
    """
    def __init__(self):
        self.templates = {
            "MAX_BUDGET": {
                "description": "Ensures total cost does not exceed a hard limit.",
                "logic": lambda ctx, params: ctx['total_cost'] <= params['limit']
            },
            "CAPACITY_LIMIT": {
                "description": "Ensures flow quantity does not exceed link capacity.",
                "logic": lambda ctx, params: ctx['quantity'] <= params['max_cap']
            },
            "AVOID_LOCATION": {
                "description": "Ensures a specific node is NOT present in the path.",
                # Logic: We assume ctx['node_in_path'] is a function mapping node_name -> Bool
                "logic": lambda ctx, params: Not(ctx['node_in_path'](params['location']))
            }
        }

    def get_template(self, template_id):
        """
        Retrieves a template by ID. Returns None if invalid.
        """
        if template_id not in self.templates:
            return None
        return self.templates[template_id]

    def list_templates(self):
        """Helper for the LLM prompt to see available tools."""
        return [f"{k}: {v['description']}" for k, v in self.templates.items()]