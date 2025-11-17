"""
GenAI-powered Rule Authoring System for Fraud Detection
This module provides AI-driven capabilities for creating, explaining, optimizing, and suggesting rules.
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class RuleType(Enum):
    FRAUD_DETECTION = "fraud_detection"
    RISK_ASSESSMENT = "risk_assessment"
    COMPLIANCE = "compliance"
    TRANSACTION_MONITORING = "transaction_monitoring"

class RulePriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class RuleCondition:
    field: str
    operator: str
    value: Any
    logical_operator: str = "AND"

@dataclass
class Rule:
    id: str
    name: str
    description: str
    rule_type: RuleType
    priority: RulePriority
    conditions: List[RuleCondition]
    action: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    confidence_score: float = 0.0

class GenAIRuleEngine:
    """
    GenAI-powered rule engine for fraud detection and risk assessment.
    Provides intelligent rule creation, optimization, and suggestion capabilities.
    """
    
    def __init__(self):
        self.rules: Dict[str, Rule] = {}
        self.rule_templates = self._load_rule_templates()
        self.ai_suggestions_cache = {}
    
    def _load_rule_templates(self) -> Dict[str, Dict]:
        """Load predefined rule templates for common fraud patterns"""
        return {
            "high_velocity_transactions": {
                "name": "High Velocity Transaction Detection",
                "description": "Detects unusually high transaction frequency",
                "conditions": [
                    {"field": "transaction_count", "operator": ">", "value": 10},
                    {"field": "time_window", "operator": "<=", "value": 300}  # 5 minutes
                ]
            },
            "unusual_amount_pattern": {
                "name": "Unusual Amount Pattern",
                "description": "Identifies transactions with suspicious amount patterns",
                "conditions": [
                    {"field": "amount", "operator": ">", "value": 10000},
                    {"field": "user_avg_transaction", "operator": "<", "value": 100}
                ]
            }
        }
    
    def create_rule_with_ai(self, rule_request: str, context: Dict[str, Any]) -> Rule:
        """
        Create a new rule using GenAI capabilities based on natural language input.
        
        Args:
            rule_request: Natural language description of the desired rule
            context: Additional context for rule creation
            
        Returns:
            Generated Rule object
        """
        # Simulate AI processing of natural language rule request
        rule_id = f"rule_{len(self.rules) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Parse rule request using simple keyword matching (simulating AI)
        rule_type = self._extract_rule_type(rule_request)
        priority = self._extract_priority(rule_request)
        conditions = self._generate_conditions_from_text(rule_request, context)
        
        # BUG: Missing validation for empty conditions list
        # This could cause issues when rules are created without proper conditions
        rule = Rule(
            id=rule_id,
            name=self._generate_rule_name(rule_request),
            description=rule_request,
            rule_type=rule_type,
            priority=priority,
            conditions=conditions,
            action=self._determine_action(priority),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            confidence_score=self._calculate_confidence_score(conditions, context)
        )
        
        self.rules[rule_id] = rule
        return rule
    
    def _extract_rule_type(self, text: str) -> RuleType:
        """Extract rule type from natural language text"""
        text_lower = text.lower()
        if "fraud" in text_lower or "suspicious" in text_lower:
            return RuleType.FRAUD_DETECTION
        elif "risk" in text_lower:
            return RuleType.RISK_ASSESSMENT
        elif "compliance" in text_lower or "regulation" in text_lower:
            return RuleType.COMPLIANCE
        else:
            return RuleType.TRANSACTION_MONITORING
    
    def _extract_priority(self, text: str) -> RulePriority:
        """Extract priority level from natural language text"""
        text_lower = text.lower()
        if "critical" in text_lower or "urgent" in text_lower:
            return RulePriority.CRITICAL
        elif "high" in text_lower or "important" in text_lower:
            return RulePriority.HIGH
        elif "low" in text_lower:
            return RulePriority.LOW
        else:
            return RulePriority.MEDIUM
    
    def _generate_conditions_from_text(self, text: str, context: Dict[str, Any]) -> List[RuleCondition]:
        """Generate rule conditions from natural language text"""
        conditions = []
        
        # Simple pattern matching for common conditions
        amount_pattern = re.search(r'amount.*?(\d+)', text.lower())
        if amount_pattern:
            amount_value = int(amount_pattern.group(1))
            conditions.append(RuleCondition(
                field="transaction_amount",
                operator=">",
                value=amount_value
            ))
        
        # Check for velocity patterns
        if "frequent" in text.lower() or "velocity" in text.lower():
            conditions.append(RuleCondition(
                field="transaction_count",
                operator=">",
                value=5,
                logical_operator="AND"
            ))
            conditions.append(RuleCondition(
                field="time_window",
                operator="<=",
                value=600  # 10 minutes
            ))
        
        # BUG: No validation if conditions list is empty
        # This could result in rules with no actual conditions being created
        return conditions
    
    def _generate_rule_name(self, request: str) -> str:
        """Generate a descriptive name for the rule"""
        # Simple name generation based on keywords
        words = request.split()[:5]  # Take first 5 words
        return " ".join(word.capitalize() for word in words if len(word) > 2)
    
    def _determine_action(self, priority: RulePriority) -> str:
        """Determine the action based on rule priority"""
        action_map = {
            RulePriority.CRITICAL: "BLOCK_TRANSACTION",
            RulePriority.HIGH: "REQUIRE_MANUAL_REVIEW",
            RulePriority.MEDIUM: "FLAG_FOR_REVIEW",
            RulePriority.LOW: "LOG_EVENT"
        }
        return action_map.get(priority, "LOG_EVENT")
    
    def _calculate_confidence_score(self, conditions: List[RuleCondition], context: Dict[str, Any]) -> float:
        """Calculate confidence score for the generated rule"""
        if not conditions:  # BUG: This check happens too late, after rule creation
            return 0.1  # Very low confidence for rules without conditions
        
        base_score = 0.7
        # Increase confidence based on number of conditions
        condition_bonus = min(len(conditions) * 0.1, 0.2)
        
        # Increase confidence if context provides historical data
        context_bonus = 0.1 if context.get("historical_data") else 0.0
        
        return min(base_score + condition_bonus + context_bonus, 1.0)
    
    def optimize_rule(self, rule_id: str) -> Dict[str, Any]:
        """
        Use GenAI to optimize an existing rule for better performance and accuracy.
        """
        if rule_id not in self.rules:
            raise ValueError(f"Rule {rule_id} not found")
        
        rule = self.rules[rule_id]
        optimization_suggestions = []
        
        # Analyze rule conditions for optimization opportunities
        for condition in rule.conditions:
            if condition.operator == ">" and isinstance(condition.value, (int, float)):
                # Suggest threshold optimization
                optimized_value = condition.value * 0.9  # Reduce threshold by 10%
                optimization_suggestions.append({
                    "type": "threshold_optimization",
                    "field": condition.field,
                    "current_value": condition.value,
                    "suggested_value": optimized_value,
                    "reason": "Lower threshold may catch more edge cases"
                })
        
        # BUG: The optimization doesn't actually apply the changes
        # It only suggests them but doesn't update the rule
        return {
            "rule_id": rule_id,
            "current_confidence": rule.confidence_score,
            "suggestions": optimization_suggestions,
            "estimated_improvement": len(optimization_suggestions) * 0.05
        }
    
    def explain_rule(self, rule_id: str) -> str:
        """
        Generate a human-readable explanation of what the rule does.
        """
        if rule_id not in self.rules:
            return "Rule not found"
        
        rule = self.rules[rule_id]
        explanation = f"Rule '{rule.name}' is a {rule.rule_type.value} rule with {rule.priority.name} priority.\n\n"
        explanation += f"Description: {rule.description}\n\n"
        explanation += "This rule triggers when:\n"
        
        for i, condition in enumerate(rule.conditions):
            logical_op = "" if i == 0 else f" {condition.logical_operator} "
            explanation += f"{logical_op}{condition.field} {condition.operator} {condition.value}\n"
        
        explanation += f"\nWhen triggered, the system will: {rule.action}"
        explanation += f"\nConfidence Score: {rule.confidence_score:.2f}"
        
        return explanation
    
    def suggest_new_rules(self, transaction_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze transaction data and suggest new rules using GenAI insights.
        """
        suggestions = []
        
        if not transaction_data:
            return suggestions
        
        # Analyze patterns in transaction data
        amounts = [t.get("amount", 0) for t in transaction_data]
        avg_amount = sum(amounts) / len(amounts)
        max_amount = max(amounts)
        
        # Suggest rule for unusually high amounts
        if max_amount > avg_amount * 5:
            suggestions.append({
                "rule_type": "fraud_detection",
                "name": "High Amount Transaction Alert",
                "description": f"Flag transactions above {avg_amount * 3:.2f}",
                "confidence": 0.8,
                "conditions": [
                    {"field": "amount", "operator": ">", "value": avg_amount * 3}
                ]
            })
        
        # BUG: The function doesn't handle the case where all amounts are 0
        # This could cause division by zero or misleading suggestions
        
        return suggestions
    
    def evaluate_rule_performance(self, rule_id: str, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate how well a rule performs against test data.
        """
        if rule_id not in self.rules:
            return {"error": "Rule not found"}
        
        rule = self.rules[rule_id]
        matches = 0
        total_tests = len(test_data)
        
        for data_point in test_data:
            if self._evaluate_conditions(rule.conditions, data_point):
                matches += 1
        
        accuracy = matches / total_tests if total_tests > 0 else 0
        
        return {
            "rule_id": rule_id,
            "total_tests": total_tests,
            "matches": matches,
            "accuracy": accuracy,
            "performance_rating": "Good" if accuracy > 0.7 else "Needs Improvement"
        }
    
    def _evaluate_conditions(self, conditions: List[RuleCondition], data: Dict[str, Any]) -> bool:
        """Evaluate if data matches rule conditions"""
        if not conditions:  # BUG: Rules with no conditions always return True
            return True
        
        results = []
        for condition in conditions:
            field_value = data.get(condition.field)
            if field_value is None:
                results.append(False)
                continue
            
            if condition.operator == ">":
                results.append(field_value > condition.value)
            elif condition.operator == "<":
                results.append(field_value < condition.value)
            elif condition.operator == "==":
                results.append(field_value == condition.value)
            elif condition.operator == ">=":
                results.append(field_value >= condition.value)
            elif condition.operator == "<=":
                results.append(field_value <= condition.value)
            else:
                results.append(False)
        
        # Simple AND logic for all conditions
        return all(results)

# Example usage and demonstration
if __name__ == "__main__":
    # Initialize the GenAI Rule Engine
    engine = GenAIRuleEngine()
    
    # Example 1: Create a rule using natural language
    rule_request = "Create a high priority fraud detection rule for transactions above 5000"
    context = {"historical_data": True, "user_type": "premium"}
    
    new_rule = engine.create_rule_with_ai(rule_request, context)
    print(f"Created rule: {new_rule.id}")
    print(f"Rule name: {new_rule.name}")
    print(f"Conditions: {len(new_rule.conditions)}")
    
    # Example 2: Explain the rule
    explanation = engine.explain_rule(new_rule.id)
    print(f"\nRule Explanation:\n{explanation}")
    
    # Example 3: Optimize the rule
    optimization = engine.optimize_rule(new_rule.id)
    print(f"\nOptimization suggestions: {len(optimization['suggestions'])}")
    
    # Example 4: Test rule performance
    test_data = [
        {"transaction_amount": 6000, "user_id": "123"},
        {"transaction_amount": 2000, "user_id": "456"},
        {"transaction_amount": 8000, "user_id": "789"}
    ]
    
    performance = engine.evaluate_rule_performance(new_rule.id, test_data)
    print(f"\nRule Performance: {performance['performance_rating']}")
    print(f"Accuracy: {performance['accuracy']:.2f}")
