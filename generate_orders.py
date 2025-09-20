#!/usr/bin/env python3
"""
Order Generator for ACSP Restaurant Simulator
This script automatically creates a bunch of simulated orders to demonstrate the system
"""

from order_simulator import OrderType, OrderProcessor, ExternalServiceManager
import random
import time
from datetime import datetime

def generate_sample_orders(num_orders=10):
    """Generate a bunch of sample orders"""
    print("🍗 ACSP Order Generator 🍗")
    print("=" * 40)
    
    # Initialize the system
    order_processor = OrderProcessor()
    external_services = ExternalServiceManager()
    
    # Sample customer names
    customer_names = [
        "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Emma Brown",
        "Frank Miller", "Grace Lee", "Henry Taylor", "Ivy Chen", "Jack Anderson",
        "Kate Martinez", "Liam O'Connor", "Maya Patel", "Noah Kim", "Olivia Garcia"
    ]
    
    # Sample order types
    order_types = [OrderType.DRIVE_THRU, OrderType.DINE_IN, OrderType.UBER_EATS, OrderType.GRUBHUB, OrderType.DOORDASH]
    
    # Sample menu items to choose from
    popular_items = [
        "chicken_sandwich", "deluxe_sandwich", "spicy_sandwich", "grilled_sandwich",
        "chicken_strips", "nuggets_8", "nuggets_12", "waffle_fries", "mac_cheese",
        "lemonade", "sweet_tea", "coke", "milkshake_vanilla", "chocolate_chip_cookie"
    ]
    
    print(f"Generating {num_orders} orders...")
    print()
    
    created_orders = []
    
    for i in range(num_orders):
        # Pick random customer and order type
        customer_name = random.choice(customer_names)
        order_type = random.choice(order_types)
        
        # Create customer
        customer = order_processor.create_customer(
            name=customer_name,
            phone=f"555-{random.randint(1000, 9999)}",
            email=f"{customer_name.lower().replace(' ', '.')}@example.com",
            loyalty_member=random.choice([True, False])
        )
        
        # Create order with 1-4 random items
        num_items = random.randint(1, 4)
        order_items = []
        
        for _ in range(num_items):
            item_id = random.choice(popular_items)
            quantity = random.randint(1, 3)
            
            # Add some random customizations
            customizations = {}
            if random.random() < 0.3:  # 30% chance of customizations
                customizations["special_request"] = random.choice([
                    "Extra crispy", "No pickles", "Light sauce", "Extra sauce", "Well done"
                ])
            
            from order_simulator import OrderItem, MENU_DICT
            order_item = OrderItem(
                menu_item=MENU_DICT[item_id],
                quantity=quantity,
                special_instructions=random.choice([
                    "", "Please make it fresh!", "Extra napkins", "No onions", "On the side"
                ]),
                customizations=customizations
            )
            order_items.append(order_item)
        
        # Create the order
        order = order_processor.create_order(
            order_type=order_type,
            customer=customer,
            items=order_items,
            special_instructions=random.choice([
                "", "Please hurry!", "Take your time", "Extra careful with packaging"
            ])
        )
        
        # Confirm the order
        order_processor.confirm_order(order.id)
        created_orders.append(order)
        
        # If it's a delivery order, create it in external service
        if order_type in [OrderType.UBER_EATS, OrderType.GRUBHUB, OrderType.DOORDASH]:
            try:
                external_response = external_services.create_order(order)
                print(f"✅ {i+1:2d}. {order_type.value:10s} | {customer_name:15s} | ${order.total_amount:6.2f} | External ID: {external_response['order_id']}")
            except Exception as e:
                print(f"❌ {i+1:2d}. {order_type.value:10s} | {customer_name:15s} | ${order.total_amount:6.2f} | Error: {e}")
        else:
            print(f"✅ {i+1:2d}. {order_type.value:10s} | {customer_name:15s} | ${order.total_amount:6.2f}")
        
        # Small delay to make it more realistic
        time.sleep(0.1)
    
    print()
    print("📊 Order Summary:")
    print("-" * 40)
    
    # Show statistics
    stats = order_processor.get_order_statistics()
    print(f"Total Orders: {stats['total_orders']}")
    print(f"Total Value: ${sum(order.total_amount for order in created_orders):.2f}")
    print(f"Average Order Value: ${stats['average_order_value']:.2f}")
    
    print("\nOrders by Type:")
    for order_type, count in stats['orders_by_type'].items():
        if count > 0:
            print(f"  {order_type.replace('_', ' ').title()}: {count}")
    
    print("\nOrders by Status:")
    for status, count in [
        ("Pending", stats['pending_orders']),
        ("Preparing", stats['preparing_orders']),
        ("Ready", stats['ready_orders']),
        ("Completed", stats['completed_orders']),
        ("Cancelled", stats['cancelled_orders'])
    ]:
        if count > 0:
            print(f"  {status}: {count}")
    
    print("\n🍽️ Sample Order Details:")
    print("-" * 40)
    
    # Show details for first 3 orders
    for i, order in enumerate(created_orders[:3]):
        print(f"\nOrder {i+1} - {order.id[:8]}...")
        print(f"  Type: {order.order_type.value}")
        print(f"  Customer: {order.customer.name}")
        print(f"  Total: ${order.total_amount:.2f}")
        print(f"  Items:")
        for item in order.items:
            print(f"    • {item.menu_item.name} x{item.quantity} - ${item.price:.2f}")
    
    print(f"\n🎉 Generated {len(created_orders)} orders successfully!")
    print("Run 'python3 restaurant_simulator.py' to see the simulation in action!")

if __name__ == "__main__":
    import sys
    
    # Allow user to specify number of orders
    num_orders = 10
    if len(sys.argv) > 1:
        try:
            num_orders = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 generate_orders.py [number_of_orders]")
            print("Default: 10 orders")
            sys.exit(1)
    
    generate_sample_orders(num_orders)
