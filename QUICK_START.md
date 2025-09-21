# Quick Start Guide

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
