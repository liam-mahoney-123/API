"""
AIML Risk Signals for Web Merchants
Generative AI-driven fraud detection and risk management system
"""

import json
import random
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Transaction:
    transaction_id: str
    merchant_id: str
    amount: float
    currency: str
    timestamp: datetime
    user_ip: str
    user_agent: str
    payment_method: str
    billing_address: Dict[str, str]
    shipping_address: Dict[str, str]
    device_fingerprint: str


@dataclass
class RiskSignal:
    signal_type: str
    confidence: float
    description: str
    severity: RiskLevel
    metadata: Dict


class AIMLRiskEngine:
    """
    AI/ML-powered risk detection engine for web merchants
    Uses generative AI to analyze transaction patterns and detect fraud
    """
    
    def __init__(self):
        self.risk_models = {}
        self.transaction_history = []
        self.blacklisted_ips = set()
        self.velocity_tracking = {}
        
    def analyze_transaction(self, transaction: Transaction) -> List[RiskSignal]:
        """
        Analyze a transaction and generate risk signals using AI/ML models
        """
        signals = []
        
        # Velocity-based risk signals
        velocity_signals = self._check_velocity_patterns(transaction)
        signals.extend(velocity_signals)
        
        # Geographic risk signals
        geo_signals = self._analyze_geographic_patterns(transaction)
        signals.extend(geo_signals)
        
        # Device fingerprinting signals
        device_signals = self._analyze_device_patterns(transaction)
        signals.extend(device_signals)
        
        # AI-generated behavioral signals
        behavioral_signals = self._generate_behavioral_signals(transaction)
        signals.extend(behavioral_signals)
        
        # Amount-based anomaly detection
        amount_signals = self._detect_amount_anomalies(transaction)
        signals.extend(amount_signals)
        
        return signals
    
    def _check_velocity_patterns(self, transaction: Transaction) -> List[RiskSignal]:
        """Check for suspicious velocity patterns"""
        signals = []
        current_time = transaction.timestamp
        
        # Track transactions per IP
        ip_key = f"ip_{transaction.user_ip}"
        if ip_key not in self.velocity_tracking:
            self.velocity_tracking[ip_key] = []
        
        # BUG: This condition has a logical error - it should be >= not >
        # This will cause the velocity check to miss transactions exactly at the threshold
        recent_transactions = [
            t for t in self.velocity_tracking[ip_key] 
            if (current_time - t).total_seconds() > 3600  # Should be <= 3600
        ]
        
        self.velocity_tracking[ip_key].append(current_time)
        
        if len(recent_transactions) > 5:
            signals.append(RiskSignal(
                signal_type="high_velocity",
                confidence=0.85,
                description=f"High transaction velocity from IP {transaction.user_ip}",
                severity=RiskLevel.HIGH,
                metadata={"transaction_count": len(recent_transactions), "timeframe": "1_hour"}
            ))
        
        return signals
    
    def _analyze_geographic_patterns(self, transaction: Transaction) -> List[RiskSignal]:
        """Analyze geographic risk patterns"""
        signals = []
        
        # Simulate IP geolocation
        ip_country = self._get_ip_country(transaction.user_ip)
        billing_country = transaction.billing_address.get("country", "Unknown")
        
        if ip_country != billing_country:
            signals.append(RiskSignal(
                signal_type="geographic_mismatch",
                confidence=0.7,
                description=f"IP country ({ip_country}) differs from billing country ({billing_country})",
                severity=RiskLevel.MEDIUM,
                metadata={"ip_country": ip_country, "billing_country": billing_country}
            ))
        
        # Check for high-risk countries
        high_risk_countries = ["XX", "YY", "ZZ"]  # Placeholder country codes
        if ip_country in high_risk_countries:
            signals.append(RiskSignal(
                signal_type="high_risk_geography",
                confidence=0.9,
                description=f"Transaction from high-risk country: {ip_country}",
                severity=RiskLevel.HIGH,
                metadata={"country": ip_country}
            ))
        
        return signals
    
    def _analyze_device_patterns(self, transaction: Transaction) -> List[RiskSignal]:
        """Analyze device fingerprinting patterns"""
        signals = []
        
        # Check for suspicious user agents
        suspicious_agents = ["bot", "crawler", "scraper", "automated"]
        user_agent_lower = transaction.user_agent.lower()
        
        for suspicious in suspicious_agents:
            if suspicious in user_agent_lower:
                signals.append(RiskSignal(
                    signal_type="suspicious_user_agent",
                    confidence=0.8,
                    description=f"Suspicious user agent detected: {suspicious}",
                    severity=RiskLevel.HIGH,
                    metadata={"user_agent": transaction.user_agent}
                ))
                break
        
        # Device fingerprint analysis
        if len(transaction.device_fingerprint) < 10:
            signals.append(RiskSignal(
                signal_type="weak_device_fingerprint",
                confidence=0.6,
                description="Weak or missing device fingerprint",
                severity=RiskLevel.MEDIUM,
                metadata={"fingerprint_length": len(transaction.device_fingerprint)}
            ))
        
        return signals
    
    def _generate_behavioral_signals(self, transaction: Transaction) -> List[RiskSignal]:
        """Generate AI-powered behavioral risk signals"""
        signals = []
        
        # Simulate AI model predictions
        behavioral_score = self._calculate_behavioral_score(transaction)
        
        if behavioral_score > 0.8:
            signals.append(RiskSignal(
                signal_type="anomalous_behavior",
                confidence=behavioral_score,
                description="AI model detected anomalous behavioral patterns",
                severity=RiskLevel.HIGH,
                metadata={"behavioral_score": behavioral_score}
            ))
        elif behavioral_score > 0.6:
            signals.append(RiskSignal(
                signal_type="suspicious_behavior",
                confidence=behavioral_score,
                description="AI model detected suspicious behavioral patterns",
                severity=RiskLevel.MEDIUM,
                metadata={"behavioral_score": behavioral_score}
            ))
        
        return signals
    
    def _detect_amount_anomalies(self, transaction: Transaction) -> List[RiskSignal]:
        """Detect anomalous transaction amounts"""
        signals = []
        
        # Check for round numbers (often fraudulent)
        if transaction.amount % 100 == 0 and transaction.amount > 500:
            signals.append(RiskSignal(
                signal_type="round_amount_anomaly",
                confidence=0.5,
                description=f"Suspicious round amount: {transaction.amount}",
                severity=RiskLevel.LOW,
                metadata={"amount": transaction.amount}
            ))
        
        # Check for unusually high amounts
        if transaction.amount > 10000:
            signals.append(RiskSignal(
                signal_type="high_amount",
                confidence=0.7,
                description=f"Unusually high transaction amount: {transaction.amount}",
                severity=RiskLevel.MEDIUM,
                metadata={"amount": transaction.amount}
            ))
        
        return signals
    
    def _get_ip_country(self, ip_address: str) -> str:
        """Simulate IP geolocation lookup"""
        # Simple hash-based simulation
        hash_val = int(hashlib.md5(ip_address.encode()).hexdigest()[:8], 16)
        countries = ["US", "CA", "GB", "DE", "FR", "JP", "AU", "BR", "IN", "CN"]
        return countries[hash_val % len(countries)]
    
    def _calculate_behavioral_score(self, transaction: Transaction) -> float:
        """Simulate AI behavioral scoring"""
        # Simple heuristic-based scoring for simulation
        score = 0.0
        
        # Time-based factors
        hour = transaction.timestamp.hour
        if hour < 6 or hour > 22:  # Late night transactions
            score += 0.2
        
        # Amount-based factors
        if transaction.amount > 5000:
            score += 0.3
        
        # Payment method factors
        if transaction.payment_method in ["prepaid_card", "cryptocurrency"]:
            score += 0.4
        
        # Add some randomness to simulate AI model uncertainty
        score += random.uniform(-0.1, 0.1)
        
        return min(max(score, 0.0), 1.0)
    
    def calculate_overall_risk_score(self, signals: List[RiskSignal]) -> Tuple[float, RiskLevel]:
        """Calculate overall risk score from individual signals"""
        if not signals:
            return 0.0, RiskLevel.LOW
        
        # Weighted scoring based on severity and confidence
        severity_weights = {
            RiskLevel.LOW: 1.0,
            RiskLevel.MEDIUM: 2.0,
            RiskLevel.HIGH: 3.0,
            RiskLevel.CRITICAL: 4.0
        }
        
        total_score = 0.0
        max_weight = 0.0
        
        for signal in signals:
            weight = severity_weights[signal.severity]
            weighted_score = signal.confidence * weight
            total_score += weighted_score
            max_weight += weight
        
        if max_weight == 0:
            return 0.0, RiskLevel.LOW
        
        normalized_score = total_score / max_weight
        
        # Determine risk level
        if normalized_score >= 0.8:
            risk_level = RiskLevel.CRITICAL
        elif normalized_score >= 0.6:
            risk_level = RiskLevel.HIGH
        elif normalized_score >= 0.4:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return normalized_score, risk_level


