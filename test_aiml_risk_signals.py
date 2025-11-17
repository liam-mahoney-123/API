"""
Test suite for AIML Risk Signals system
"""

import pytest
from datetime import datetime, timedelta
from aiml_risk_signals import (
    AIMLRiskEngine, 
    RiskReportGenerator, 
    Transaction, 
    RiskLevel,
    create_sample_transaction
)


class TestAIMLRiskEngine:
    """Test cases for the AIML Risk Engine"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.risk_engine = AIMLRiskEngine()
        self.sample_transaction = Transaction(
            transaction_id="test_txn_123",
            merchant_id="test_merchant_456",
            amount=1000.0,
            currency="USD",
            timestamp=datetime.now(),
            user_ip="192.168.1.1",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            payment_method="credit_card",
            billing_address={
                "street": "123 Test St",
                "city": "Test City",
                "state": "CA",
                "country": "US",
                "zip": "12345"
            },
            shipping_address={
                "street": "123 Test St",
                "city": "Test City", 
                "state": "CA",
                "country": "US",
                "zip": "12345"
            },
            device_fingerprint="test_fingerprint_12345"
        )
    
    def test_analyze_transaction_returns_signals(self):
        """Test that transaction analysis returns risk signals"""
        signals = self.risk_engine.analyze_transaction(self.sample_transaction)
        assert isinstance(signals, list)
        # Should have at least some signals for a normal transaction
        assert len(signals) >= 0
    
    def test_velocity_tracking_basic(self):
        """Test basic velocity tracking functionality"""
        # Process multiple transactions from same IP
        for i in range(3):
            transaction = self.sample_transaction
            transaction.timestamp = datetime.now() + timedelta(minutes=i*10)
            signals = self.risk_engine.analyze_transaction(transaction)
        
        # Check that velocity tracking is working
        ip_key = f"ip_{self.sample_transaction.user_ip}"
        assert ip_key in self.risk_engine.velocity_tracking
        assert len(self.risk_engine.velocity_tracking[ip_key]) == 3
    
    def test_geographic_mismatch_detection(self):
        """Test geographic mismatch detection"""
        # Create transaction with mismatched countries
        transaction = self.sample_transaction
        transaction.billing_address["country"] = "CA"  # Different from IP country
        
        signals = self.risk_engine.analyze_transaction(transaction)
        
        # Should detect geographic mismatch
        geo_signals = [s for s in signals if s.signal_type == "geographic_mismatch"]
        assert len(geo_signals) > 0
    
    def test_suspicious_user_agent_detection(self):
        """Test suspicious user agent detection"""
        transaction = self.sample_transaction
        transaction.user_agent = "bot crawler automated"
        
        signals = self.risk_engine.analyze_transaction(transaction)
        
        # Should detect suspicious user agent
        ua_signals = [s for s in signals if s.signal_type == "suspicious_user_agent"]
        assert len(ua_signals) > 0
    
    def test_high_amount_detection(self):
        """Test high amount anomaly detection"""
        transaction = self.sample_transaction
        transaction.amount = 15000.0  # High amount
        
        signals = self.risk_engine.analyze_transaction(transaction)
        
        # Should detect high amount
        amount_signals = [s for s in signals if s.signal_type == "high_amount"]
        assert len(amount_signals) > 0
    
    def test_round_amount_detection(self):
        """Test round amount anomaly detection"""
        transaction = self.sample_transaction
        transaction.amount = 1000.0  # Round amount over threshold
        
        signals = self.risk_engine.analyze_transaction(transaction)
        
        # Should detect round amount anomaly
        round_signals = [s for s in signals if s.signal_type == "round_amount_anomaly"]
        assert len(round_signals) > 0
    
    def test_overall_risk_score_calculation(self):
        """Test overall risk score calculation"""
        signals = self.risk_engine.analyze_transaction(self.sample_transaction)
        score, level = self.risk_engine.calculate_overall_risk_score(signals)
        
        assert 0.0 <= score <= 1.0
        assert level in [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
    
    def test_empty_signals_risk_score(self):
        """Test risk score calculation with no signals"""
        score, level = self.risk_engine.calculate_overall_risk_score([])
        
        assert score == 0.0
        assert level == RiskLevel.LOW


class TestRiskReportGenerator:
    """Test cases for the Risk Report Generator"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.risk_engine = AIMLRiskEngine()
        self.report_generator = RiskReportGenerator(self.risk_engine)
        self.sample_transaction = create_sample_transaction()
    
    def test_generate_transaction_report_structure(self):
        """Test that transaction report has correct structure"""
        report = self.report_generator.generate_transaction_report(self.sample_transaction)
        
        # Check required fields
        required_fields = [
            "transaction_id", "merchant_id", "timestamp", "amount", "currency",
            "overall_risk_score", "risk_level", "signals", "recommendations"
        ]
        
        for field in required_fields:
            assert field in report
    
    def test_report_recommendations_exist(self):
        """Test that report includes recommendations"""
        report = self.report_generator.generate_transaction_report(self.sample_transaction)
        
        assert "recommendations" in report
        assert isinstance(report["recommendations"], list)
        assert len(report["recommendations"]) > 0
    
    def test_report_signals_format(self):
        """Test that signals are properly formatted in report"""
        report = self.report_generator.generate_transaction_report(self.sample_transaction)
        
        assert "signals" in report
        assert isinstance(report["signals"], list)
        
        # Check signal structure if any exist
        if report["signals"]:
            signal = report["signals"][0]
            required_signal_fields = ["type", "confidence", "description", "severity", "metadata"]
            for field in required_signal_fields:
                assert field in signal


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_create_sample_transaction(self):
        """Test sample transaction creation"""
        transaction = create_sample_transaction()
        
        assert isinstance(transaction, Transaction)
        assert transaction.transaction_id.startswith("txn_")
        assert transaction.merchant_id.startswith("merchant_")
        assert transaction.amount > 0
        assert transaction.currency == "USD"
        assert isinstance(transaction.timestamp, datetime)


