# Restaurant Order Processing Simulator

A Golang program that simulates a restaurant processing orders with realistic kitchen operations, order management, and delivery simulation.

## Features

- **Order Management**: Create, queue, and track orders through their lifecycle
- **Kitchen Simulation**: Multiple chefs working in parallel with capacity limits
- **Realistic Timing**: Different prep times for different menu items
- **Delivery System**: Simulated delivery times for completed orders
- **Statistics Tracking**: Real-time monitoring of restaurant operations
- **Concurrent Processing**: Uses goroutines for parallel order processing

## Order Lifecycle

1. **Received**: Order is created and added to the kitchen queue
2. **Preparing**: Kitchen staff is working on the order
3. **Ready**: Order is completed and ready for delivery
4. **Delivered**: Order has been delivered to the customer

## Menu Items

The simulator includes a variety of menu items with different preparation times:

- **Classic Burger** - $12.99 (8 minutes prep)
- **Margherita Pizza** - $15.99 (12 minutes prep)
- **Spaghetti Carbonara** - $14.99 (10 minutes prep)
- **Caesar Salad** - $9.99 (5 minutes prep)
- **Tomato Soup** - $6.99 (3 minutes prep)
- **French Fries** - $4.99 (4 minutes prep)

## Running the Simulation

```bash
# Navigate to the project directory
cd restaurant-simulator

# Run a single restaurant simulation (default: Restaurant #1, real-time mode)
go run main.go

# Run a specific restaurant simulation in real-time mode
go run main.go -restaurant=5 -mode=realtime

# Run in fast-forward mode (shows sequence without waiting)
go run main.go -restaurant=1 -mode=fastforward

# Run multiple restaurant simulations simultaneously
go run main.go -restaurant=1 -mode=fastforward &
go run main.go -restaurant=2 -mode=fastforward &
go run main.go -restaurant=3 -mode=fastforward &
wait
```

## Simulation Modes

### Real-Time Mode (Default)
- Simulates actual time delays
- Perfect for watching the restaurant operations unfold
- Shows realistic timing for order processing

### Fast-Forward Mode
- Shows the sequence of events without waiting
- Displays simulated delays with ⏱️ emoji
- Perfect for quick analysis and testing
- Useful for running multiple restaurant simulations

## Configuration

The restaurant can be configured with:
- Restaurant number (1-999, default: 1) - passed as command-line argument
- Simulation mode (realtime/fastforward, default: realtime)
- Number of chefs (default: 3)
- Kitchen capacity (default: 10 orders)
- Restaurant name (automatically generated as "Restaurant #X - The Golden Spoon")

## Command Line Arguments

- `-restaurant=N`: Specify the restaurant number (1-999)
- `-mode=MODE`: Simulation mode - 'realtime'/'rt' or 'fastforward'/'ff'
- `-h` or `--help`: Show help information

## Sample Output

The simulation will show:
- Order creation and processing
- Kitchen load and capacity
- Order status updates
- Delivery confirmations
- Final statistics including order counts by status
- Total processing times for each order

## Architecture

- **Restaurant**: Main system managing orders and statistics
- **Kitchen**: Handles order preparation with chef management
- **Order**: Represents individual customer orders
- **MenuItem**: Defines available menu items with pricing and prep times

The system uses Go channels for communication between components and goroutines for concurrent processing.
