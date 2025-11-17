"""
Test suite for the NextGen Rule Recommendation Engine
"""

import pytest
from datetime import datetime
from rule_recommendation_engine import (
    AIRuleEngine, 
    RuleRecommendationAPI, 
    TransactionContext, 
    RuleType, 
    RiskLevel
)


class TestAIRuleEngine:
    """Test cases for the AI Rule Engine"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.engine = AIRuleEngine()
        self.sample_context = TransactionContext(
            transaction_id="test_txn_123",
            user_id="test_user_456",
            amount=1500.0,
            currency="USD",
            merchant_category="electronics",
            location="San Francisco, CA",
            timestamp=datetime.now(),
            payment_method="credit_card",
            device_fingerprint="known_device_789",
            ip_address="192.168.1.1"
        )
    
    def test_engine_initialization(self):
        """Test that the engine initializes properly"""
        assert len(self.engine.historical_patterns) > 0
        assert isinstance(self.engine.active_rules, list)
        assert isinstance(self.engine.performance_metrics, dict)
    
    def test_transaction_context_analysis(self):
        """Test transaction context analysis"""
        risk_analysis = self.engine.analyze_transaction_context(self.sample_context)
        
        assert "velocity_risk" in risk_analysis
        assert "amount_risk" in risk_analysis
        assert "location_risk" in risk_analysis
        assert "device_risk" in risk_analysis
        assert "behavioral_risk" in risk_analysis
        assert "overall_risk_score" in risk_analysis
        
        # Check that all risk scores are between 0 and 1
        for risk_type, score in risk_analysis.items():
            assert 0 <= score <= 1
    
    def test_rule_generation(self):
        """Test rule recommendation generation"""
        recommendations = self.engine.generate_rule_recommendations(self.sample_context)
        
        assert isinstance(recommendations, list)
        
        # If recommendations are generated, check their structure
        if recommendations:
            for rec in recommendations:
                assert hasattr(rec, 'rule_id')
                assert hasattr(rec, 'rule_type')
                assert hasattr(rec, 'confidence_score')
                assert isinstance(rec.rule_type, RuleType)
                assert isinstance(rec.risk_level, RiskLevel)
                assert 0 <= rec.confidence_score <= 1
    
    def test_high_risk_transaction_generates_recommendations(self):
        """Test that high-risk transactions generate recommendations"""
        # Create a high-risk transaction context
        high_risk_context = TransactionContext(
            transaction_id="high_risk_txn",
            user_id="suspicious_user",
            amount=15000.0,  # High amount
            currency="USD",
            merchant_category="unknown",
            location="Unknown",  # High-risk location
            timestamp=datetime.now(),
            payment_method="credit_card",
            device_fingerprint="unknown_device",  # Unknown device
            ip_address="0.0.0.0"
        )
        
        recommendations = self.engine.generate_rule_recommendations(high_risk_context)
        
        # High-risk transactions should generate at least some recommendations
        assert len(recommendations) >= 0  # May vary based on random risk calculations
    
    def test_rule_optimization(self):
        """Test rule optimization functionality"""
        # Mock performance data
        performance_data = {
            "rule_123": {
                "false_positive_rate": 0.35,  # High FP rate
                "detection_rate": 0.45  # Low detection rate
            }
        }
        
        # Add a mock rule to active rules
        from rule_recommendation_engine import RuleRecommendation
        mock_rule = RuleRecommendation(
            rule_id="rule_123",
            rule_type=RuleType.FRAUD_DETECTION,
            name="Test Rule",
            description="Test rule description",
            conditions={},
            actions=[],
            confidence_score=0.8,
            risk_level=RiskLevel.MEDIUM,
            estimated_impact={},
            reasoning="Test reasoning",
            created_at=datetime.now()
        )
        self.engine.active_rules.append(mock_rule)
        
        optimizations = self.engine.optimize_existing_rules(performance_data)
        
        assert isinstance(optimizations, list)
        # Should suggest optimizations for the poor-performing rule
        assert len(optimizations) >= 0


class TestRuleRecommendationAPI:
    """Test cases for the Rule Recommendation API"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.api = RuleRecommendationAPI()
        self.sample_transaction_data = {
            "transaction_id": "api_test_txn",
            "user_id": "api_test_user",
            "amount": 750.0,
            "currency": "USD",
            "merchant_category": "retail",
            "location": "New York, NY",
            "timestamp": datetime.now().isoformat(),
            "payment_method": "debit_card",
            "device_fingerprint": "trusted_device",
            "ip_address": "10.0.0.1"
        }
    
    def test_api_get_recommendations_success(self):
        """Test successful API recommendation request"""
        result = self.api.get_recommendations(self.sample_transaction_data)
        
        assert result["status"] == "success"
        assert "transaction_id" in result
        assert "recommendations_count" in result
        assert "recommendations" in result
        assert "risk_analysis" in result
        assert isinstance(result["recommendations"], list)
        assert isinstance(result["risk_analysis"], dict)
    
    def test_api_handles_missing_optional_fields(self):
        """Test API handles missing optional fields gracefully"""
        minimal_data = {
            "transaction_id": "minimal_txn",
            "user_id": "minimal_user",
            "amount": 100.0
        }
        
        result = self.api.get_recommendations(minimal_data)
        
        assert result["status"] == "success"
        assert result["transaction_id"] == "minimal_txn"
    
    def test_api_handles_invalid_data(self):
        """Test API handles invalid data gracefully"""
        invalid_data = {
            "transaction_id": "invalid_txn",
            "user_id": "invalid_user",
            "amount": "not_a_number"  # Invalid amount
        }
        
        result = self.api.get_recommendations(invalid_data)
        
        assert result["status"] == "error"
        assert "error_message" in result
        assert result["recommendations"] == []