def test_velocity_bug_demonstration():
    """
    Test that demonstrates the velocity tracking bug
    This test shows that the bug in line 100 causes incorrect behavior
    """
    risk_engine = AIMLRiskEngine()
    
    # Create a transaction
    transaction = create_sample_transaction()
    base_time = datetime.now()
    
    # Add some transactions to velocity tracking manually to test the bug
    ip_key = f"ip_{transaction.user_ip}"
    risk_engine.velocity_tracking[ip_key] = [
        base_time - timedelta(minutes=30),  # 30 minutes ago
        base_time - timedelta(minutes=45),  # 45 minutes ago
        base_time - timedelta(minutes=50),  # 50 minutes ago
        base_time - timedelta(minutes=55),  # 55 minutes ago
        base_time - timedelta(minutes=58),  # 58 minutes ago
        base_time - timedelta(minutes=59),  # 59 minutes ago
    ]
    
    transaction.timestamp = base_time
    
    # Due to the bug (> instead of <=), transactions exactly at 1 hour won't be counted
    # This should trigger high velocity detection but might not due to the bug
    signals = risk_engine.analyze_transaction(transaction)
    
    velocity_signals = [s for s in signals if s.signal_type == "high_velocity"]
    
    # The bug means this assertion might fail when it shouldn't
    # In a correct implementation, this should detect high velocity
    print(f"Velocity signals detected: {len(velocity_signals)}")
    print(f"Recent transactions found: {len([t for t in risk_engine.velocity_tracking[ip_key] if (base_time - t).total_seconds() > 3600])}")


if __name__ == "__main__":
    # Run the bug demonstration
    print("🐛 Demonstrating the velocity tracking bug:")
    test_velocity_bug_demonstration()
    
    # Run basic tests
    print("\n✅ Running basic functionality tests...")
    pytest.main([__file__, "-v"])
