package main

import (
	"flag"
	"fmt"
	"log"
	"math/rand"
	"sync"
	"time"
)

// OrderStatus represents the current status of an order
type OrderStatus string

const (
	OrderReceived   OrderStatus = "received"
	OrderPreparing  OrderStatus = "preparing"
	OrderReady      OrderStatus = "ready"
	OrderDelivered  OrderStatus = "delivered"
	OrderCancelled  OrderStatus = "cancelled"
)

// Order represents a restaurant order
type Order struct {
	ID          int
	CustomerName string
	Items       []MenuItem
	TotalAmount float64
	Status      OrderStatus
	CreatedAt   time.Time
	ReadyAt     time.Time
	DeliveredAt time.Time
}

// MenuItem represents a single item in an order
type MenuItem struct {
	Name     string
	Price    float64
	PrepTime time.Duration
}

// Kitchen represents the restaurant kitchen
type Kitchen struct {
	RestaurantID int
	Mode         SimulationMode
	Chefs        int
	MaxCapacity  int
	CurrentLoad  int
	OrderQueue   chan *Order
	ReadyOrders  chan *Order
	mu           sync.RWMutex
}

// SimulationMode represents the type of simulation
type SimulationMode string

const (
	RealTimeMode    SimulationMode = "realtime"
	FastForwardMode SimulationMode = "fastforward"
)

// Restaurant represents the main restaurant system
type Restaurant struct {
	Name        string
	ID          int
	Mode        SimulationMode
	Kitchen     *Kitchen
	Orders      map[int]*Order
	OrderCount  int
	mu          sync.RWMutex
}

// NewRestaurant creates a new restaurant instance
func NewRestaurant(name string, id int, mode SimulationMode, chefs int, maxCapacity int) *Restaurant {
	return &Restaurant{
		Name:   name,
		ID:     id,
		Mode:   mode,
		Kitchen: NewKitchen(id, mode, chefs, maxCapacity),
		Orders: make(map[int]*Order),
	}
}

// NewKitchen creates a new kitchen instance
func NewKitchen(restaurantID int, mode SimulationMode, chefs int, maxCapacity int) *Kitchen {
	return &Kitchen{
		RestaurantID: restaurantID,
		Mode:        mode,
		Chefs:       chefs,
		MaxCapacity: maxCapacity,
		OrderQueue:  make(chan *Order, maxCapacity),
		ReadyOrders: make(chan *Order, maxCapacity),
	}
}

// CreateOrder creates a new order and adds it to the queue
func (r *Restaurant) CreateOrder(customerName string, items []MenuItem) *Order {
	r.mu.Lock()
	defer r.mu.Unlock()
	
	r.OrderCount++
	order := &Order{
		ID:          r.OrderCount,
		CustomerName: customerName,
		Items:       items,
		TotalAmount: calculateTotal(items),
		Status:      OrderReceived,
		CreatedAt:   time.Now(),
	}
	
	r.Orders[order.ID] = order
	r.Kitchen.OrderQueue <- order
	
	log.Printf("[Restaurant #%d] Order #%d created for %s - Total: $%.2f", r.ID, order.ID, customerName, order.TotalAmount)
	return order
}

// calculateTotal calculates the total amount for menu items
func calculateTotal(items []MenuItem) float64 {
	total := 0.0
	for _, item := range items {
		total += item.Price
	}
	return total
}

// simulateDelay handles time delays based on simulation mode
func simulateDelay(mode SimulationMode, duration time.Duration, description string) {
	if mode == RealTimeMode {
		time.Sleep(duration)
	} else {
		// In fast-forward mode, just log the delay without waiting
		log.Printf("⏱️  [SIMULATED] %s (would take %v)", description, duration)
	}
}

// ProcessOrders processes orders in the kitchen
func (k *Kitchen) ProcessOrders() {
	for order := range k.OrderQueue {
		// Wait if kitchen is at capacity
		for {
			k.mu.Lock()
			if k.CurrentLoad < k.MaxCapacity {
				k.CurrentLoad++
				k.mu.Unlock()
				break
			}
			k.mu.Unlock()
			log.Printf("[Restaurant #%d] Kitchen at capacity, order #%d waiting...", k.RestaurantID, order.ID)
			simulateDelay(k.Mode, 1*time.Second, "Kitchen capacity wait")
		}
		
		go k.prepareOrder(order)
	}
}

