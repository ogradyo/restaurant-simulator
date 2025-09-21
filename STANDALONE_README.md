# Standalone Order Message Generator

The order_simulator has been enhanced to support standalone operation for creating order messages that can be delivered to various restaurant applications via different messaging mechanisms.

## Features

### 🚀 Standalone Operation
- Generate orders without running the full restaurant simulation
- Create order messages in multiple formats (JSON, XML, CSV, POS, Kitchen, Delivery)
- Route messages to different restaurant systems automatically
- Support for continuous order generation

### 📤 Message Formats
- **JSON**: Standard JSON format for general integration
- **XML**: XML format for legacy systems
- **CSV**: Comma-separated values for data analysis
- **POS**: Point-of-sale system specific format
- **Kitchen**: Kitchen display system format
- **Delivery**: Delivery service integration format

### 🎯 Message Routing
- Automatic routing based on order type and format
- Support for multiple delivery methods (file, HTTP, message queue)
- Configurable routing rules
- Real-time message processing

## Quick Start

### 1. Generate Sample Orders

```bash
# Generate 5 orders in JSON and POS formats
python standalone_order_generator.py --num-orders 5 --formats json pos kitchen

# Generate orders for specific order types
python standalone_order_generator.py --order-types drive_thru uber_eats --formats json

# Run in continuous mode (generates orders every 30 seconds)
python standalone_order_generator.py --continuous --interval 30
```

### 2. Run the Demo

```bash
# Run the complete message routing demo
python restaurant_message_demo.py
```

### 3. Create Configuration

```bash
# Create a sample configuration file
python standalone_order_generator.py --create-config
```

## Usage Examples

### Basic Order Generation

```python
from order_simulator import OrderProcessor, OrderType, OrderItem, MENU_DICT
from order_simulator.message_generator import OrderMessageGenerator, OrderMessageDelivery

# Initialize components
processor = OrderProcessor()
message_generator = OrderMessageGenerator()
delivery = OrderMessageDelivery()

# Create an order
customer = processor.create_customer("John Doe", "555-1234")
items = [OrderItem(menu_item=MENU_DICT["chicken_sandwich"], quantity=1)]
order = processor.create_order(OrderType.DRIVE_THRU, customer, items)
processor.confirm_order(order.id)

# Generate message
message = message_generator.generate_order_message(order, "json")

# Deliver message
delivery.deliver_message(message, "order.json", "file")
```

### Message Routing

```python
from order_simulator import MessageRouterBuilder, OrderMessageDelivery

# Create router with standard restaurant routes
router = (MessageRouterBuilder()
          .add_pos_system_route()
          .add_kitchen_display_route()
          .add_delivery_service_route()
          .build())

# Register delivery handler
delivery = OrderMessageDelivery()
router.register_delivery_handler(delivery)

# Start async processing
router.start_async_processing()

# Route messages
router.route_message(message)
```

## Configuration

### Configuration File (order_config.json)

```json
{
  "order_generation": {
    "num_orders": 5,
    "order_types": ["drive_thru", "dine_in", "uber_eats", "grubhub", "doordash"],
    "include_metadata": true
  },
  "message_formats": {
    "json": {"enabled": true, "destination": "file"},
    "xml": {"enabled": true, "destination": "file"},
    "pos": {"enabled": true, "destination": "file"},
    "kitchen": {"enabled": true, "destination": "file"},
    "delivery": {"enabled": true, "destination": "file"}
  },
  "delivery": {
    "output_directory": "order_messages",
    "file_naming": "order_{order_id}_{format}_{timestamp}",
    "http_endpoints": {
      "pos_system": "http://localhost:8080/api/orders",
      "kitchen_display": "http://localhost:8081/api/kitchen"
    }
  }
}
```

## Message Formats

### JSON Format
```json
{
  "order_id": "abc123",
  "order_type": "drive_thru",
  "status": "confirmed",
  "customer": {
    "name": "John Doe",
    "phone": "555-1234"
  },
  "items": [
    {
      "name": "ACSP Chicken Sandwich",
      "quantity": 1,
      "price": 4.79
    }
  ],
  "totals": {
    "subtotal": 4.79,
    "tax_amount": 0.38,
    "total_amount": 5.17
  }
}
```