class RiskReportGenerator:
    """Generate comprehensive risk reports for merchants"""
    
    def __init__(self, risk_engine: AIMLRiskEngine):
        self.risk_engine = risk_engine
    
    def generate_transaction_report(self, transaction: Transaction) -> Dict:
        """Generate a detailed risk report for a transaction"""
        signals = self.risk_engine.analyze_transaction(transaction)
        overall_score, risk_level = self.risk_engine.calculate_overall_risk_score(signals)
        
        return {
            "transaction_id": transaction.transaction_id,
            "merchant_id": transaction.merchant_id,
            "timestamp": transaction.timestamp.isoformat(),
            "amount": transaction.amount,
            "currency": transaction.currency,
            "overall_risk_score": overall_score,
            "risk_level": risk_level.value,
            "signals": [
                {
                    "type": signal.signal_type,
                    "confidence": signal.confidence,
                    "description": signal.description,
                    "severity": signal.severity.value,
                    "metadata": signal.metadata
                }
                for signal in signals
            ],
            "recommendations": self._generate_recommendations(risk_level, signals)
        }
    
    def _generate_recommendations(self, risk_level: RiskLevel, signals: List[RiskSignal]) -> List[str]:
        """Generate actionable recommendations based on risk assessment"""
        recommendations = []
        
        if risk_level == RiskLevel.CRITICAL:
            recommendations.append("BLOCK TRANSACTION - Critical fraud risk detected")
            recommendations.append("Flag merchant account for manual review")
        elif risk_level == RiskLevel.HIGH:
            recommendations.append("Hold transaction for manual review")
            recommendations.append("Request additional verification from customer")
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.append("Apply additional authentication measures")
            recommendations.append("Monitor customer behavior closely")
        else:
            recommendations.append("Process transaction normally")
            recommendations.append("Continue standard monitoring")
        
        # Add signal-specific recommendations
        signal_types = [signal.signal_type for signal in signals]
        
        if "high_velocity" in signal_types:
            recommendations.append("Implement rate limiting for this IP address")
        
        if "geographic_mismatch" in signal_types:
            recommendations.append("Verify customer location through additional means")
        
        if "suspicious_user_agent" in signal_types:
            recommendations.append("Block or flag automated/bot traffic")
        
        return recommendations


