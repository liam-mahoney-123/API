"""
Adaptive Payment UI Components
Modular widgets for different payment experiences
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

class DeviceType(Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"

class PaymentMethodType(Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    BANK_TRANSFER = "bank_transfer"
    CRYPTOCURRENCY = "cryptocurrency"

@dataclass
class UIConfig:
    """Configuration for adaptive UI rendering"""
    device_type: DeviceType
    screen_width: int
    screen_height: int
    layout_style: str = "standard"  # compact, standard, expanded
    theme: str = "light"  # light, dark, auto
    accessibility_mode: bool = False
    high_contrast: bool = False
    font_size_multiplier: float = 1.0

@dataclass
class PaymentMethodConfig:
    """Configuration for individual payment methods"""
    method_type: PaymentMethodType
    display_name: str
    icon_class: str
    required_fields: List[str]
    validation_rules: Dict[str, Any]
    enabled: bool = True
    priority: int = 0  # Higher priority methods appear first

class AdaptiveUIRenderer:
    """Renders payment UI components based on device and context"""
    
    def __init__(self):
        self.payment_methods = self._initialize_payment_methods()
    
    def _initialize_payment_methods(self) -> Dict[PaymentMethodType, PaymentMethodConfig]:
        """Initialize default payment method configurations"""
        return {
            PaymentMethodType.CREDIT_CARD: PaymentMethodConfig(
                method_type=PaymentMethodType.CREDIT_CARD,
                display_name="Credit/Debit Card",
                icon_class="fas fa-credit-card",
                required_fields=["card_number", "expiry_date", "cvv", "cardholder_name"],
                validation_rules={
                    "card_number": {"pattern": r"^\d{13,19}$", "luhn_check": True},
                    "expiry_date": {"pattern": r"^(0[1-9]|1[0-2])\/\d{2}$"},
                    "cvv": {"pattern": r"^\d{3,4}$"},
                    "cardholder_name": {"min_length": 2, "max_length": 50}
                },
                priority=10
            ),
            PaymentMethodType.PAYPAL: PaymentMethodConfig(
                method_type=PaymentMethodType.PAYPAL,
                display_name="PayPal",
                icon_class="fab fa-paypal",
                required_fields=["email"],
                validation_rules={
                    "email": {"pattern": r"^[^\s@]+@[^\s@]+\.[^\s@]+$"}
                },
                priority=8
            ),
            PaymentMethodType.APPLE_PAY: PaymentMethodConfig(
                method_type=PaymentMethodType.APPLE_PAY,
                display_name="Apple Pay",
                icon_class="fab fa-apple",
                required_fields=[],
                validation_rules={},
                priority=9
            ),
            PaymentMethodType.GOOGLE_PAY: PaymentMethodConfig(
                method_type=PaymentMethodType.GOOGLE_PAY,
                display_name="Google Pay",
                icon_class="fab fa-google",
                required_fields=[],
                validation_rules={},
                priority=9
            ),
            PaymentMethodType.BANK_TRANSFER: PaymentMethodConfig(
                method_type=PaymentMethodType.BANK_TRANSFER,
                display_name="Bank Transfer",
                icon_class="fas fa-university",
                required_fields=["account_number", "routing_number", "account_holder"],
                validation_rules={
                    "account_number": {"pattern": r"^\d{8,17}$"},
                    "routing_number": {"pattern": r"^\d{9}$"},
                    "account_holder": {"min_length": 2, "max_length": 50}
                },
                priority=5
            ),
            PaymentMethodType.CRYPTOCURRENCY: PaymentMethodConfig(
                method_type=PaymentMethodType.CRYPTOCURRENCY,
                display_name="Cryptocurrency",
                icon_class="fab fa-bitcoin",
                required_fields=["wallet_address", "currency_type"],
                validation_rules={
                    "wallet_address": {"min_length": 26, "max_length": 62},
                    "currency_type": {"allowed_values": ["BTC", "ETH", "LTC", "BCH"]}
                },
                priority=3
            )
        }
    
    def get_adaptive_layout(self, ui_config: UIConfig) -> Dict[str, Any]:
        """Generate adaptive layout configuration"""
        layout = {
            "container_class": self._get_container_class(ui_config),
            "grid_columns": self._get_grid_columns(ui_config),
            "form_style": self._get_form_style(ui_config),
            "button_size": self._get_button_size(ui_config),
            "spacing": self._get_spacing(ui_config),
            "typography": self._get_typography(ui_config)
        }
        
        return layout
    
    def _get_container_class(self, ui_config: UIConfig) -> str:
        """Determine container CSS class based on device"""
        base_class = "payment-container"
        
        if ui_config.device_type == DeviceType.MOBILE:
            return f"{base_class} mobile-layout"
        elif ui_config.device_type == DeviceType.TABLET:
            return f"{base_class} tablet-layout"
        else:
            return f"{base_class} desktop-layout"
    
    def _get_grid_columns(self, ui_config: UIConfig) -> int:
        """Determine number of grid columns for payment methods"""
        if ui_config.device_type == DeviceType.MOBILE:
            return 1
        elif ui_config.device_type == DeviceType.TABLET:
            return 2
        else:
            return 3
    
    def _get_form_style(self, ui_config: UIConfig) -> str:
        """Determine form layout style"""
        if ui_config.device_type == DeviceType.MOBILE:
            return "stacked"
        else:
            return "inline" if ui_config.layout_style == "compact" else "standard"
    
    def _get_button_size(self, ui_config: UIConfig) -> str:
        """Determine button size"""
        if ui_config.device_type == DeviceType.MOBILE:
            return "large"
        else:
            return "medium"
    
    def _get_spacing(self, ui_config: UIConfig) -> Dict[str, str]:
        """Determine spacing values"""
        if ui_config.device_type == DeviceType.MOBILE:
            return {"padding": "15px", "margin": "10px", "gap": "10px"}
        else:
            return {"padding": "20px", "margin": "15px", "gap": "15px"}
    
    def _get_typography(self, ui_config: UIConfig) -> Dict[str, str]:
        """Determine typography settings"""
        base_size = 16 * ui_config.font_size_multiplier
        
        return {
            "base_font_size": f"{base_size}px",
            "heading_size": f"{base_size * 1.5}px",
            "small_text_size": f"{base_size * 0.875}px",
            "font_weight": "600" if ui_config.accessibility_mode else "400"
        }
    
    def get_enabled_payment_methods(self, user_context: Optional[Dict] = None) -> List[PaymentMethodConfig]:
        """Get list of enabled payment methods sorted by priority"""
        methods = [method for method in self.payment_methods.values() if method.enabled]
        
        # Apply user context filtering if provided
        if user_context:
            methods = self._filter_methods_by_context(methods, user_context)
        
        # Sort by priority (higher first)
        return sorted(methods, key=lambda x: x.priority, reverse=True)
    
    def _filter_methods_by_context(self, methods: List[PaymentMethodConfig], 
                                 context: Dict) -> List[PaymentMethodConfig]:
        """Filter payment methods based on user context"""
        filtered_methods = []
        
        for method in methods:
            # Check geographic restrictions
            if "country" in context:
                if method.method_type == PaymentMethodType.APPLE_PAY and context["country"] not in ["US", "CA", "GB", "AU"]:
                    continue
                if method.method_type == PaymentMethodType.GOOGLE_PAY and context["country"] not in ["US", "CA", "GB", "AU", "IN"]:
                    continue
            
            # Check device capabilities
            if "device_capabilities" in context:
                capabilities = context["device_capabilities"]
                if method.method_type == PaymentMethodType.APPLE_PAY and not capabilities.get("touch_id", False):
                    continue
                if method.method_type == PaymentMethodType.GOOGLE_PAY and not capabilities.get("nfc", False):
                    continue
            
            # Check amount restrictions
            if "amount" in context:
                amount = context["amount"]
                if method.method_type == PaymentMethodType.CRYPTOCURRENCY and amount < 10:
                    continue  # Minimum amount for crypto
            
            filtered_methods.append(method)
        
        return filtered_methods
    
    def generate_form_fields(self, method_type: PaymentMethodType, 
                           ui_config: UIConfig) -> List[Dict[str, Any]]:
        """Generate form field configurations for a payment method"""
        if method_type not in self.payment_methods:
            return []
        
        method_config = self.payment_methods[method_type]
        fields = []
        
        for field_name in method_config.required_fields:
            field_config = self._get_field_config(field_name, method_config, ui_config)
            fields.append(field_config)
        
        return fields
    
    def _get_field_config(self, field_name: str, method_config: PaymentMethodConfig, 
                         ui_config: UIConfig) -> Dict[str, Any]:
        """Generate configuration for a specific form field"""
        base_config = {
            "name": field_name,
            "type": "text",
            "required": True,
            "class": "form-control adaptive-input"
        }
        
        # Field-specific configurations
        field_configs = {
            "card_number": {
                "label": "Card Number",
                "placeholder": "1234 5678 9012 3456",
                "type": "text",
                "maxlength": 19,
                "pattern": r"[\d\s]*",
                "autocomplete": "cc-number"
            },
            "expiry_date": {
                "label": "Expiry Date",
                "placeholder": "MM/YY",
                "type": "text",
                "maxlength": 5,
                "pattern": r"\d{2}/\d{2}",
                "autocomplete": "cc-exp"
            },
            "cvv": {
                "label": "CVV",
                "placeholder": "123",
                "type": "password" if ui_config.accessibility_mode else "text",
                "maxlength": 4,
                "pattern": r"\d*",
                "autocomplete": "cc-csc"
            },
            "cardholder_name": {
                "label": "Cardholder Name",
                "placeholder": "John Doe",
                "type": "text",
                "autocomplete": "cc-name"
            },
            "email": {
                "label": "Email Address",
                "placeholder": "your@email.com",
                "type": "email",
                "autocomplete": "email"
            },
            "account_number": {
                "label": "Account Number",
                "placeholder": "123456789",
                "type": "text",
                "autocomplete": "off"
            },
            "routing_number": {
                "label": "Routing Number",
                "placeholder": "021000021",
                "type": "text",
                "maxlength": 9,
                "autocomplete": "off"
            },
            "account_holder": {
                "label": "Account Holder Name",
                "placeholder": "John Doe",
                "type": "text",
                "autocomplete": "name"
            },
            "wallet_address": {
                "label": "Wallet Address",
                "placeholder": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                "type": "text",
                "autocomplete": "off"
            },
            "currency_type": {
                "label": "Currency",
                "type": "select",
                "options": [
                    {"value": "BTC", "label": "Bitcoin (BTC)"},
                    {"value": "ETH", "label": "Ethereum (ETH)"},
                    {"value": "LTC", "label": "Litecoin (LTC)"},
                    {"value": "BCH", "label": "Bitcoin Cash (BCH)"}
                ]
            }
        }
        
        if field_name in field_configs:
            base_config.update(field_configs[field_name])
        
        # Apply UI config modifications
        if ui_config.device_type == DeviceType.MOBILE:
            base_config["class"] += " mobile-input"
        
        if ui_config.accessibility_mode:
            base_config["aria-required"] = "true"
            base_config["class"] += " accessible-input"
        
        return base_config
    
    def validate_payment_data(self, method_type: PaymentMethodType, 
                            payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate payment data against method requirements"""
        if method_type not in self.payment_methods:
            return {"valid": False, "errors": ["Invalid payment method"]}
        
        method_config = self.payment_methods[method_type]
        errors = []
        
        # Check required fields
        for field in method_config.required_fields:
            if field not in payment_data or not payment_data[field]:
                errors.append(f"{field.replace('_', ' ').title()} is required")
        
        # Apply validation rules
        for field, value in payment_data.items():
            if field in method_config.validation_rules:
                field_errors = self._validate_field(field, value, method_config.validation_rules[field])
                errors.extend(field_errors)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _validate_field(self, field_name: str, value: Any, rules: Dict[str, Any]) -> List[str]:
        """Validate a single field against its rules"""
        errors = []
        
        if "pattern" in rules:
            import re
            if not re.match(rules["pattern"], str(value)):
                errors.append(f"Invalid format for {field_name.replace('_', ' ')}")
        
        if "min_length" in rules:
            if len(str(value)) < rules["min_length"]:
                errors.append(f"{field_name.replace('_', ' ').title()} is too short")
        
        if "max_length" in rules:
            if len(str(value)) > rules["max_length"]:
                errors.append(f"{field_name.replace('_', ' ').title()} is too long")
        
        if "allowed_values" in rules:
            if value not in rules["allowed_values"]:
                errors.append(f"Invalid value for {field_name.replace('_', ' ')}")
        
        if "luhn_check" in rules and rules["luhn_check"]:
            if not self._luhn_check(str(value).replace(" ", "")):
                errors.append("Invalid card number")
        
        return errors
    
    def _luhn_check(self, card_number: str) -> bool:
        """Perform Luhn algorithm check for credit card validation"""
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        
        return luhn_checksum(card_number) == 0

# Example usage and factory functions
def create_mobile_payment_ui(user_context: Optional[Dict] = None) -> Dict[str, Any]:
    """Create a mobile-optimized payment UI configuration"""
    ui_config = UIConfig(
        device_type=DeviceType.MOBILE,
        screen_width=375,
        screen_height=812,
        layout_style="compact",
        theme="light"
    )
    
    renderer = AdaptiveUIRenderer()
    
    return {
        "layout": renderer.get_adaptive_layout(ui_config),
        "payment_methods": renderer.get_enabled_payment_methods(user_context),
        "ui_config": ui_config
    }

def create_desktop_payment_ui(user_context: Optional[Dict] = None) -> Dict[str, Any]:
    """Create a desktop-optimized payment UI configuration"""
    ui_config = UIConfig(
        device_type=DeviceType.DESKTOP,
        screen_width=1920,
        screen_height=1080,
        layout_style="standard",
        theme="light"
    )
    
    renderer = AdaptiveUIRenderer()
    
    return {
        "layout": renderer.get_adaptive_layout(ui_config),
        "payment_methods": renderer.get_enabled_payment_methods(user_context),
        "ui_config": ui_config
    }
