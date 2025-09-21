#!/usr/bin/env python3
"""
Setup script for standalone order simulator
"""

import os
import sys
import json

def create_directories():
    """Create necessary directories"""
    directories = [
        "order_messages",
        "pos_orders",
        "kitchen_orders", 
        "delivery_orders",
        "inventory_updates",
        "analytics_data",
        "message_logs"
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}/")

def create_config_file():
    """Create a sample configuration file"""
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
    
    print("⚙️ Creating configuration file...")
    with open("order_config.json", "w") as f:
        json.dump(config, f, indent=2)
    print("  ✅ order_config.json")

def create_readme():
    """Create a quick start README"""
    readme_content = """# Quick Start Guide

## Basic Usage

1. Generate sample orders:
```bash
python standalone_order_generator.py --num-orders 5 --formats json pos kitchen
```

2. Run the demo:
```bash
python restaurant_message_demo.py
```

3. Run examples:
```bash
python example_usage.py
```

4. Run tests:
```bash
python test_standalone.py
```

## Available Commands

- `standalone_order_generator.py` - Main CLI application
- `restaurant_message_demo.py` - Complete demo with routing
- `example_usage.py` - Usage examples
- `test_standalone.py` - Test the functionality

## Configuration

Edit `order_config.json` to customize:
- Order generation settings
- Message formats
- Delivery destinations
- Continuous mode settings

## Output

Generated messages will be saved to:
- `order_messages/` - Main output directory
- `pos_orders/` - POS system messages
- `kitchen_orders/` - Kitchen display messages
- `delivery_orders/` - Delivery service messages
- `inventory_updates/` - Inventory system messages
- `analytics_data/` - Analytics messages
"""
    
    print("📖 Creating README...")
    with open("QUICK_START.md", "w") as f:
        f.write(readme_content)
    print("  ✅ QUICK_START.md")

def main():
    """Run setup"""
    print("🍗 Setting up Standalone Order Simulator 🍗")
    print("=" * 50)
    
    try:
        create_directories()
        create_config_file()
        create_readme()
        
        print("\n✅ Setup completed successfully!")
        print("\n🚀 Quick start:")
        print("   python standalone_order_generator.py --help")
        print("   python restaurant_message_demo.py")
        print("   python example_usage.py")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