def create_sample_transaction() -> Transaction:
    """Create a sample transaction for testing"""
    return Transaction(
        transaction_id=f"txn_{random.randint(100000, 999999)}",
        merchant_id=f"merchant_{random.randint(1000, 9999)}",
        amount=random.uniform(10.0, 5000.0),
        currency="USD",
        timestamp=datetime.now(),
        user_ip=f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        payment_method=random.choice(["credit_card", "debit_card", "paypal", "bank_transfer"]),
        billing_address={
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "country": "US",
            "zip": "12345"
        },
        shipping_address={
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "country": "US",
            "zip": "12345"
        },
        device_fingerprint=hashlib.md5(f"device_{random.randint(1, 10000)}".encode()).hexdigest()
    )


def main():
    """Main function to demonstrate the AIML risk signals system"""
    print("🤖 AIML Risk Signals for Web Merchants")
    print("=" * 50)
    
    # Initialize the risk engine
    risk_engine = AIMLRiskEngine()
    report_generator = RiskReportGenerator(risk_engine)
    
    # Process sample transactions
    for i in range(5):
        print(f"\n📊 Processing Transaction {i + 1}")
        print("-" * 30)
        
        # Create sample transaction
        transaction = create_sample_transaction()
        
        # Generate risk report
        report = report_generator.generate_transaction_report(transaction)
        
        # Display results
        print(f"Transaction ID: {report['transaction_id']}")
        print(f"Amount: ${report['amount']:.2f} {report['currency']}")
        print(f"Risk Score: {report['overall_risk_score']:.3f}")
        print(f"Risk Level: {report['risk_level'].upper()}")
        
        if report['signals']:
            print("\n🚨 Risk Signals Detected:")
            for signal in report['signals']:
                print(f"  • {signal['type']}: {signal['description']} (Confidence: {signal['confidence']:.2f})")
        
        print("\n💡 Recommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
        
        time.sleep(1)  # Simulate processing time
    
    print("\n✅ Risk analysis complete!")


if __name__ == "__main__":
    main()
