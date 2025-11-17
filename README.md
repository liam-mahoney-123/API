# NextGen Rule Recommendation Engine

A next-generation rule recommendation engine powered by generative AI to provide intelligent, context-aware suggestions for rule creation and optimization in fraud detection and risk management systems.

## Overview

This engine analyzes transaction patterns, user behavior, and risk indicators to automatically generate intelligent rule recommendations that help prevent fraud while minimizing false positives.

## Features

### 🤖 AI-Powered Recommendations
- **Context-Aware Analysis**: Analyzes transaction context including amount, location, device, and behavioral patterns
- **Multi-Risk Assessment**: Evaluates velocity, amount anomalies, geographic risks, device fingerprinting, and behavioral patterns
- **Confidence Scoring**: Each recommendation includes a confidence score and estimated impact metrics

### 🎯 Rule Types Supported
- **Fraud Detection**: Amount-based anomaly detection
- **Velocity Checks**: High-frequency transaction monitoring  
- **Geographic Restrictions**: Location-based risk assessment
- **Behavioral Analysis**: User behavior pattern analysis
- **Device Verification**: Unknown device detection
- **Risk Assessment**: Comprehensive risk scoring

### 📊 Performance Optimization
- **Rule Optimization**: Automatically suggests improvements for existing rules based on performance data
- **False Positive Reduction**: Identifies and reduces rules with high false positive rates
- **Detection Rate Enhancement**: Improves rules with low fraud detection rates

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from rule_recommendation_engine import RuleRecommendationAPI
from datetime import datetime

# Initialize the API
api = RuleRecommendationAPI()

# Sample transaction data
transaction_data = {
    "transaction_id": "txn_12345",
    "user_id": "user_67890", 
    "amount": 2500.00,
    "currency": "USD",
    "merchant_category": "electronics",
    "location": "New York, NY",
    "timestamp": datetime.now().isoformat(),
    "payment_method": "credit_card",
    "device_fingerprint": "device_abc123",
    "ip_address": "192.168.1.100"
}

# Get rule recommendations
result = api.get_recommendations(transaction_data)

print(f"Generated {result['recommendations_count']} recommendations")
for rec in result['recommendations']:
    print(f"- {rec['name']} (Confidence: {rec['confidence_score']:.2f})")
```

### Example Output

```
=== NextGen Rule Recommendation Engine Results ===
Status: success
Transaction ID: txn_12345
Number of Recommendations: 3

=== Recommended Rules ===

1. Amount Anomaly Detection Rule - USD
   Type: fraud_detection
   Risk Level: medium
   Confidence: 0.89
   Description: Flag transactions with amounts significantly above user's normal spending pattern
   Reasoning: Amount anomaly detected (0.67). Transaction amount $2500.0 significantly exceeds normal patterns.

2. Device Verification Rule - device_a
   Type: behavioral_analysis  
   Risk Level: medium
   Confidence: 0.82
   Description: Verify transactions from unrecognized or suspicious devices
   Reasoning: Device risk detected (0.58). Unrecognized device fingerprint requires additional verification.

3. Behavioral Anomaly Rule - user_67890
   Type: behavioral_analysis
   Risk Level: medium
   Confidence: 0.79
   Description: Detect behavioral patterns that deviate from user's normal activity
   Reasoning: Behavioral anomaly detected (0.54). Transaction pattern deviates from user's normal behavior.
```

## Architecture

### Core Components

1. **AIRuleEngine**: Core recommendation engine with risk analysis capabilities
2. **RuleRecommendationAPI**: REST API interface for generating recommendations  
3. **TransactionContext**: Data model for transaction information
4. **RuleRecommendation**: Data model for generated rule recommendations
5. **HistoricalPattern**: Pattern analysis for historical fraud data

### Risk Analysis Pipeline

```
Transaction Data → Context Analysis → Risk Scoring → Rule Generation → Optimization
```

1. **Context Analysis**: Extracts relevant features from transaction data
2. **Risk Scoring**: Calculates risk scores across multiple dimensions
3. **Rule Generation**: Creates targeted rules based on risk indicators
4. **Optimization**: Suggests improvements for existing rules

## API Reference

### RuleRecommendationAPI

#### `get_recommendations(transaction_data: Dict) -> Dict`

Generates rule recommendations for a given transaction.

**Parameters:**
- `transaction_data`: Dictionary containing transaction information

**Required Fields:**
- `transaction_id`: Unique transaction identifier
- `user_id`: User identifier  
- `amount`: Transaction amount

**Optional Fields:**
- `currency`: Currency code (default: "USD")
- `merchant_category`: Merchant category
- `location`: Transaction location
- `timestamp`: Transaction timestamp
- `payment_method`: Payment method used
- `device_fingerprint`: Device identifier
- `ip_address`: IP address

**Returns:**
```python
{
    "status": "success",
    "transaction_id": "txn_12345", 
    "recommendations_count": 3,
    "recommendations": [...],
    "risk_analysis": {...}
}
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest test_rule_engine.py -v

# Run with coverage
pytest test_rule_engine.py --cov=rule_recommendation_engine

# Run basic tests
python test_rule_engine.py
```

## Integration with Existing Systems

### Visa Integrated Risk Platform (IRP)

This engine is designed to integrate with Visa's Integrated Risk Platform as part of the Rule Management as a Service initiative:

```python
# Integration example
from rule_recommendation_engine import RuleRecommendationAPI

class VisaRiskIntegration:
    def __init__(self):
        self.rule_engine = RuleRecommendationAPI()
    
    def process_transaction(self, visa_transaction):
        # Convert Visa transaction format
        transaction_data = self.convert_visa_format(visa_transaction)
        
        # Get recommendations
        recommendations = self.rule_engine.get_recommendations(transaction_data)
        
        # Apply to IRP
        return self.apply_to_irp(recommendations)
```

### Webhook Integration

```python
from flask import Flask, request, jsonify
from rule_recommendation_engine import RuleRecommendationAPI

app = Flask(__name__)
api = RuleRecommendationAPI()

@app.route('/recommend-rules', methods=['POST'])
def recommend_rules():
    transaction_data = request.json
    result = api.get_recommendations(transaction_data)
    return jsonify(result)
```

## Performance Metrics

The engine tracks several key performance indicators:

- **Fraud Prevention Rate**: Percentage of fraud successfully detected
- **False Positive Rate**: Percentage of legitimate transactions flagged
- **Processing Delay**: Average time added to transaction processing
- **Confidence Score**: AI confidence in recommendation accuracy
- **Rule Effectiveness**: Historical performance of generated rules

## Roadmap

### Phase 1: Core Engine (Current)
- ✅ Basic rule recommendation engine
- ✅ Multi-dimensional risk analysis
- ✅ API interface and testing framework

### Phase 2: Enhanced AI Capabilities
- 🔄 Machine learning model integration
- 🔄 Real-time pattern learning
- 🔄 Advanced behavioral analysis

### Phase 3: Production Integration  
- 📋 Visa IRP integration
- 📋 Real-time processing pipeline
- 📋 Performance monitoring dashboard
- 📋 A/B testing framework

### Phase 4: Advanced Features
- 📋 Explainable AI recommendations
- 📋 Multi-language support
- 📋 Advanced optimization algorithms
- 📋 Regulatory compliance features

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is part of Visa's Integrated Risk Platform initiative and is proprietary to Visa Inc.

## Support

For questions and support, please contact the Visa Risk Engineering team or create an issue in this repository.

---

**Built with ❤️ by the Visa Risk Engineering Team**
