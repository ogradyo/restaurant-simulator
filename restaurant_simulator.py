from order_simulator import OrderProcessor, ExternalServiceManager, OrderType, OrderStatus, OrderItem, MENU_DICT, get_menu_by_category, ItemCategory
from typing import List, Dict, Any
import json
import time
from datetime import datetime

class RestaurantSimulator:
    """Main restaurant simulator class"""
    
    def __init__(self):
        self.order_processor = OrderProcessor()
        self.external_services = ExternalServiceManager()
        self.running = False
        self.simulation_speed = 1.0  # 1.0 = real time, 2.0 = 2x speed, etc.
    
    def start_simulation(self):
        """Start the restaurant simulation"""
        self.running = True
        print("🍗 ACSP (A Chicken Sandwich Place) Restaurant Simulator Started! 🍗")
        print("=" * 50)
        
        while self.running:
            self._process_orders()
            self._display_status()
            time.sleep(5 / self.simulation_speed)  # Update every 5 seconds
    
    def stop_simulation(self):
        """Stop the restaurant simulation"""
        self.running = False
        print("\n🛑 Simulation stopped.")
    
    def create_sample_order(self, order_type: OrderType, customer_name: str) -> str:
        """Create a sample order for testing"""
        customer = self.order_processor.create_customer(
            name=customer_name,
            phone="555-0123",
            email=f"{customer_name.lower().replace(' ', '.')}@example.com",
            loyalty_member=order_type == OrderType.DRIVE_THRU
        )
        
        # Create a sample order with popular items
        sample_items = self._get_sample_items()
        order = self.order_processor.create_order(
            order_type=order_type,
            customer=customer,
            items=sample_items,
            special_instructions="Please make it fresh!"
        )
        
        # Confirm the order
        self.order_processor.confirm_order(order.id)
        
        # If it's a delivery order, create it in the external service
        if order_type in [OrderType.UBER_EATS, OrderType.GRUBHUB, OrderType.DOORDASH]:
            try:
                external_response = self.external_services.create_order(order)
                print(f"✅ Created {order_type.value} order: {external_response['order_id']}")
            except Exception as e:
                print(f"❌ Error creating external order: {e}")
        
        return order.id
    
    def _get_sample_items(self) -> List[OrderItem]:
        """Get sample menu items for testing"""
        sample_items = []
        
        # Add a chicken sandwich
        if "chicken_sandwich" in MENU_DICT:
            sample_items.append(OrderItem(
                menu_item=MENU_DICT["chicken_sandwich"],
                quantity=1,
                special_instructions="No pickle"
            ))
        
        # Add waffle fries
        if "waffle_fries" in MENU_DICT:
            sample_items.append(OrderItem(
                menu_item=MENU_DICT["waffle_fries"],
                quantity=1
            ))
        
        # Add a drink
        if "lemonade" in MENU_DICT:
            sample_items.append(OrderItem(
                menu_item=MENU_DICT["lemonade"],
                quantity=1
            ))
        
        return sample_items
    
    def _process_orders(self):
        """Process orders in the queue"""
        # Move confirmed orders to preparation
        confirmed_orders = self.order_processor.get_orders_by_status(OrderStatus.CONFIRMED)
        for order in confirmed_orders:
            if self.order_processor.start_preparation(order.id):
                print(f"👨‍🍳 Started preparing order {order.id} ({order.order_type.value})")
        
        # Complete orders that are ready
        preparing_orders = self.order_processor.get_orders_by_status(OrderStatus.PREPARING)
        for order in preparing_orders:
            # Simulate preparation time
            if order.estimated_ready_time and datetime.now() >= order.estimated_ready_time:
                if self.order_processor.complete_order(order.id):
                    print(f"✅ Order {order.id} is ready for pickup/delivery!")
    
    def _display_status(self):
        """Display current restaurant status"""
        stats = self.order_processor.get_order_statistics()
        
        print(f"\n📊 Restaurant Status - {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 40)
        print(f"Total Orders: {stats['total_orders']}")
        print(f"Pending: {stats['pending_orders']} | Preparing: {stats['preparing_orders']} | Ready: {stats['ready_orders']}")
        print(f"Completed: {stats['completed_orders']} | Cancelled: {stats['cancelled_orders']}")
        print(f"Average Order Value: ${stats['average_order_value']}")
        
        # Show orders by type
        print("\nOrders by Type:")
        for order_type, count in stats['orders_by_type'].items():
            if count > 0:
                print(f"  {order_type.replace('_', ' ').title()}: {count}")
        
        # Show current queue
        if self.order_processor.order_queue:
            print(f"\nCurrent Queue ({len(self.order_processor.order_queue)} orders):")
            for i, order_id in enumerate(self.order_processor.order_queue[:5], 1):
                order = self.order_processor.get_order(order_id)
                if order:
                    wait_time = self.order_processor.get_estimated_wait_time(order_id)
                    print(f"  {i}. Order {order_id[:8]}... ({order.order_type.value}) - {wait_time}min")
    
    def get_menu_display(self) -> str:
        """Get a formatted menu display"""
        menu_display = "🍗 ACSP (A Chicken Sandwich Place) Menu 🍗\n"
        menu_display += "=" * 30 + "\n\n"
        
        for category in ItemCategory:
            items = get_menu_by_category(category)
            if items:
                menu_display += f"{category.value.replace('_', ' ').title()}:\n"
                menu_display += "-" * 20 + "\n"
                
                for item in items:
                    menu_display += f"• {item.name} - ${item.base_price:.2f}\n"
                    menu_display += f"  {item.description[:60]}...\n"
                    menu_display += f"  Calories: {item.calories} | Prep: {item.preparation_time}min\n\n"
        
        return menu_display
    
    def get_order_details(self, order_id: str) -> str:
        """Get detailed information about an order"""
        order = self.order_processor.get_order(order_id)
        if not order:
            return "Order not found."
        
        details = f"Order Details - {order_id}\n"
        details += "=" * 30 + "\n"
        details += f"Type: {order.order_type.value.replace('_', ' ').title()}\n"
        details += f"Customer: {order.customer.name}\n"
        details += f"Status: {order.status.value.title()}\n"
        details += f"Order Time: {order.order_time.strftime('%H:%M:%S')}\n"
        details += f"Total: ${order.total_amount:.2f}\n"
        
        if order.estimated_ready_time:
            details += f"Estimated Ready: {order.estimated_ready_time.strftime('%H:%M:%S')}\n"
        
        if order.external_order_id:
            details += f"External ID: {order.external_order_id}\n"
        
        details += "\nItems:\n"
        for i, item in enumerate(order.items, 1):
            details += f"  {i}. {item.menu_item.name} x{item.quantity} - ${item.price:.2f}\n"
            if item.special_instructions:
                details += f"     Note: {item.special_instructions}\n"
        
        return details

def main():
    """Main function to run the simulator"""
    simulator = RestaurantSimulator()
    
    print("Welcome to the ACSP (A Chicken Sandwich Place) Restaurant Simulator!")
    print("Commands:")
    print("  start - Start the simulation")
    print("  stop - Stop the simulation")
    print("  menu - Display the menu")
    print("  order <type> <name> - Create a sample order")
    print("  status - Show current status")
    print("  details <order_id> - Show order details")
    print("  quit - Exit the simulator")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().lower().split()
            
            if not command:
                continue
            
            if command[0] == "quit":
                if simulator.running:
                    simulator.stop_simulation()
                break
            
            elif command[0] == "start":
                if not simulator.running:
                    simulator.start_simulation()
                else:
                    print("Simulation is already running!")
            
            elif command[0] == "stop":
                if simulator.running:
                    simulator.stop_simulation()
                else:
                    print("No simulation running.")
            
            elif command[0] == "menu":
                print(simulator.get_menu_display())
            
            elif command[0] == "order":
                if len(command) < 3:
                    print("Usage: order <type> <name>")
                    print("Types: drive_thru, dine_in, uber_eats, grubhub, doordash")
                    continue
                
                order_type_str = command[1].lower()
                customer_name = " ".join(command[2:])
                
                try:
                    order_type = OrderType(order_type_str)
                    order_id = simulator.create_sample_order(order_type, customer_name)
                    print(f"Created order: {order_id}")
                except ValueError:
                    print("Invalid order type. Use: drive_thru, dine_in, uber_eats, grubhub, doordash")
            
            elif command[0] == "status":
                simulator._display_status()
            
            elif command[0] == "details":
                if len(command) < 2:
                    print("Usage: details <order_id>")
                    continue
                
                order_id = command[1]
                print(simulator.get_order_details(order_id))
            
            else:
                print("Unknown command. Type 'quit' to exit.")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            if simulator.running:
                simulator.stop_simulation()
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