### POS System Format
```json
{
  "transaction_id": "abc123",
  "transaction_type": "ORDER",
  "customer": {
    "name": "John Doe",
    "loyalty_number": "12345"
  },
  "order_details": {
    "items": [
      {
        "sku": "chicken_sandwich",
        "name": "ACSP Chicken Sandwich",
        "qty": 1,
        "price": 4.79
      }
    ],
    "total": 5.17
  }
}
```

### Kitchen Display Format
```json
{
  "order_number": "abc123",
  "order_type": "DRIVE_THRU",
  "customer_name": "John Doe",
  "items": [
    {
      "name": "ACSP Chicken Sandwich",
      "quantity": 1,
      "prep_time": 6,
      "instructions": "No pickle"
    }
  ],
  "priority": "HIGH"
}
```

## Integration Examples

### 1. POS System Integration

```python
# Generate POS-specific messages
message = message_generator.generate_order_message(order, "pos")
delivery.deliver_message(message, "pos_orders/order.json", "file")
```

### 2. Kitchen Display Integration

```python
# Generate kitchen display messages
message = message_generator.generate_order_message(order, "kitchen")
delivery.deliver_message(message, "kitchen_orders/order.json", "file")
```

### 3. HTTP API Integration

```python
# Send messages via HTTP
message = message_generator.generate_order_message(order, "json")
delivery.deliver_message(message, "http://localhost:8080/api/orders", "http")
```

### 4. Message Queue Integration

```python
# Send to message queue
message = message_generator.generate_order_message(order, "json")
delivery.deliver_message(message, "order_queue", "mq")
```

## Command Line Interface

### Basic Usage
```bash
python standalone_order_generator.py [options]
```

### Options
- `--num-orders, -n`: Number of orders to generate (default: 5)
- `--formats, -f`: Message formats to generate (json, xml, csv, pos, kitchen, delivery)
- `--order-types, -t`: Order types to generate (drive_thru, dine_in, uber_eats, grubhub, doordash)
- `--output-dir, -o`: Output directory for messages (default: order_messages)
- `--continuous, -c`: Run in continuous mode
- `--interval, -i`: Interval in seconds for continuous mode (default: 30)
- `--create-config`: Create a sample configuration file
- `--config`: Configuration file path (default: order_config.json)

### Examples

```bash
# Generate 10 orders in JSON and POS formats
python standalone_order_generator.py -n 10 -f json pos

# Generate only drive-thru and dine-in orders
python standalone_order_generator.py -t drive_thru dine_in -f json kitchen

# Run continuously with custom interval
python standalone_order_generator.py -c -i 60 -f json pos kitchen

# Use custom configuration
python standalone_order_generator.py --config my_config.json
```

## File Structure

```
restaurant-simulator/
├── order_simulator/
│   ├── message_generator.py      # Message generation
│   ├── message_router.py         # Message routing
│   └── ...                       # Other modules
├── standalone_order_generator.py # CLI application
├── restaurant_message_demo.py    # Demo application
├── order_config.json            # Configuration file
└── order_messages/              # Generated messages
    ├── pos_orders/
    ├── kitchen_orders/
    ├── delivery_orders/
    └── ...
```

## Advanced Features

### Custom Message Formats

```python
# Create custom message format
def custom_format(message_data):
    return {
        "format": "custom",
        "content": f"Order {message_data['order_id']} for {message_data['customer']['name']}",
        "content_type": "text/plain"
    }

# Register custom format
message_generator.register_format("custom", custom_format)
```

### Custom Delivery Methods

```python
# Create custom delivery method
def custom_delivery(message, destination, **kwargs):
    # Custom delivery logic
    print(f"Delivering to {destination}")
    return True

# Register custom delivery method
delivery.register_delivery_method("custom", custom_delivery)
```

### Message Filtering

```python
# Create route with filters
route = MessageRoute(
    name="pos_only",
    destination="pos_orders",
    method="file",
    format_filter=["pos", "json"],
    order_type_filter=["drive_thru", "dine_in"]
)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the correct directory
2. **File Permissions**: Ensure write permissions for output directories
3. **Configuration Errors**: Validate JSON configuration files
4. **Network Issues**: Check HTTP endpoints for connectivity

### Debug Mode

```bash
# Enable debug output
python standalone_order_generator.py --debug
```

## Contributing

To add new message formats or delivery methods:

1. Extend the `OrderMessageGenerator` class
2. Add new format methods following the naming convention `_format_as_<format>`
3. Update the CLI options and help text
4. Add tests for the new functionality

## License

This project is for educational and demonstration purposes.
