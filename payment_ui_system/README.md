# Adaptive & Integrated Payment UI System

A flexible, responsive payment interface built with Python Flask that adapts to different devices and payment methods.

## Features

### 🎯 Adaptive Design
- **Device Detection**: Automatically detects mobile, tablet, and desktop devices
- **Responsive Layout**: Grid system that adapts to screen size
- **Touch-Friendly**: Optimized for touch interactions on mobile devices
- **Accessibility**: Support for screen readers and keyboard navigation

### 💳 Multiple Payment Methods
- **Credit/Debit Cards**: Full card processing with validation
- **Digital Wallets**: Apple Pay, Google Pay integration
- **PayPal**: Email-based PayPal payments
- **Bank Transfer**: ACH/wire transfer support
- **Cryptocurrency**: Bitcoin, Ethereum, and other crypto support

### 🔧 Modular Architecture
- **Component-Based**: Reusable UI components
- **Configuration-Driven**: Easy to customize payment methods
- **Validation Engine**: Built-in form validation with Luhn algorithm
- **Context-Aware**: Filters payment methods based on user context

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd payment_ui_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Core Endpoints

- `GET /` - Main payment interface
- `GET /api/payment-methods` - Get available payment methods
- `GET /api/adaptive-config` - Get device-specific UI configuration
- `POST /api/create-transaction` - Create a new payment transaction
- `POST /api/process-payment` - Process a payment
- `GET /api/transaction/<id>` - Get transaction details

### Example API Usage

#### Create Transaction
```bash
curl -X POST http://localhost:5000/api/create-transaction \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 99.99,
    "currency": "USD",
    "payment_method": "credit_card"
  }'
```

#### Process Payment
```bash
curl -X POST http://localhost:5000/api/process-payment \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "uuid-here",
    "payment_data": {
      "card_number": "4111111111111111",
      "expiry_date": "12/25",
      "cvv": "123",
      "cardholder_name": "John Doe"
    }
  }'
```

## Architecture

### Backend Components

#### `app.py`
Main Flask application with API endpoints and payment processing logic.

#### `components/payment_widgets.py`
Modular payment UI components with:
- `AdaptiveUIRenderer`: Renders UI based on device type
- `PaymentMethodConfig`: Configuration for payment methods
- `UIConfig`: Device and accessibility configuration
- Validation engine with Luhn algorithm

### Frontend Components

#### `templates/payment_interface.html`
Responsive HTML template with:
- CSS Grid layout system
- JavaScript for dynamic form handling
- Real-time validation
- Adaptive styling based on device

## Customization

### Adding New Payment Methods

```python
# In payment_widgets.py
PaymentMethodType.NEW_METHOD = PaymentMethodConfig(
    method_type=PaymentMethodType.NEW_METHOD,
    display_name="New Payment Method",
    icon_class="fas fa-new-icon",
    required_fields=["field1", "field2"],
    validation_rules={
        "field1": {"pattern": r"^[A-Z0-9]+$"},
        "field2": {"min_length": 5, "max_length": 20}
    },
    priority=7
)
```

### Device-Specific Styling

```python
# Custom UI configuration
ui_config = UIConfig(
    device_type=DeviceType.MOBILE,
    screen_width=375,
    screen_height=812,
    layout_style="compact",
    theme="dark",
    accessibility_mode=True,
    font_size_multiplier=1.2
)
```

### Context-Based Filtering

```python
# Filter payment methods by user context
user_context = {
    "country": "US",
    "device_capabilities": {"touch_id": True, "nfc": True},
    "amount": 50.00
}

methods = renderer.get_enabled_payment_methods(user_context)
```

## Security Features

- **Input Validation**: Server-side validation for all payment data
- **Luhn Algorithm**: Credit card number validation
- **CORS Protection**: Configurable cross-origin resource sharing
- **Session Management**: Secure session handling
- **Transaction Expiry**: 15-minute transaction timeout

## Mobile Optimization

- **Touch Targets**: Minimum 44px touch targets
- **Viewport Meta**: Proper viewport configuration
- **Input Types**: Optimized keyboard types for mobile
- **Gesture Support**: Swipe and tap interactions
- **Performance**: Optimized for mobile networks

## Browser Support

- **Modern Browsers**: Chrome 70+, Firefox 65+, Safari 12+, Edge 79+
- **Mobile Browsers**: iOS Safari 12+, Chrome Mobile 70+
- **Progressive Enhancement**: Graceful degradation for older browsers

## Development

### Project Structure
```
payment_ui_system/
├── app.py                          # Main Flask application
├── components/
│   └── payment_widgets.py          # UI components and validation
├── templates/
│   └── payment_interface.html      # Frontend template
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

### Testing

```bash
# Run the application in debug mode
python app.py

# Test API endpoints
curl -X GET http://localhost:5000/api/payment-methods
curl -X GET http://localhost:5000/api/adaptive-config
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support, please open an issue in the repository or contact the development team.
