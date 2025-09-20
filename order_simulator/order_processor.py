from .order_models import Order, OrderItem, OrderType, OrderStatus, Customer, MenuItem
from .menu_data import MENU_DICT, get_available_items
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import random

class OrderProcessor:
    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.order_queue: List[str] = []  # Order IDs in processing queue
        self.completed_orders: List[str] = []
        
    def create_customer(self, name: str, phone: Optional[str] = None, 
                       email: Optional[str] = None, loyalty_member: bool = False) -> Customer:
        """Create a new customer"""
        return Customer(
            id=str(uuid.uuid4()),
            name=name,
            phone=phone,
            email=email,
            loyalty_member=loyalty_member
        )
    
    def create_order(self, order_type: OrderType, customer: Customer, 
                    items: List[OrderItem], special_instructions: str = "") -> Order:
        """Create a new order"""
        order = Order(
            id=str(uuid.uuid4()),
            order_type=order_type,
            customer=customer,
            items=items,
            order_time=datetime.now(),
            special_instructions=special_instructions
        )
        
        # Add external order ID for delivery services
        if order_type in [OrderType.UBER_EATS, OrderType.GRUBHUB, OrderType.DOORDASH]:
            order.external_order_id = self._generate_external_order_id(order_type)
        
        self.orders[order.id] = order
        self.order_queue.append(order.id)
        return order
    
    def add_item_to_order(self, order_id: str, menu_item_id: str, 
                         quantity: int = 1, customizations: Dict[str, Any] = None,
                         special_instructions: str = "") -> bool:
        """Add an item to an existing order"""
        if order_id not in self.orders:
            return False
        
        if menu_item_id not in MENU_DICT:
            return False
        
        order = self.orders[order_id]
        if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            return False  # Can't modify order once it's being prepared
        
        menu_item = MENU_DICT[menu_item_id]
        order_item = OrderItem(
            menu_item=menu_item,
            quantity=quantity,
            special_instructions=special_instructions,
            customizations=customizations or {}
        )
        
        order.items.append(order_item)
        order.calculate_totals()
        return True
    
    def remove_item_from_order(self, order_id: str, item_index: int) -> bool:
        """Remove an item from an order by index"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            return False
        
        if 0 <= item_index < len(order.items):
            del order.items[item_index]
            order.calculate_totals()
            return True
        return False
    
    def confirm_order(self, order_id: str) -> bool:
        """Confirm an order and move it to preparation queue"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        if order.status != OrderStatus.PENDING:
            return False
        
        if not order.items:  # Empty order
            return False
        
        order.update_status(OrderStatus.CONFIRMED)
        return True
    
    def start_preparation(self, order_id: str) -> bool:
        """Start preparing an order"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        if order.status != OrderStatus.CONFIRMED:
            return False
        
        order.update_status(OrderStatus.PREPARING)
        return True
    
    def complete_order(self, order_id: str) -> bool:
        """Mark an order as ready for pickup/delivery"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        if order.status != OrderStatus.PREPARING:
            return False
        
        order.update_status(OrderStatus.READY)
        return True
    
    def finalize_order(self, order_id: str) -> bool:
        """Mark an order as completed"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        if order.status not in [OrderStatus.READY, OrderStatus.COMPLETED]:
            return False
        
        order.update_status(OrderStatus.COMPLETED)
        if order_id in self.order_queue:
            self.order_queue.remove(order_id)
        self.completed_orders.append(order_id)
        return True
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            return False
        
        order.update_status(OrderStatus.CANCELLED)
        if order_id in self.order_queue:
            self.order_queue.remove(order_id)
        return True
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get an order by ID"""
        return self.orders.get(order_id)
    
    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Get all orders with a specific status"""
        return [order for order in self.orders.values() if order.status == status]
    
    def get_orders_by_type(self, order_type: OrderType) -> List[Order]:
        """Get all orders of a specific type"""
        return [order for order in self.orders.values() if order.order_type == order_type]
    
    def get_queue_position(self, order_id: str) -> int:
        """Get the position of an order in the preparation queue"""
        try:
            return self.order_queue.index(order_id) + 1
        except ValueError:
            return -1
    
    def get_estimated_wait_time(self, order_id: str) -> int:
        """Get estimated wait time in minutes for an order"""
        if order_id not in self.orders:
            return -1
        
        order = self.orders[order_id]
        if order.status == OrderStatus.READY:
            return 0
        
        queue_position = self.get_queue_position(order_id)
        if queue_position == -1:
            return order.get_estimated_prep_time()
        
        # Estimate based on queue position and average prep time
        avg_prep_time = 5  # minutes
        return (queue_position - 1) * avg_prep_time + order.get_estimated_prep_time()
    
    def _generate_external_order_id(self, order_type: OrderType) -> str:
        """Generate a mock external order ID for delivery services"""
        prefixes = {
            OrderType.UBER_EATS: "UE",
            OrderType.GRUBHUB: "GH",
            OrderType.DOORDASH: "DD"
        }
        prefix = prefixes.get(order_type, "EXT")
        return f"{prefix}{random.randint(100000, 999999)}"
    
    def get_order_statistics(self) -> Dict[str, Any]:
        """Get order processing statistics"""
        total_orders = len(self.orders)
        completed_orders = len(self.completed_orders)
        cancelled_orders = len([o for o in self.orders.values() if o.status == OrderStatus.CANCELLED])
        
        # Calculate average order value
        completed_order_values = [
            order.total_amount for order in self.orders.values() 
            if order.status == OrderStatus.COMPLETED
        ]
        avg_order_value = sum(completed_order_values) / len(completed_order_values) if completed_order_values else 0
        
        # Calculate orders by type
        orders_by_type = {}
        for order_type in OrderType:
            orders_by_type[order_type.value] = len(self.get_orders_by_type(order_type))
        
        return {
            "total_orders": total_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
            "pending_orders": len(self.get_orders_by_status(OrderStatus.PENDING)),
            "preparing_orders": len(self.get_orders_by_status(OrderStatus.PREPARING)),
            "ready_orders": len(self.get_orders_by_status(OrderStatus.READY)),
            "average_order_value": round(avg_order_value, 2),
            "orders_by_type": orders_by_type
        }