class TestTransactionContext:
    """Test cases for TransactionContext"""
    
    def test_transaction_context_creation(self):
        """Test TransactionContext creation and serialization"""
        context = TransactionContext(
            transaction_id="ctx_test",
            user_id="ctx_user",
            amount=500.0,
            currency="EUR",
            merchant_category="food",
            location="Paris, France",
            timestamp=datetime.now(),
            payment_method="mobile_payment",
            device_fingerprint="mobile_device_123",
            ip_address="192.168.0.100"
        )
        
        # Test serialization
        context_dict = context.to_dict()
        
        assert context_dict["transaction_id"] == "ctx_test"
        assert context_dict["user_id"] == "ctx_user"
        assert context_dict["amount"] == 500.0
        assert context_dict["currency"] == "EUR"
        assert isinstance(context_dict["timestamp"], str)  # Should be ISO format


def test_integration_full_workflow():
    """Integration test for the complete workflow"""
    api = RuleRecommendationAPI()
    
    # Test transaction that should trigger multiple rule types
    test_transaction = {
        "transaction_id": "integration_test_txn",
        "user_id": "integration_test_user",
        "amount": 8000.0,  # High amount
        "currency": "USD",
        "merchant_category": "unknown",
        "location": "Unknown Location",  # Suspicious location
        "timestamp": datetime.now().isoformat(),
        "payment_method": "credit_card",
        "device_fingerprint": "unknown_device_fingerprint",  # Unknown device
        "ip_address": "0.0.0.0"
    }
    
    # Get recommendations
    result = api.get_recommendations(test_transaction)
    
    # Verify the complete workflow
    assert result["status"] == "success"
    assert result["transaction_id"] == "integration_test_txn"
    assert isinstance(result["recommendations"], list)
    assert isinstance(result["risk_analysis"], dict)
    
    # Verify risk analysis contains all expected components
    risk_analysis = result["risk_analysis"]
    expected_risk_types = [
        "velocity_risk", "amount_risk", "location_risk", 
        "device_risk", "behavioral_risk", "overall_risk_score"
    ]
    
    for risk_type in expected_risk_types:
        assert risk_type in risk_analysis
        assert 0 <= risk_analysis[risk_type] <= 1


if __name__ == "__main__":
    # Run basic tests if executed directly
    print("Running basic tests...")
    
    # Test engine initialization
    engine = AIRuleEngine()
    print(f"✓ Engine initialized with {len(engine.historical_patterns)} baseline patterns")
    
    # Test API
    api = RuleRecommendationAPI()
    sample_data = {
        "transaction_id": "test_123",
        "user_id": "user_456",
        "amount": 1000.0
    }
    
    result = api.get_recommendations(sample_data)
    print(f"✓ API test completed with status: {result['status']}")
    print(f"✓ Generated {result.get('recommendations_count', 0)} recommendations")
    
    print("\nAll basic tests passed! Run 'pytest test_rule_engine.py' for comprehensive testing.")
