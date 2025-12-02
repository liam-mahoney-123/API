"""
Adaptive & Integrated Payment UI System
Flask-based backend for payment experiences with responsive design
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'payment-ui-secret-key'
CORS(app)

# Payment method configurations
PAYMENT_METHODS = {
    'credit_card': {
        'name': 'Credit/Debit Card',
        'icon': 'credit-card',
        'fields': ['card_number', 'expiry_date', 'cvv', 'cardholder_name'],
        'validation': 'strict'
    },
    'paypal': {
        'name': 'PayPal',
        'icon': 'paypal',
        'fields': ['email'],
        'validation': 'email'
    },
    'apple_pay': {
        'name': 'Apple Pay',
        'icon': 'apple',
        'fields': [],
        'validation': 'biometric'
    },
    'google_pay': {
        'name': 'Google Pay',
        'icon': 'google',
        'fields': [],
        'validation': 'biometric'
    },
    'bank_transfer': {
        'name': 'Bank Transfer',
        'icon': 'bank',
        'fields': ['account_number', 'routing_number', 'account_holder'],
        'validation': 'bank'
    }
}

class PaymentProcessor:
    """Handles payment processing logic"""
    
    def __init__(self):
        self.transactions = {}
    
    def create_transaction(self, amount: float, currency: str = 'USD', 
                         payment_method: str = 'credit_card') -> Dict:
        """Create a new payment transaction"""
        transaction_id = str(uuid.uuid4())
        transaction = {
            'id': transaction_id,
            'amount': amount,
            'currency': currency,
            'payment_method': payment_method,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=15)).isoformat()
        }
        self.transactions[transaction_id] = transaction
        return transaction
    
    def process_payment(self, transaction_id: str, payment_data: Dict) -> Dict:
        """Process payment for a transaction"""
        if transaction_id not in self.transactions:
            return {'success': False, 'error': 'Transaction not found'}
        
        transaction = self.transactions[transaction_id]
        
        # Simulate payment processing
        if self._validate_payment_data(payment_data, transaction['payment_method']):
            transaction['status'] = 'completed'
            transaction['processed_at'] = datetime.now().isoformat()
            return {'success': True, 'transaction': transaction}
        else:
            transaction['status'] = 'failed'
            return {'success': False, 'error': 'Payment validation failed'}
    
    def _validate_payment_data(self, payment_data: Dict, method: str) -> bool:
        """Validate payment data based on method"""
        required_fields = PAYMENT_METHODS.get(method, {}).get('fields', [])
        return all(field in payment_data for field in required_fields)

# Initialize payment processor
payment_processor = PaymentProcessor()

@app.route('/')
def index():
    """Main payment interface"""
    return render_template('payment_interface.html', 
                         payment_methods=PAYMENT_METHODS)

@app.route('/api/payment-methods')
def get_payment_methods():
    """Get available payment methods"""
    return jsonify(PAYMENT_METHODS)

@app.route('/api/create-transaction', methods=['POST'])
def create_transaction():
    """Create a new payment transaction"""
    data = request.get_json()
    
    try:
        amount = float(data.get('amount', 0))
        currency = data.get('currency', 'USD')
        payment_method = data.get('payment_method', 'credit_card')
        
        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
        
        transaction = payment_processor.create_transaction(
            amount, currency, payment_method
        )
        
        return jsonify(transaction)
    
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        return jsonify({'error': 'Failed to create transaction'}), 500

@app.route('/api/process-payment', methods=['POST'])
def process_payment():
    """Process a payment"""
    data = request.get_json()
    
    try:
        transaction_id = data.get('transaction_id')
        payment_data = data.get('payment_data', {})
        
        if not transaction_id:
            return jsonify({'error': 'Transaction ID required'}), 400
        
        result = payment_processor.process_payment(transaction_id, payment_data)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        logger.error(f"Error processing payment: {e}")
        return jsonify({'error': 'Payment processing failed'}), 500

@app.route('/api/transaction/<transaction_id>')
def get_transaction(transaction_id):
    """Get transaction details"""
    transaction = payment_processor.transactions.get(transaction_id)
    
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    return jsonify(transaction)

@app.route('/api/adaptive-config')
def get_adaptive_config():
    """Get adaptive UI configuration based on device/context"""
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Simple device detection
    is_mobile = any(device in user_agent for device in ['mobile', 'android', 'iphone'])
    is_tablet = 'tablet' in user_agent or 'ipad' in user_agent
    
    config = {
        'device_type': 'mobile' if is_mobile else 'tablet' if is_tablet else 'desktop',
        'layout': 'compact' if is_mobile else 'standard',
        'payment_methods_per_row': 1 if is_mobile else 2 if is_tablet else 3,
        'show_icons': True,
        'enable_biometric': is_mobile,
        'form_style': 'stacked' if is_mobile else 'inline'
    }
    
    return jsonify(config)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
