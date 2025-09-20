# ACSP (A Chicken Sandwich Place) Restaurant Simulator

A comprehensive restaurant simulation system that handles drive-thru, dine-in, and external delivery service orders (Uber Eats, Grubhub, DoorDash) with an ACSP inspired menu.

## Features

### Order Types
- **Drive-Thru**: Traditional drive-through orders
- **Dine-In**: In-restaurant dining orders  
- **External Delivery**: Integration with delivery services
  - Uber Eats
  - Grubhub
  - DoorDash

### Menu Categories
- Sandwiches (Chicken Sandwich, Deluxe, Spicy, Grilled)
- Chicken Strips & Nuggets
- Salads (Cobb, Market)
- Sides (Waffle Fries, Mac & Cheese, Fruit Cup)
- Beverages (Lemonade, Sweet Tea, Soft Drinks, Milkshakes)
- Desserts (Cookies, Brownies)
- Breakfast Items
- Kids Meals

### Order Management
- Real-time order processing
- Order status tracking (Pending → Confirmed → Preparing → Ready → Completed)
- Queue management and wait time estimation
- Order customization and special instructions
- Customer management with loyalty program support

### External Service Integration
- Mock API integrations for delivery services
- Automatic order creation in external systems
- Status synchronization
- Delivery fee and service fee calculation
- Order cancellation handling

## Installation

1. Clone or download the project files
2. Ensure Python 3.7+ is installed
3. No additional dependencies required (uses only Python standard library)

## Usage

### Running the Simulator

**Option 1: Direct execution**
```bash
python restaurant_simulator.py
```

**Option 2: Using the run script**
```bash
python run_simulator.py
```

**Option 3: As a module**
```bash
python -m restaurant_simulator
```

### Available Commands

- `start` - Start the simulation
- `stop` - Stop the simulation  
- `menu` - Display the complete menu
- `order <type> <name>` - Create a sample order
  - Types: `drive_thru`, `dine_in`, `uber_eats`, `grubhub`, `doordash`
- `status` - Show current restaurant status
- `details <order_id>` - Show detailed order information
- `quit` - Exit the simulator

### Example Usage

```bash
# Start the simulation
start

# Create a drive-thru order
order drive_thru John Smith

# Create a delivery order
order uber_eats Jane Doe

# Check status
status

# View order details
details <order_id>

# Stop simulation
stop
```

## Project Structure

```
restaurant-simulator/
├── order_simulator/           # Order simulation package
│   ├── __init__.py           # Package initialization
│   ├── order_models.py       # Data models and enums
│   ├── menu_data.py          # Menu items and categories
│   ├── order_processor.py    # Order processing logic
│   └── external_services.py  # Delivery service integrations
├── restaurant_simulator.py   # Main simulator application
├── demo.py                   # Demo script
├── run_simulator.py          # Convenience run script
├── setup.py                  # Package setup script
├── requirements.txt          # Dependencies (none required)
└── README.md                # This file
```

## Key Components

### Order Models (`order_simulator/order_models.py`)
- `Order`: Main order entity with customer, items, and status
- `OrderItem`: Individual menu items with customizations
- `Customer`: Customer information and preferences
- `MenuItem`: Menu item definitions with pricing and nutrition info
- Enums for order types, statuses, and categories

### Menu System (`order_simulator/menu_data.py`)
- Comprehensive ACSP inspired menu
- 30+ menu items across 8 categories
- Nutritional information and allergen data
- Customization options for each item
- Search and filtering capabilities

### Order Processing (`order_simulator/order_processor.py`)
- Order creation and validation
- Status management and transitions
- Queue management and wait time calculation
- Order statistics and reporting
- Customer management

### External Services (`order_simulator/external_services.py`)
- Mock implementations of delivery service APIs
- Order creation and status management
- Fee calculation (delivery and service fees)
- Service-specific business logic

### Main Simulator (`restaurant_simulator.py`)
- Interactive CLI interface
- Real-time order processing simulation
- Status monitoring and display
- Sample order generation for testing

## Customization

### Adding New Menu Items
Edit `order_simulator/menu_data.py` and add new `MenuItem` objects to the `MENU_ITEMS` list.

### Adding New Order Types
1. Add new enum value to `OrderType` in `order_simulator/order_models.py`
2. Implement corresponding service in `order_simulator/external_services.py`
3. Update `ExternalServiceManager` to handle the new type

### Modifying Order Processing
Edit `order_simulator/order_processor.py` to customize order flow, validation rules, or business logic.

## Simulation Features

- **Real-time Processing**: Orders are processed in real-time with configurable speed
- **Queue Management**: Orders are queued and processed in order
- **Wait Time Estimation**: Calculates estimated wait times based on queue position
- **Status Tracking**: Complete order lifecycle tracking
- **Statistics**: Real-time restaurant performance metrics
- **External Integration**: Seamless integration with delivery services

## Future Enhancements

- Web-based dashboard interface
- Database persistence
- Real API integrations
- Payment processing
- Inventory management
- Staff scheduling
- Analytics and reporting
- Multi-location support

## License

This project is for educational and demonstration purposes.