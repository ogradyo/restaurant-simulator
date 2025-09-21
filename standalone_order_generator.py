#!/usr/bin/env python3
"""
Standalone Order Message Generator

This script generates order messages in various formats that can be delivered
to standalone restaurant applications via different mechanisms.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Any

# Add the current directory to the path so we can import order_simulator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from order_simulator import OrderProcessor, OrderType, OrderItem, MENU_DICT, get_available_items
from order_simulator.message_generator import OrderMessageGenerator, OrderMessageDelivery

class StandaloneOrderGenerator:
    """Standalone order generator for creating restaurant order messages"""
    
    def __init__(self):
        self.order_processor = OrderProcessor()
        self.message_generator = OrderMessageGenerator()
        self.message_delivery = OrderMessageDelivery()
        self.output_dir = "order_messages"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_sample_orders(self, num_orders: int = 5, order_types: List[str] = None) -> List[Dict[str, Any]]:
        """Generate sample orders with various types"""
        if order_types is None:
            order_types = ["drive_thru", "dine_in", "uber_eats", "grubhub", "doordash"]
        
        orders = []
        customer_names = [
            "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Emma Brown",
            "Frank Miller", "Grace Lee", "Henry Taylor", "Ivy Chen", "Jack Anderson"
        ]
        
        print(f"🍗 Generating {num_orders} sample orders...")
        
        for i in range(num_orders):
            # Select random order type
            order_type_str = order_types[i % len(order_types)]
            order_type = OrderType(order_type_str)
            
            # Create customer
            customer_name = customer_names[i % len(customer_names)]
            customer = self.order_processor.create_customer(
                name=customer_name,
                phone=f"555-{1000 + i:04d}",
                email=f"{customer_name.lower().replace(' ', '.')}@example.com",
                loyalty_member=i % 3 == 0  # Every 3rd customer is loyalty member
            )
            
            # Create order items
            items = self._create_sample_order_items()
            
            # Create order
            order = self.order_processor.create_order(
                order_type=order_type,
                customer=customer,
                items=items,
                special_instructions=self._get_random_special_instructions()
            )
            
            # Confirm order
            self.order_processor.confirm_order(order.id)
            orders.append(order)
            
            print(f"  ✅ Created {order_type.value} order for {customer_name}")
        
        return orders
    
    def _create_sample_order_items(self) -> List[OrderItem]:
        """Create sample order items"""
        items = []
        
        # Popular menu items
        popular_items = [
            "chicken_sandwich", "deluxe_sandwich", "spicy_sandwich", "grilled_sandwich",
            "chicken_strips", "nuggets_8", "waffle_fries", "mac_cheese", "lemonade", "sweet_tea"
        ]
        
        # Randomly select 1-4 items
        import random
        num_items = random.randint(1, 4)
        selected_items = random.sample(popular_items, min(num_items, len(popular_items)))
        
        for item_id in selected_items:
            if item_id in MENU_DICT:
                quantity = random.randint(1, 3)
                customizations = {}
                
                # Add some random customizations
                if random.random() < 0.3:  # 30% chance
                    customizations["special_request"] = random.choice([
                        "Extra crispy", "No pickles", "Light sauce", "Extra sauce", "Well done"
                    ])
                
                order_item = OrderItem(
                    menu_item=MENU_DICT[item_id],
                    quantity=quantity,
                    special_instructions=random.choice([
                        "", "Please make it fresh!", "Extra napkins", "No onions", "On the side"
                    ]),
                    customizations=customizations
                )
                items.append(order_item)
        
        return items
    
    def _get_random_special_instructions(self) -> str:
        """Get random special instructions"""
        import random
        instructions = [
            "", "Please hurry!", "Take your time", "Extra careful with packaging",
            "No onions please", "Extra napkins", "Well done", "Light on the sauce"
        ]
        return random.choice(instructions)
    
    def generate_messages(self, orders: List[Dict[str, Any]], formats: List[str] = None, 
                         destinations: List[str] = None) -> List[Dict[str, Any]]:
        """Generate messages for orders in various formats"""
        if formats is None:
            formats = ["json", "xml", "pos", "kitchen", "delivery"]
        
        if destinations is None:
            destinations = ["console"]
        
        messages = []
        
        print(f"\n📤 Generating messages in {len(formats)} formats...")
        
        for i, order in enumerate(orders):
            order_messages = []
            
            for format_type in formats:
                try:
                    message = self.message_generator.generate_order_message(
                        order, format_type, include_metadata=True
                    )
                    order_messages.append(message)
                    
                    # Deliver to destinations
                    for destination in destinations:
                        if destination == "console":
                            self.message_delivery.deliver_message(message, "", "console")
                        elif destination == "file":
                            filename = f"{self.output_dir}/order_{order.id}_{format_type}_{i+1}.{format_type}"
                            self.message_delivery.deliver_message(message, filename, "file")
                        else:
                            # Custom destination
                            self.message_delivery.deliver_message(message, destination, "file")
                    
                    print(f"  ✅ Generated {format_type} message for order {order.id[:8]}...")
                    
                except Exception as e:
                    print(f"  ❌ Error generating {format_type} message: {e}")
            
            messages.extend(order_messages)
        
        return messages
    
    def run_continuous_mode(self, interval: int = 30, formats: List[str] = None):
        """Run in continuous mode, generating orders at intervals"""
        if formats is None:
            formats = ["json", "pos", "kitchen"]
        
        print(f"🔄 Starting continuous mode - generating orders every {interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                # Generate 1-3 random orders
                import random
                num_orders = random.randint(1, 3)
                
                orders = self.generate_sample_orders(num_orders)
                self.generate_messages(orders, formats, ["file"])
                
                print(f"⏰ Waiting {interval} seconds for next batch...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Continuous mode stopped by user")
    
    def create_config_file(self, config_path: str = "order_config.json"):
        """Create a configuration file for the order generator"""
        config = {
            "order_generation": {
                "num_orders": 5,
                "order_types": ["drive_thru", "dine_in", "uber_eats", "grubhub", "doordash"],
                "include_metadata": True
            },
            "message_formats": {
                "json": {"enabled": True, "destination": "file"},
                "xml": {"enabled": True, "destination": "file"},
                "csv": {"enabled": False, "destination": "file"},
                "pos": {"enabled": True, "destination": "file"},
                "kitchen": {"enabled": True, "destination": "file"},
                "delivery": {"enabled": True, "destination": "file"}
            },
            "delivery": {
                "output_directory": "order_messages",
                "file_naming": "order_{order_id}_{format}_{timestamp}",
                "http_endpoints": {
                    "pos_system": "http://localhost:8080/api/orders",
                    "kitchen_display": "http://localhost:8081/api/kitchen",
                    "delivery_service": "http://localhost:8082/api/delivery"
                }
            },
            "continuous_mode": {
                "enabled": False,
                "interval_seconds": 30,
                "orders_per_batch": 3
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration file created: {config_path}")
    
    def load_config(self, config_path: str = "order_config.json") -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {config_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing configuration file: {e}")
            return {}

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Standalone Order Message Generator")
    parser.add_argument("--num-orders", "-n", type=int, default=5, 
                       help="Number of orders to generate (default: 5)")
    parser.add_argument("--formats", "-f", nargs="+", 
                       choices=["json", "xml", "csv", "pos", "kitchen", "delivery"],
                       default=["json", "pos", "kitchen"],
                       help="Message formats to generate")
    parser.add_argument("--order-types", "-t", nargs="+",
                       choices=["drive_thru", "dine_in", "uber_eats", "grubhub", "doordash"],
                       default=["drive_thru", "dine_in", "uber_eats"],
                       help="Order types to generate")
    parser.add_argument("--output-dir", "-o", default="order_messages",
                       help="Output directory for messages (default: order_messages)")
    parser.add_argument("--continuous", "-c", action="store_true",
                       help="Run in continuous mode")
    parser.add_argument("--interval", "-i", type=int, default=30,
                       help="Interval in seconds for continuous mode (default: 30)")
    parser.add_argument("--create-config", action="store_true",
                       help="Create a sample configuration file")
    parser.add_argument("--config", default="order_config.json",
                       help="Configuration file path (default: order_config.json)")
    
    args = parser.parse_args()
    
    generator = StandaloneOrderGenerator()
    generator.output_dir = args.output_dir
    
    if args.create_config:
        generator.create_config_file(args.config)
        return
    
    # Load configuration if it exists
    config = generator.load_config(args.config)
    
    print("🍗 Standalone Order Message Generator 🍗")
    print("=" * 50)
    
    if args.continuous:
        generator.run_continuous_mode(args.interval, args.formats)
    else:
        # Generate orders
        orders = generator.generate_sample_orders(args.num_orders, args.order_types)
        
        # Generate messages
        messages = generator.generate_messages(orders, args.formats, ["file", "console"])
        
        print(f"\n📊 Summary:")
        print(f"  Generated {len(orders)} orders")
        print(f"  Created {len(messages)} messages")
        print(f"  Output directory: {generator.output_dir}")
        
        # Show file listing
        if os.path.exists(generator.output_dir):
            files = os.listdir(generator.output_dir)
            if files:
                print(f"\n📁 Generated files:")
                for file in sorted(files):
                    print(f"  {file}")

if __name__ == "__main__":
    main()
