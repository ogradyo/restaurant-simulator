#!/usr/bin/env python3
"""
Restaurant Message Demo

This script demonstrates how to use the standalone order simulator to create
order messages and route them to various restaurant applications.
"""

import os
import sys
import time
import json
from datetime import datetime

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from order_simulator import (
    OrderProcessor, OrderType, OrderItem, MENU_DICT, 
    OrderMessageGenerator, OrderMessageDelivery, 
    MessageRouter, MessageRouterBuilder, create_standard_restaurant_router
)

class RestaurantMessageDemo:
    """Demo class for restaurant message routing"""
    
    def __init__(self):
        self.order_processor = OrderProcessor()
        self.message_generator = OrderMessageGenerator()
        self.message_delivery = OrderMessageDelivery()
        self.router = None
        self.setup_directories()
    
    def setup_directories(self):
        """Create output directories for different systems"""
        directories = [
            "pos_orders",
            "kitchen_orders", 
            "delivery_orders",
            "inventory_updates",
            "analytics_data",
            "message_logs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created directory: {directory}")
    
    def setup_message_router(self):
        """Setup the message router with standard restaurant routes"""
        print("\n🔧 Setting up message router...")
        
        # Create a custom router with specific configurations
        self.router = (MessageRouterBuilder()
                      .add_pos_system_route(
                          destination="pos_orders",
                          file_extension="json"
                      )
                      .add_kitchen_display_route(
                          destination="kitchen_orders",
                          file_extension="json"
                      )
                      .add_delivery_service_route(
                          destination="delivery_orders",
                          file_extension="json"
                      )
                      .add_inventory_system_route(
                          destination="inventory_updates",
                          file_extension="csv"
                      )
                      .add_analytics_system_route(
                          destination="analytics_data",
                          file_extension="json"
                      )
                      .add_custom_route(
                          name="message_logger",
                          destination="message_logs",
                          method="file",
                          format_filter=["json"],
                          file_extension="json"
                      )
                      .build())
        
        # Register the delivery handler
        self.router.register_delivery_handler(self.message_delivery)
        
        # Start async processing
        self.router.start_async_processing()
        
        print("✅ Message router configured and started")
    
    def create_sample_orders(self, num_orders: int = 8) -> list:
        """Create sample orders of different types"""
        print(f"\n🍗 Creating {num_orders} sample orders...")
        
        orders = []
        customer_names = [
            "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", 
            "Emma Brown", "Frank Miller", "Grace Lee", "Henry Taylor"
        ]
        
        order_types = [
            OrderType.DRIVE_THRU, OrderType.DINE_IN, OrderType.UBER_EATS,
            OrderType.GRUBHUB, OrderType.DOORDASH
        ]
        
        for i in range(num_orders):
            # Select order type
            order_type = order_types[i % len(order_types)]
            customer_name = customer_names[i % len(customer_names)]
            
            # Create customer
            customer = self.order_processor.create_customer(
                name=customer_name,
                phone=f"555-{1000 + i:04d}",
                email=f"{customer_name.lower().replace(' ', '.')}@example.com",
                loyalty_member=i % 4 == 0
            )
            
            # Create order items
            items = self._create_order_items(order_type)
            
            # Create order
            order = self.order_processor.create_order(
                order_type=order_type,
                customer=customer,
                items=items,
                special_instructions=self._get_special_instructions(order_type)
            )
            
            # Confirm order
            self.order_processor.confirm_order(order.id)
            orders.append(order)
            
            print(f"  ✅ {order_type.value:10s} | {customer_name:15s} | ${order.total_amount:6.2f}")
        
        return orders
    
    def _create_order_items(self, order_type: OrderType) -> list:
        """Create order items based on order type"""
        items = []
        
        # Different item sets for different order types
        if order_type in [OrderType.DRIVE_THRU, OrderType.DINE_IN]:
            # Quick service items
            item_ids = ["chicken_sandwich", "waffle_fries", "lemonade"]
        elif order_type in [OrderType.UBER_EATS, OrderType.GRUBHUB, OrderType.DOORDASH]:
            # Delivery items (more complex orders)
            item_ids = ["deluxe_sandwich", "chicken_strips", "mac_cheese", "sweet_tea"]
        else:
            item_ids = ["grilled_sandwich", "fruit_cup", "coke"]
        
        import random
        num_items = random.randint(1, min(3, len(item_ids)))
        selected_items = random.sample(item_ids, num_items)
        
        for item_id in selected_items:
            if item_id in MENU_DICT:
                quantity = random.randint(1, 2)
                customizations = {}
                
                # Add customizations for delivery orders
                if order_type in [OrderType.UBER_EATS, OrderType.GRUBHUB, OrderType.DOORDASH]:
                    if random.random() < 0.4:  # 40% chance
                        customizations["special_request"] = random.choice([
                            "Extra crispy", "No pickles", "Light sauce", "Well done"
                        ])
                
                order_item = OrderItem(
                    menu_item=MENU_DICT[item_id],
                    quantity=quantity,
                    special_instructions=random.choice([
                        "", "Please make it fresh!", "Extra napkins", "No onions"
                    ]),
                    customizations=customizations
                )
                items.append(order_item)
        
        return items
    
    def _get_special_instructions(self, order_type: OrderType) -> str:
        """Get special instructions based on order type"""
        import random
        
        if order_type == OrderType.DRIVE_THRU:
            return random.choice(["", "Please hurry!", "Extra napkins"])
        elif order_type in [OrderType.UBER_EATS, OrderType.GRUBHUB, OrderType.DOORDASH]:
            return random.choice([
                "", "Extra careful with packaging", "No onions please", 
                "Well done", "Extra napkins"
            ])
        else:
            return random.choice(["", "Take your time", "Extra careful"])
    
    def generate_and_route_messages(self, orders: list):
        """Generate messages for orders and route them to appropriate systems"""
        print(f"\n📤 Generating and routing messages for {len(orders)} orders...")
        
        formats = ["json", "pos", "kitchen", "delivery", "csv"]
        routed_messages = []
        
        for i, order in enumerate(orders):
            print(f"\n📋 Processing order {i+1}/{len(orders)}: {order.id[:8]}... ({order.order_type.value})")
            
            # Generate messages in different formats
            for format_type in formats:
                try:
                    message = self.message_generator.generate_order_message(
                        order, format_type, include_metadata=True
                    )
                    
                    # Route the message
                    routed_to = self.router.route_message(message)
                    
                    if routed_to:
                        print(f"  ✅ {format_type:8s} -> {', '.join(routed_to)}")
                        routed_messages.append({
                            "order_id": order.id,
                            "format": format_type,
                            "routed_to": routed_to,
                            "message": message
                        })
                    else:
                        print(f"  ⚠️  {format_type:8s} -> No routes matched")
                
                except Exception as e:
                    print(f"  ❌ {format_type:8s} -> Error: {e}")
            
            # Small delay to show async processing
            time.sleep(0.5)
        
        return routed_messages
    
    def show_router_statistics(self):
        """Show router statistics"""
        print(f"\n📊 Message Router Statistics:")
        print("=" * 50)
        
        stats = self.router.get_route_statistics()
        
        for route_name, data in stats.items():
            print(f"\n{route_name}:")
            print(f"  Destination: {data['destination']}")
            print(f"  Method: {data['method']}")
            print(f"  Enabled: {data['enabled']}")
            print(f"  Messages: {data['message_count']}")
            print(f"  Errors: {data['errors']}")
            print(f"  Success Rate: {data['success_rate']:.1f}%")
            if data['last_delivery']:
                print(f"  Last Delivery: {data['last_delivery']}")
    
    def show_file_listings(self):
        """Show generated files in each directory"""
        print(f"\n📁 Generated Files:")
        print("=" * 50)
        
        directories = [
            "pos_orders", "kitchen_orders", "delivery_orders", 
            "inventory_updates", "analytics_data", "message_logs"
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                files = os.listdir(directory)
                if files:
                    print(f"\n{directory}/:")
                    for file in sorted(files):
                        file_path = os.path.join(directory, file)
                        size = os.path.getsize(file_path)
                        print(f"  {file} ({size} bytes)")
                else:
                    print(f"\n{directory}/: (empty)")
    
    def run_demo(self):
        """Run the complete demo"""
        print("🍗 Restaurant Message Routing Demo 🍗")
        print("=" * 50)
        
        # Setup
        self.setup_message_router()
        
        # Create orders
        orders = self.create_sample_orders(6)
        
        # Generate and route messages
        routed_messages = self.generate_and_route_messages(orders)
        
        # Wait for async processing to complete
        print(f"\n⏳ Waiting for async message processing to complete...")
        time.sleep(3)
        
        # Show statistics
        self.show_router_statistics()
        
        # Show file listings
        self.show_file_listings()
        
        # Show sample message content
        self.show_sample_messages(routed_messages)
        
        # Cleanup
        self.router.stop_async_processing()
        
        print(f"\n🎉 Demo completed! Check the generated directories for message files.")
    
    def show_sample_messages(self, routed_messages: list):
        """Show sample message content"""
        print(f"\n📄 Sample Message Content:")
        print("=" * 50)
        
        if routed_messages:
            # Show first message as example
            sample = routed_messages[0]
            message = sample["message"]
            
            print(f"\nOrder: {sample['order_id'][:8]}...")
            print(f"Format: {sample['format']}")
            print(f"Routed to: {', '.join(sample['routed_to'])}")
            print(f"\nContent preview:")
            print("-" * 30)
            
            # Show first 20 lines of content
            content_lines = message["content"].split('\n')
            for line in content_lines[:20]:
                print(line)
            
            if len(content_lines) > 20:
                print("... (truncated)")

def main():
    """Main function"""
    demo = RestaurantMessageDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
