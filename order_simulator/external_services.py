from .order_models import Order, OrderType, OrderStatus, Customer, OrderItem
from typing import Dict, List, Optional, Any
from datetime import datetime
import random
import json

class ExternalServiceInterface:
    """Base class for external delivery service integrations"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.orders: Dict[str, Dict] = {}
    
    def create_order(self, order: Order) -> Dict[str, Any]:
        """Create an order in the external service"""
        raise NotImplementedError
    
    def get_order_status(self, external_order_id: str) -> str:
        """Get the status of an order from the external service"""
        raise NotImplementedError
    
    def update_order_status(self, external_order_id: str, status: str) -> bool:
        """Update the status of an order in the external service"""
        raise NotImplementedError
    
    def cancel_order(self, external_order_id: str) -> bool:
        """Cancel an order in the external service"""
        raise NotImplementedError

class UberEatsService(ExternalServiceInterface):
    """Mock Uber Eats service integration"""
    
    def __init__(self):
        super().__init__("Uber Eats")
        self.api_key = "mock_uber_eats_key"
        self.base_url = "https://api.uber.com/v1"
    
    def create_order(self, order: Order) -> Dict[str, Any]:
        """Create an order in Uber Eats"""
        external_order_id = f"UE{random.randint(100000, 999999)}"
        
        # Mock API response
        response = {
            "order_id": external_order_id,
            "status": "pending",
            "estimated_delivery_time": self._calculate_delivery_time(order),
            "delivery_fee": self._calculate_delivery_fee(order),
            "service_fee": self._calculate_service_fee(order),
            "total_amount": order.total_amount,
            "created_at": datetime.now().isoformat(),
            "restaurant_id": "acsp_123",
            "customer_info": {
                "name": order.customer.name,
                "phone": order.customer.phone,
                "email": order.customer.email
            }
        }
        
        self.orders[external_order_id] = response
        return response
    
    def get_order_status(self, external_order_id: str) -> str:
        """Get order status from Uber Eats"""
        if external_order_id in self.orders:
            return self.orders[external_order_id]["status"]
        return "not_found"
    
    def update_order_status(self, external_order_id: str, status: str) -> bool:
        """Update order status in Uber Eats"""
        if external_order_id in self.orders:
            self.orders[external_order_id]["status"] = status
            self.orders[external_order_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False
    
    def cancel_order(self, external_order_id: str) -> bool:
        """Cancel order in Uber Eats"""
        if external_order_id in self.orders:
            self.orders[external_order_id]["status"] = "cancelled"
            self.orders[external_order_id]["cancelled_at"] = datetime.now().isoformat()
            return True
        return False
    
    def _calculate_delivery_time(self, order: Order) -> int:
        """Calculate estimated delivery time in minutes"""
        base_time = 25  # Base delivery time
        distance_factor = random.randint(5, 15)  # Mock distance factor
        return base_time + distance_factor
    
    def _calculate_delivery_fee(self, order: Order) -> float:
        """Calculate delivery fee"""
        base_fee = 2.99
        if order.total_amount > 15:
            base_fee = 1.99  # Reduced fee for larger orders
        return base_fee
    
    def _calculate_service_fee(self, order: Order) -> float:
        """Calculate service fee"""
        return round(order.total_amount * 0.15, 2)  # 15% service fee

class GrubhubService(ExternalServiceInterface):
    """Mock Grubhub service integration"""
    
    def __init__(self):
        super().__init__("Grubhub")
        self.api_key = "mock_grubhub_key"
        self.base_url = "https://api.grubhub.com/v1"
    
    def create_order(self, order: Order) -> Dict[str, Any]:
        """Create an order in Grubhub"""
        external_order_id = f"GH{random.randint(100000, 999999)}"
        
        # Mock API response
        response = {
            "order_id": external_order_id,
            "status": "pending",
            "estimated_delivery_time": self._calculate_delivery_time(order),
            "delivery_fee": self._calculate_delivery_fee(order),
            "service_fee": self._calculate_service_fee(order),
            "total_amount": order.total_amount,
            "created_at": datetime.now().isoformat(),
            "restaurant_id": "acsp_456",
            "customer_info": {
                "name": order.customer.name,
                "phone": order.customer.phone,
                "email": order.customer.email
            }
        }
        
        self.orders[external_order_id] = response
        return response
    
    def get_order_status(self, external_order_id: str) -> str:
        """Get order status from Grubhub"""
        if external_order_id in self.orders:
            return self.orders[external_order_id]["status"]
        return "not_found"
    
    def update_order_status(self, external_order_id: str, status: str) -> bool:
        """Update order status in Grubhub"""
        if external_order_id in self.orders:
            self.orders[external_order_id]["status"] = status
            self.orders[external_order_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False
    
    def cancel_order(self, external_order_id: str) -> bool:
        """Cancel order in Grubhub"""
        if external_order_id in self.orders:
            self.orders[external_order_id]["status"] = "cancelled"
            self.orders[external_order_id]["cancelled_at"] = datetime.now().isoformat()
            return True
        return False
    
    def _calculate_delivery_time(self, order: Order) -> int:
        """Calculate estimated delivery time in minutes"""
        base_time = 30  # Base delivery time
        distance_factor = random.randint(5, 20)  # Mock distance factor
        return base_time + distance_factor
    
    def _calculate_delivery_fee(self, order: Order) -> float:
        """Calculate delivery fee"""
        base_fee = 3.99
        if order.total_amount > 20:
            base_fee = 2.99  # Reduced fee for larger orders
        return base_fee
    
    def _calculate_service_fee(self, order: Order) -> float:
        """Calculate service fee"""
        return round(order.total_amount * 0.12, 2)  # 12% service fee

class DoorDashService(ExternalServiceInterface):
    """Mock DoorDash service integration"""
    
    def __init__(self):
        super().__init__("DoorDash")
        self.api_key = "mock_doordash_key"
        self.base_url = "https://api.doordash.com/v1"
    
    def create_order(self, order: Order) -> Dict[str, Any]:
        """Create an order in DoorDash"""
        external_order_id = f"DD{random.randint(100000, 999999)}"
        
        # Mock API response
        response = {
            "order_id": external_order_id,
            "status": "pending",
            "estimated_delivery_time": self._calculate_delivery_time(order),
            "delivery_fee": self._calculate_delivery_fee(order),
            "service_fee": self._calculate_service_fee(order),
            "total_amount": order.total_amount,
            "created_at": datetime.now().isoformat(),
            "restaurant_id": "acsp_789",
            "customer_info": {
                "name": order.customer.name,
                "phone": order.customer.phone,
                "email": order.customer.email
            }
        }
        
        self.orders[external_order_id] = response
        return response
    
    def get_order_status(self, external_order_id: str) -> str:
        """Get order status from DoorDash"""
        if external_order_id in self.orders:
            return self.orders[external_order_id]["status"]
        return "not_found"
    
    def update_order_status(self, external_order_id: str, status: str) -> bool:
        """Update order status in DoorDash"""
        if external_order_id in self.orders:
            self.orders[external_order_id]["status"] = status
            self.orders[external_order_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False
    
    def cancel_order(self, external_order_id: str) -> bool:
        """Cancel order in DoorDash"""
        if external_order_id in self.orders:
            self.orders[external_order_id]["status"] = "cancelled"
            self.orders[external_order_id]["cancelled_at"] = datetime.now().isoformat()
            return True
        return False
    
    def _calculate_delivery_time(self, order: Order) -> int:
        """Calculate estimated delivery time in minutes"""
        base_time = 28  # Base delivery time
        distance_factor = random.randint(5, 18)  # Mock distance factor
        return base_time + distance_factor
    
    def _calculate_delivery_fee(self, order: Order) -> float:
        """Calculate delivery fee"""
        base_fee = 2.99
        if order.total_amount > 12:
            base_fee = 1.99  # Reduced fee for larger orders
        return base_fee
    
    def _calculate_service_fee(self, order: Order) -> float:
        """Calculate service fee"""
        return round(order.total_amount * 0.10, 2)  # 10% service fee

class ExternalServiceManager:
    """Manages all external delivery services"""
    
    def __init__(self):
        self.services = {
            OrderType.UBER_EATS: UberEatsService(),
            OrderType.GRUBHUB: GrubhubService(),
            OrderType.DOORDASH: DoorDashService()
        }
    
    def create_order(self, order: Order) -> Dict[str, Any]:
        """Create an order in the appropriate external service"""
        if order.order_type not in self.services:
            raise ValueError(f"No service available for order type: {order.order_type}")
        
        service = self.services[order.order_type]
        return service.create_order(order)
    
    def get_order_status(self, order_type: OrderType, external_order_id: str) -> str:
        """Get order status from the appropriate service"""
        if order_type not in self.services:
            return "service_not_available"
        
        service = self.services[order_type]
        return service.get_order_status(external_order_id)
    
    def update_order_status(self, order_type: OrderType, external_order_id: str, status: str) -> bool:
        """Update order status in the appropriate service"""
        if order_type not in self.services:
            return False
        
        service = self.services[order_type]
        return service.update_order_status(external_order_id, status)
    
    def cancel_order(self, order_type: OrderType, external_order_id: str) -> bool:
        """Cancel order in the appropriate service"""
        if order_type not in self.services:
            return False
        
        service = self.services[order_type]
        return service.cancel_order(external_order_id)
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """Get statistics for all external services"""
        stats = {}
        for order_type, service in self.services.items():
            stats[order_type.value] = {
                "total_orders": len(service.orders),
                "active_orders": len([o for o in service.orders.values() if o["status"] != "cancelled"]),
                "cancelled_orders": len([o for o in service.orders.values() if o["status"] == "cancelled"])
            }
        return stats
