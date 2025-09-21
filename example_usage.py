#!/usr/bin/env python3
"""
Example usage of the standalone order simulator
"""

import os
import sys
import json

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from order_simulator import OrderProcessor, OrderType, OrderItem, MENU_DICT
from order_simulator.message_generator import OrderMessageGenerator, OrderMessageDelivery
from order_simulator.message_router import MessageRouterBuilder

def example_1_basic_order_creation():
    """Example 1: Basic order creation and message generation"""
    print("📝 Example 1: Basic Order Creation")
    print("-" * 40)
    
    # Initialize the order processor
    processor = OrderProcessor()
    
    # Create a customer
    customer = processor.create_customer(
        name="Alice Johnson",
        phone="555-1234",
        email="alice@example.com",
        loyalty_member=True
    )
    
    # Create order items
    items = [
        OrderItem(
            menu_item=MENU_DICT["chicken_sandwich"],
            quantity=1,
            special_instructions="No pickles"
        ),
        OrderItem(
            menu_item=MENU_DICT["waffle_fries"],
            quantity=1
        ),
        OrderItem(
            menu_item=MENU_DICT["lemonade"],
            quantity=1
        )
    ]
    
    # Create the order
    order = processor.create_order(
        order_type=OrderType.DRIVE_THRU,
        customer=customer,
        items=items,
        special_instructions="Please make it fresh!"
    )
    
    # Confirm the order
    processor.confirm_order(order.id)
    
    print(f"✅ Created order: {order.id}")
    print(f"   Customer: {customer.name}")
    print(f"   Total: ${order.total_amount:.2f}")
    print(f"   Items: {len(order.items)}")
    
    return order

def example_2_message_generation(order):
    """Example 2: Generate messages in different formats"""
    print("\n📝 Example 2: Message Generation")
    print("-" * 40)
    
    # Initialize message generator
    message_generator = OrderMessageGenerator()
    
    # Generate messages in different formats
    formats = ["json", "xml", "pos", "kitchen", "delivery"]
    
    for format_type in formats:
        message = message_generator.generate_order_message(order, format_type)
        print(f"✅ Generated {format_type} message")
        print(f"   Content type: {message['content_type']}")
        print(f"   Content length: {len(message['content'])} characters")

def example_3_message_delivery(order):
    """Example 3: Deliver messages to different destinations"""
    print("\n📝 Example 3: Message Delivery")
    print("-" * 40)
    
    # Initialize components
    message_generator = OrderMessageGenerator()
    delivery = OrderMessageDelivery()
    
    # Generate a JSON message
    message = message_generator.generate_order_message(order, "json")
    
    # Deliver to different destinations
    destinations = [
        ("order.json", "file"),
        ("", "console"),  # Console output
    ]
    
    for destination, method in destinations:
        success = delivery.deliver_message(message, destination, method)
        if success:
            print(f"✅ Delivered to {destination or 'console'} via {method}")
        else:
            print(f"❌ Failed to deliver to {destination} via {method}")

def example_4_message_routing():
    """Example 4: Message routing to different systems"""
    print("\n📝 Example 4: Message Routing")
    print("-" * 40)
    
    # Create a router with different routes
    router = (MessageRouterBuilder()
              .add_pos_system_route(destination="pos_orders")
              .add_kitchen_display_route(destination="kitchen_orders")
              .add_delivery_service_route(destination="delivery_orders")
              .build())
    
    # Register delivery handler
    delivery = OrderMessageDelivery()
    router.register_delivery_handler(delivery)
    
    # Create different types of orders
    processor = OrderProcessor()
    message_generator = OrderMessageGenerator()
    
    order_types = [
        (OrderType.DRIVE_THRU, "Drive-thru Order"),
        (OrderType.UBER_EATS, "Uber Eats Order"),
        (OrderType.DINE_IN, "Dine-in Order")
    ]
    
    for order_type, description in order_types:
        # Create customer and order
        customer = processor.create_customer(f"Customer {order_type.value}")
        items = [OrderItem(menu_item=MENU_DICT["chicken_sandwich"], quantity=1)]
        order = processor.create_order(order_type, customer, items)
        processor.confirm_order(order.id)
        
        # Generate messages in different formats
        for format_type in ["json", "pos", "kitchen", "delivery"]:
            message = message_generator.generate_order_message(order, format_type)
            routed_to = router.route_message(message)
            print(f"✅ {description} ({format_type}) -> {routed_to}")

def example_5_batch_processing():
    """Example 5: Batch order processing"""
    print("\n📝 Example 5: Batch Processing")
    print("-" * 40)
    
    from standalone_order_generator import StandaloneOrderGenerator
    
    # Initialize generator
    generator = StandaloneOrderGenerator()
    
    # Generate multiple orders
    orders = generator.generate_sample_orders(5)
    print(f"✅ Generated {len(orders)} orders")
    
    # Generate messages for all orders
    messages = generator.generate_messages(
        orders, 
        formats=["json", "pos", "kitchen"], 
        destinations=["file"]
    )
    print(f"✅ Generated {len(messages)} messages")
    
    # Show statistics
    stats = generator.order_processor.get_order_statistics()
    print(f"📊 Statistics:")
    print(f"   Total orders: {stats['total_orders']}")
    print(f"   Average order value: ${stats['average_order_value']:.2f}")

def main():
    """Run all examples"""
    print("🍗 Standalone Order Simulator Examples 🍗")
    print("=" * 50)
    
    try:
        # Run examples
        order = example_1_basic_order_creation()
        example_2_message_generation(order)
        example_3_message_delivery(order)
        example_4_message_routing()
        example_5_batch_processing()
        
        print("\n🎉 All examples completed successfully!")
        print("\n📁 Check the generated files:")
        print("   - order.json")
        print("   - pos_orders/")
        print("   - kitchen_orders/")
        print("   - delivery_orders/")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
