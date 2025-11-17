"""
Test file to demonstrate the bugs in the GenAI Rule Engine
"""

from genai_rule_engine import GenAIRuleEngine, RuleType, RulePriority

def test_empty_conditions_bug():
    """
    Test that demonstrates the bug where rules can be created with no conditions
    """
    print("=== Testing Empty Conditions Bug ===")
    engine = GenAIRuleEngine()
    
    # This request doesn't contain any recognizable patterns for conditions
    rule_request = "Create a rule for monitoring"
    context = {"user_type": "standard"}
    
    # BUG: This will create a rule with empty conditions list
    rule = engine.create_rule_with_ai(rule_request, context)
    
    print(f"Rule created: {rule.id}")
    print(f"Number of conditions: {len(rule.conditions)}")
    print(f"Confidence score: {rule.confidence_score}")
    
    # BUG: Rules with no conditions will always match any data
    test_data = {"transaction_amount": 100, "user_id": "test"}
    matches = engine._evaluate_conditions(rule.conditions, test_data)
    print(f"Empty rule matches test data: {matches}")  # This will be True!
    
    return rule

def test_optimization_bug():
    """
    Test that demonstrates the bug where optimization suggestions aren't applied
    """
    print("\n=== Testing Optimization Bug ===")
    engine = GenAIRuleEngine()
    
    # Create a rule with conditions
    rule_request = "Create a fraud detection rule for transactions above 1000"
    context = {"historical_data": True}
    
    rule = engine.create_rule_with_ai(rule_request, context)
    original_conditions = rule.conditions.copy()
    
    print(f"Original rule conditions: {len(original_conditions)}")
    if original_conditions:
        print(f"First condition value: {original_conditions[0].value}")
    
    # Get optimization suggestions
    optimization = engine.optimize_rule(rule.id)
    print(f"Optimization suggestions: {len(optimization['suggestions'])}")
    
    # BUG: The rule conditions remain unchanged after optimization
    current_conditions = engine.rules[rule.id].conditions
    if current_conditions and original_conditions:
        print(f"Condition value after optimization: {current_conditions[0].value}")
        print(f"Values are the same: {current_conditions[0].value == original_conditions[0].value}")
    
    return rule, optimization

def test_division_by_zero_bug():
    """
    Test that demonstrates potential division by zero in rule suggestions
    """
    print("\n=== Testing Division by Zero Bug ===")
    engine = GenAIRuleEngine()
    
    # Transaction data with all zero amounts
    transaction_data = [
        {"amount": 0, "user_id": "user1"},
        {"amount": 0, "user_id": "user2"},
        {"amount": 0, "user_id": "user3"}
    ]
    
    try:
        suggestions = engine.suggest_new_rules(transaction_data)
        print(f"Suggestions generated: {len(suggestions)}")
        
        # The bug might not cause an immediate crash but could lead to misleading suggestions
        amounts = [t.get("amount", 0) for t in transaction_data]
        avg_amount = sum(amounts) / len(amounts)  # This will be 0
        max_amount = max(amounts)  # This will be 0
        
        print(f"Average amount: {avg_amount}")
        print(f"Max amount: {max_amount}")
        
        # BUG: When max_amount is 0 and avg_amount is 0, 
        # the condition max_amount > avg_amount * 5 becomes 0 > 0, which is False
        # But this could still create misleading rules in other scenarios
        
    except Exception as e:
        print(f"Error occurred: {e}")
    
    return suggestions

def demonstrate_all_bugs():
    """
    Run all bug demonstrations
    """
    print("GenAI Rule Engine Bug Demonstration")
    print("=" * 50)
    
    # Bug 1: Empty conditions
    empty_rule = test_empty_conditions_bug()
    
    # Bug 2: Optimization not applied
    rule, optimization = test_optimization_bug()
    
    # Bug 3: Division by zero potential
    suggestions = test_division_by_zero_bug()
    
    print("\n=== Summary of Bugs Found ===")
    print("1. Rules can be created with no conditions, making them match everything")
    print("2. Rule optimization suggestions are generated but never applied")
    print("3. Rule suggestion logic doesn't handle edge cases with zero amounts properly")
    print("4. Rules with empty conditions always evaluate to True in condition checking")

if __name__ == "__main__":
    demonstrate_all_bugs()