// prepareOrder simulates preparing a single order
func (k *Kitchen) prepareOrder(order *Order) {
	order.Status = OrderPreparing
	log.Printf("[Restaurant #%d] Kitchen: Starting to prepare order #%d for %s", k.RestaurantID, order.ID, order.CustomerName)
	
	// Calculate total prep time for all items
	totalPrepTime := time.Duration(0)
	for _, item := range order.Items {
		totalPrepTime += item.PrepTime
	}
	
	// Simulate cooking time (reduced for demo purposes)
	actualPrepTime := totalPrepTime / time.Duration(k.Chefs)
	if actualPrepTime < 1*time.Second {
		actualPrepTime = 1 * time.Second
	}
	
	simulateDelay(k.Mode, actualPrepTime, fmt.Sprintf("Preparing order #%d for %s", order.ID, order.CustomerName))
	
	order.Status = OrderReady
	order.ReadyAt = time.Now()
	
	k.mu.Lock()
	k.CurrentLoad--
	k.mu.Unlock()
	
	log.Printf("[Restaurant #%d] Kitchen: Order #%d is ready for %s (prep time: %v)", 
		k.RestaurantID, order.ID, order.CustomerName, actualPrepTime)
	
	k.ReadyOrders <- order
}

// DeliveryService handles order delivery
func (r *Restaurant) DeliveryService() {
	for order := range r.Kitchen.ReadyOrders {
		// Simulate delivery time
		deliveryTime := time.Duration(rand.Intn(5)+1) * time.Second
		simulateDelay(r.Mode, deliveryTime, fmt.Sprintf("Delivering order #%d to %s", order.ID, order.CustomerName))
		
		order.Status = OrderDelivered
		order.DeliveredAt = time.Now()
		
		log.Printf("[Restaurant #%d] Delivery: Order #%d delivered to %s (delivery time: %v)", 
			r.ID, order.ID, order.CustomerName, deliveryTime)
	}
}

// GetOrderStatus returns the status of an order
func (r *Restaurant) GetOrderStatus(orderID int) (*Order, bool) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	order, exists := r.Orders[orderID]
	return order, exists
}

// GetRestaurantStats returns current restaurant statistics
func (r *Restaurant) GetRestaurantStats() map[string]interface{} {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	stats := map[string]interface{}{
		"total_orders":     r.OrderCount,
		"kitchen_load":     r.Kitchen.CurrentLoad,
		"kitchen_capacity": r.Kitchen.MaxCapacity,
		"chefs":           r.Kitchen.Chefs,
	}
	
	// Count orders by status
	statusCounts := make(map[OrderStatus]int)
	for _, order := range r.Orders {
		statusCounts[order.Status]++
	}
	stats["orders_by_status"] = statusCounts
	
	return stats
}

// Sample menu items
var menuItems = map[string]MenuItem{
	"burger": {
		Name:     "Classic Burger",
		Price:    12.99,
		PrepTime: 8 * time.Minute,
	},
	"pizza": {
		Name:     "Margherita Pizza",
		Price:    15.99,
		PrepTime: 12 * time.Minute,
	},
	"pasta": {
		Name:     "Spaghetti Carbonara",
		Price:    14.99,
		PrepTime: 10 * time.Minute,
	},
	"salad": {
		Name:     "Caesar Salad",
		Price:    9.99,
		PrepTime: 5 * time.Minute,
	},
	"soup": {
		Name:     "Tomato Soup",
		Price:    6.99,
		PrepTime: 3 * time.Minute,
	},
	"fries": {
		Name:     "French Fries",
		Price:    4.99,
		PrepTime: 4 * time.Minute,
	},
}

