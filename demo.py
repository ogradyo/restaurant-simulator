#!/usr/bin/env python3
"""
Demo script for the ACSP (A Chicken Sandwich Place) Restaurant Simulator
This script demonstrates the various features of the simulator
"""

from restaurant_simulator import RestaurantSimulator
from order_simulator import OrderType
import time

def run_demo():
    """Run a demonstration of the restaurant simulator"""
    print("🍗 ACSP (A Chicken Sandwich Place) Restaurant Simulator Demo 🍗")
    print("=" * 50)
    
    # Create simulator instance
    simulator = RestaurantSimulator()
    
    # Set simulation speed to 2x for demo purposes
    simulator.simulation_speed = 2.0
    
    print("\n1. Creating sample orders...")
    
    # Create various types of orders
    orders = []
    
    # Drive-thru order
    drive_thru_order = simulator.create_sample_order(OrderType.DRIVE_THRU, "Alice Johnson")
    orders.append(drive_thru_order)
    print(f"   ✅ Created drive-thru order: {drive_thru_order}")
    
    # Dine-in order
    dine_in_order = simulator.create_sample_order(OrderType.DINE_IN, "Bob Smith")
    orders.append(dine_in_order)
    print(f"   ✅ Created dine-in order: {dine_in_order}")
    
    # Uber Eats order
    uber_order = simulator.create_sample_order(OrderType.UBER_EATS, "Carol Davis")
    orders.append(uber_order)
    print(f"   ✅ Created Uber Eats order: {uber_order}")
    
    # Grubhub order
    grubhub_order = simulator.create_sample_order(OrderType.GRUBHUB, "David Wilson")
    orders.append(grubhub_order)
    print(f"   ✅ Created Grubhub order: {grubhub_order}")
    
    print("\n2. Starting simulation...")
    print("   (Press Ctrl+C to stop the demo)")
    
    try:
        # Start simulation in background
        simulator.running = True
        
        # Run simulation for demo
        for i in range(10):  # Run for 10 iterations
            simulator._process_orders()
            simulator._display_status()
            
            # Show order details for first few orders
            if i < 3 and i < len(orders):
                print(f"\n📋 Order Details for {orders[i][:8]}...")
                print(simulator.get_order_details(orders[i]))
            
            time.sleep(3)  # Wait 3 seconds between updates
            
    except KeyboardInterrupt:
        print("\n\n🛑 Demo stopped by user")
    
    finally:
        simulator.stop_simulation()
    
    print("\n3. Final Statistics:")
    stats = simulator.order_processor.get_order_statistics()
    print(f"   Total Orders: {stats['total_orders']}")
    print(f"   Completed: {stats['completed_orders']}")
    print(f"   Average Order Value: ${stats['average_order_value']}")
    
    print("\n4. External Service Statistics:")
    ext_stats = simulator.external_services.get_service_statistics()
    for service, data in ext_stats.items():
        print(f"   {service.replace('_', ' ').title()}: {data['total_orders']} orders")
    
    print("\n🎉 Demo completed! Run 'python restaurant_simulator.py' for interactive mode.")

if __name__ == "__main__":
    run_demo()
