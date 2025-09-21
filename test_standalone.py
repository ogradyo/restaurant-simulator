#!/usr/bin/env python3
"""
Test script for standalone order message generation
"""

import os
import sys
import json

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from order_simulator import OrderProcessor, OrderType, OrderItem, MENU_DICT
from order_simulator.message_generator import OrderMessageGenerator, OrderMessageDelivery
from order_simulator.message_router import MessageRouterBuilder

def test_basic_message_generation():
    """Test basic message generation"""
    print("🧪 Testing basic message generation...")
    
    # Initialize components
    processor = OrderProcessor()
    message_generator = OrderMessageGenerator()
    delivery = OrderMessageDelivery()
    
    # Create a test order
    customer = processor.create_customer("Test Customer", "555-1234", "test@example.com")
    
    items = [
        OrderItem(menu_item=MENU_DICT["chicken_sandwich"], quantity=1),
        OrderItem(menu_item=MENU_DICT["waffle_fries"], quantity=1)
    ]
    
    order = processor.create_order(OrderType.DRIVE_THRU, customer, items)
    processor.confirm_order(order.id)
    
    print(f"✅ Created order: {order.id}")
    
    # Test different message formats
    formats = ["json", "xml", "pos", "kitchen", "delivery"]
    
    for format_type in formats:
        try:
            message = message_generator.generate_order_message(order, format_type)
            print(f"✅ Generated {format_type} message")
            
            # Save to file
            filename = f"test_order_{format_type}.{format_type}"
            delivery.deliver_message(message, filename, "file")
            print(f"✅ Saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error with {format_type}: {e}")

def test_message_routing():
    """Test message routing"""
    print("\n🧪 Testing message routing...")
    
    # Create router
    router = (MessageRouterBuilder()
              .add_pos_system_route(destination="test_pos")
              .add_kitchen_display_route(destination="test_kitchen")
              .add_delivery_service_route(destination="test_delivery")
              .build())
    
    # Register delivery handler
    delivery = OrderMessageDelivery()
    router.register_delivery_handler(delivery)
    
    # Create test order
    processor = OrderProcessor()
    customer = processor.create_customer("Routing Test", "555-5678")
    items = [OrderItem(menu_item=MENU_DICT["deluxe_sandwich"], quantity=1)]
    order = processor.create_order(OrderType.UBER_EATS, customer, items)
    processor.confirm_order(order.id)
    
    # Generate messages and route them
    message_generator = OrderMessageGenerator()
    
    formats = ["json", "pos", "kitchen", "delivery"]
    for format_type in formats:
        message = message_generator.generate_order_message(order, format_type)
        routed_to = router.route_message(message)
        print(f"✅ {format_type} message routed to: {routed_to}")

def test_continuous_generation():
    """Test continuous order generation"""
    print("\n🧪 Testing continuous generation...")
    
    from standalone_order_generator import StandaloneOrderGenerator
    
    generator = StandaloneOrderGenerator()
    
    # Generate a few orders
    orders = generator.generate_sample_orders(3)
    print(f"✅ Generated {len(orders)} orders")
    
    # Generate messages
    messages = generator.generate_messages(orders, ["json", "pos"], ["console"])
    print(f"✅ Generated {len(messages)} messages")

def main():
    """Run all tests"""
    print("🍗 Standalone Order Simulator Tests 🍗")
    print("=" * 50)
    
    try:
        test_basic_message_generation()
        test_message_routing()
        test_continuous_generation()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