func main() {
	// Parse command line arguments
	var restaurantNum int
	var modeStr string
	flag.IntVar(&restaurantNum, "restaurant", 1, "Restaurant number (1-999)")
	flag.StringVar(&modeStr, "mode", "realtime", "Simulation mode: 'realtime' or 'fastforward'")
	flag.Parse()
	
	// Validate restaurant number
	if restaurantNum < 1 || restaurantNum > 999 {
		log.Fatal("Restaurant number must be between 1 and 999")
	}
	
	// Validate and set simulation mode
	var mode SimulationMode
	switch modeStr {
	case "realtime", "rt":
		mode = RealTimeMode
	case "fastforward", "ff":
		mode = FastForwardMode
	default:
		log.Fatal("Mode must be 'realtime' or 'fastforward'")
	}
	
	// Initialize restaurant with dynamic naming
	restaurantName := fmt.Sprintf("Restaurant #%d - The Golden Spoon", restaurantNum)
	restaurant := NewRestaurant(restaurantName, restaurantNum, mode, 3, 10)
	
	// Start kitchen processing
	go restaurant.Kitchen.ProcessOrders()
	
	// Start delivery service
	go restaurant.DeliveryService()
	
	log.Printf("[Restaurant #%d] Restaurant simulation started!", restaurant.ID)
	log.Printf("[Restaurant #%d] Restaurant: %s", restaurant.ID, restaurant.Name)
	log.Printf("[Restaurant #%d] Kitchen: %d chefs, capacity: %d orders", restaurant.ID, restaurant.Kitchen.Chefs, restaurant.Kitchen.MaxCapacity)
	
	// Create sample orders
	sampleOrders := []struct {
		customer string
		items    []string
	}{
		{"Alice Johnson", []string{"burger", "fries"}},
		{"Bob Smith", []string{"pizza", "salad"}},
		{"Carol Davis", []string{"pasta", "soup"}},
		{"David Wilson", []string{"burger", "pizza", "fries"}},
		{"Eva Brown", []string{"salad", "soup"}},
		{"Frank Miller", []string{"pasta", "salad", "fries"}},
		{"Grace Lee", []string{"pizza"}},
		{"Henry Taylor", []string{"burger", "soup"}},
	}
	
	// Create orders with delays
	for i, orderData := range sampleOrders {
		orderDelay := time.Duration(rand.Intn(3)+1) * time.Second
		simulateDelay(restaurant.Mode, orderDelay, fmt.Sprintf("Creating order #%d", i+1))
		
		var items []MenuItem
		for _, itemName := range orderData.items {
			if item, exists := menuItems[itemName]; exists {
				items = append(items, item)
			}
		}
		
		restaurant.CreateOrder(orderData.customer, items)
		
		// Print stats every few orders
		if (i+1)%3 == 0 {
			stats := restaurant.GetRestaurantStats()
			log.Printf("[Restaurant #%d] Stats: %+v", restaurant.ID, stats)
		}
	}
	
	// Wait for all orders to be processed
	log.Printf("[Restaurant #%d] Waiting for all orders to be processed...", restaurant.ID)
	
	// Wait for kitchen to be empty
	for {
		restaurant.Kitchen.mu.RLock()
		load := restaurant.Kitchen.CurrentLoad
		restaurant.Kitchen.mu.RUnlock()
		
		if load == 0 {
			break
		}
		log.Printf("[Restaurant #%d] Kitchen still processing %d orders...", restaurant.ID, load)
		simulateDelay(restaurant.Mode, 2*time.Second, "Waiting for kitchen to finish")
	}
	
	// Wait a bit more for delivery
	simulateDelay(restaurant.Mode, 5*time.Second, "Final delivery wait")
	
	// Print final statistics
	log.Printf("\n[Restaurant #%d] === FINAL RESTAURANT STATISTICS ===", restaurant.ID)
	stats := restaurant.GetRestaurantStats()
	for key, value := range stats {
		log.Printf("[Restaurant #%d] %s: %v", restaurant.ID, key, value)
	}
	
	// Print order summary
	log.Printf("\n[Restaurant #%d] === ORDER SUMMARY ===", restaurant.ID)
	restaurant.mu.RLock()
	for _, order := range restaurant.Orders {
		var duration time.Duration
		if order.DeliveredAt.IsZero() {
			if order.ReadyAt.IsZero() {
				duration = time.Since(order.CreatedAt)
			} else {
				duration = order.ReadyAt.Sub(order.CreatedAt)
			}
		} else {
			duration = order.DeliveredAt.Sub(order.CreatedAt)
		}
		log.Printf("[Restaurant #%d] Order #%d: %s - %s - $%.2f - Total time: %v", 
			restaurant.ID, order.ID, order.CustomerName, order.Status, order.TotalAmount, duration)
	}
	restaurant.mu.RUnlock()
	
	log.Printf("[Restaurant #%d] Restaurant simulation completed!", restaurant.ID)
}
