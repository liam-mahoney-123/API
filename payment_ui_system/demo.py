#!/usr/bin/env python3
"""
Demo script for the Adaptive Payment UI System
Shows how to use the payment components programmatically
"""

from components.payment_widgets import (
    AdaptiveUIRenderer, 
    UIConfig, 
    DeviceType, 
    PaymentMethodType,
    create_mobile_payment_ui,
    create_desktop_payment_ui
)
import json

def demo_adaptive_ui():
    """Demonstrate adaptive UI configuration for different devices"""
    print("🎯 Adaptive Payment UI System Demo")
    print("=" * 50)
    
    # Create renderer
    renderer = AdaptiveUIRenderer()
    
    # Demo 1: Mobile UI Configuration
    print("\n📱 Mobile UI Configuration:")
    mobile_config = UIConfig(
        device_type=DeviceType.MOBILE,
        screen_width=375,
        screen_height=812,
        layout_style="compact",
        theme="light",
        accessibility_mode=True,
        font_size_multiplier=1.1
    )
    
    mobile_layout = renderer.get_adaptive_layout(mobile_config)
    print(f"  Container Class: {mobile_layout['container_class']}")
    print(f"  Grid Columns: {mobile_layout['grid_columns']}")
    print(f"  Form Style: {mobile_layout['form_style']}")
    print(f"  Button Size: {mobile_layout['button_size']}")
    
    # Demo 2: Desktop UI Configuration
    print("\n🖥️  Desktop UI Configuration:")
    desktop_config = UIConfig(
        device_type=DeviceType.DESKTOP,
        screen_width=1920,
        screen_height=1080,
        layout_style="standard",
        theme="light"
    )
    
    desktop_layout = renderer.get_adaptive_layout(desktop_config)
    print(f"  Container Class: {desktop_layout['container_class']}")
    print(f"  Grid Columns: {desktop_layout['grid_columns']}")
    print(f"  Form Style: {desktop_layout['form_style']}")
    print(f"  Button Size: {desktop_layout['button_size']}")

def demo_payment_methods():
    """Demonstrate payment method configuration and filtering"""
    print("\n💳 Payment Methods Demo:")
    print("=" * 30)
    
    renderer = AdaptiveUIRenderer()
    
    # Get all payment methods
    all_methods = renderer.get_enabled_payment_methods()
    print(f"\n📋 Available Payment Methods ({len(all_methods)}):")
    for method in all_methods:
        print(f"  • {method.display_name} (Priority: {method.priority})")
    
    # Demo context-based filtering
    print("\n🌍 Context-Based Filtering:")
    
    # US user with mobile device
    us_context = {
        "country": "US",
        "device_capabilities": {"touch_id": True, "nfc": True},
        "amount": 25.00
    }
    
    us_methods = renderer.get_enabled_payment_methods(us_context)
    print(f"\n🇺🇸 US User with Touch ID/NFC ({len(us_methods)} methods):")
    for method in us_methods:
        print(f"  • {method.display_name}")
    
    # International user with limited capabilities
    intl_context = {
        "country": "DE",
        "device_capabilities": {"touch_id": False, "nfc": False},
        "amount": 100.00
    }
    
    intl_methods = renderer.get_enabled_payment_methods(intl_context)
    print(f"\n🇩🇪 German User without biometrics ({len(intl_methods)} methods):")
    for method in intl_methods:
        print(f"  • {method.display_name}")

def demo_form_generation():
    """Demonstrate dynamic form field generation"""
    print("\n📝 Form Generation Demo:")
    print("=" * 25)
    
    renderer = AdaptiveUIRenderer()
    
    # Generate credit card form for mobile
    mobile_config = UIConfig(
        device_type=DeviceType.MOBILE,
        screen_width=375,
        screen_height=812,
        accessibility_mode=True
    )
    
    cc_fields = renderer.generate_form_fields(PaymentMethodType.CREDIT_CARD, mobile_config)
    print(f"\n💳 Credit Card Form Fields (Mobile):")
    for field in cc_fields:
        print(f"  • {field['label']}: {field['type']} ({field.get('placeholder', 'N/A')})")
    
    # Generate PayPal form for desktop
    desktop_config = UIConfig(
        device_type=DeviceType.DESKTOP,
        screen_width=1920,
        screen_height=1080
    )
    
    paypal_fields = renderer.generate_form_fields(PaymentMethodType.PAYPAL, desktop_config)
    print(f"\n💰 PayPal Form Fields (Desktop):")
    for field in paypal_fields:
        print(f"  • {field['label']}: {field['type']} ({field.get('placeholder', 'N/A')})")

