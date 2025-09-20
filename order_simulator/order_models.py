from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class OrderType(Enum):
    DRIVE_THRU = "drive_thru"
    DINE_IN = "dine_in"
    UBER_EATS = "uber_eats"
    GRUBHUB = "grubhub"
    DOORDASH = "doordash"

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ItemCategory(Enum):
    SANDWICHES = "sandwiches"
    CHICKEN_STRIPS = "chicken_strips"
    SALADS = "salads"
    SIDES = "sides"
    BEVERAGES = "beverages"
    DESSERTS = "desserts"
    BREAKFAST = "breakfast"
    KIDS_MEALS = "kids_meals"

@dataclass
class MenuItem:
    id: str
    name: str
    description: str
    category: ItemCategory
    base_price: float
    calories: int
    allergens: List[str]
    is_available: bool = True
    preparation_time: int = 5  # minutes
    customizations: List[str] = None
    
    def __post_init__(self):
        if self.customizations is None:
            self.customizations = []

@dataclass
class OrderItem:
    menu_item: MenuItem
    quantity: int
    special_instructions: str = ""
    customizations: Dict[str, Any] = None
    price: float = 0.0
    
    def __post_init__(self):
        if self.customizations is None:
            self.customizations = {}
        if self.price == 0.0:
            self.price = self.menu_item.base_price * self.quantity

@dataclass
class Customer:
    id: str
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    loyalty_member: bool = False
    preferred_payment: str = "card"

@dataclass
class Order:
    id: str
    order_type: OrderType
    customer: Customer
    items: List[OrderItem]
    order_time: datetime
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = 0.0
    tax_amount: float = 0.0
    tip_amount: float = 0.0
    special_instructions: str = ""
    estimated_ready_time: Optional[datetime] = None
    external_order_id: Optional[str] = None  # For delivery services
    
    def __post_init__(self):
        self.calculate_totals()
    
    def calculate_totals(self):
        """Calculate order totals including tax and tip"""
        subtotal = sum(item.price for item in self.items)
        self.tax_amount = subtotal * 0.08  # 8% tax
        self.total_amount = subtotal + self.tax_amount + self.tip_amount
    
    def add_tip(self, tip_amount: float):
        """Add tip to the order"""
        self.tip_amount = tip_amount
        self.calculate_totals()
    
    def get_estimated_prep_time(self) -> int:
        """Calculate estimated preparation time in minutes"""
        return max(item.menu_item.preparation_time for item in self.items) + 2  # +2 for order processing
    
    def update_status(self, new_status: OrderStatus):
        """Update order status"""
        self.status = new_status
        if new_status == OrderStatus.PREPARING:
            self.estimated_ready_time = datetime.now().replace(
                minute=datetime.now().minute + self.get_estimated_prep_time()
            )