def demo_validation():
    """Demonstrate payment data validation"""
    print("\n✅ Validation Demo:")
    print("=" * 18)
    
    renderer = AdaptiveUIRenderer()
    
    # Valid credit card data
    valid_cc_data = {
        "card_number": "4111111111111111",  # Valid test card
        "expiry_date": "12/25",
        "cvv": "123",
        "cardholder_name": "John Doe"
    }
    
    validation_result = renderer.validate_payment_data(
        PaymentMethodType.CREDIT_CARD, 
        valid_cc_data
    )
    
    print(f"\n💳 Valid Credit Card Data:")
    print(f"  Valid: {validation_result['valid']}")
    if validation_result['errors']:
        print(f"  Errors: {validation_result['errors']}")
    
    # Invalid credit card data
    invalid_cc_data = {
        "card_number": "1234567890123456",  # Invalid card number
        "expiry_date": "13/25",  # Invalid month
        "cvv": "12",  # Too short
        "cardholder_name": ""  # Empty name
    }
    
    validation_result = renderer.validate_payment_data(
        PaymentMethodType.CREDIT_CARD, 
        invalid_cc_data
    )
    
    print(f"\n❌ Invalid Credit Card Data:")
    print(f"  Valid: {validation_result['valid']}")
    print(f"  Errors:")
    for error in validation_result['errors']:
        print(f"    • {error}")

def demo_factory_functions():
    """Demonstrate factory functions for quick UI creation"""
    print("\n🏭 Factory Functions Demo:")
    print("=" * 26)
    
    # Create mobile payment UI
    mobile_ui = create_mobile_payment_ui({
        "country": "US",
        "device_capabilities": {"touch_id": True}
    })
    
    print(f"\n📱 Mobile Payment UI:")
    print(f"  Device Type: {mobile_ui['ui_config'].device_type.value}")
    print(f"  Layout Style: {mobile_ui['ui_config'].layout_style}")
    print(f"  Available Methods: {len(mobile_ui['payment_methods'])}")
    
    # Create desktop payment UI
    desktop_ui = create_desktop_payment_ui({
        "country": "CA",
        "amount": 150.00
    })
    
    print(f"\n🖥️  Desktop Payment UI:")
    print(f"  Device Type: {desktop_ui['ui_config'].device_type.value}")
    print(f"  Layout Style: {desktop_ui['ui_config'].layout_style}")
    print(f"  Available Methods: {len(desktop_ui['payment_methods'])}")

def demo_json_export():
    """Demonstrate JSON export of configurations"""
    print("\n📄 JSON Export Demo:")
    print("=" * 19)
    
    # Create a complete UI configuration
    mobile_ui = create_mobile_payment_ui({
        "country": "US",
        "device_capabilities": {"touch_id": True, "nfc": True},
        "amount": 75.00
    })
    
    # Convert to JSON-serializable format
    export_data = {
        "device_type": mobile_ui['ui_config'].device_type.value,
        "layout": mobile_ui['layout'],
        "payment_methods": [
            {
                "type": method.method_type.value,
                "name": method.display_name,
                "icon": method.icon_class,
                "fields": method.required_fields,
                "priority": method.priority
            }
            for method in mobile_ui['payment_methods']
        ]
    }
    
    print(f"\n📱 Mobile UI Configuration (JSON):")
    print(json.dumps(export_data, indent=2))

if __name__ == "__main__":
    try:
        demo_adaptive_ui()
        demo_payment_methods()
        demo_form_generation()
        demo_validation()
        demo_factory_functions()
        demo_json_export()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the web interface:")
        print("  python app.py")
        print("  Then visit: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
