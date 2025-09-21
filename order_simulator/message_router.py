"""
Message Router for Restaurant Applications

This module provides routing capabilities for order messages to different
restaurant applications and systems.
"""

import json
import os
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import threading
from queue import Queue, Empty

class MessageRoute:
    """Represents a message route to a specific destination"""
    
    def __init__(self, name: str, destination: str, method: str = "file", 
                 format_filter: List[str] = None, order_type_filter: List[str] = None,
                 enabled: bool = True, **kwargs):
        self.name = name
        self.destination = destination
        self.method = method
        self.format_filter = format_filter or []
        self.order_type_filter = order_type_filter or []
        self.enabled = enabled
        self.kwargs = kwargs
        self.message_count = 0
        self.last_delivery = None
        self.errors = 0
    
    def should_route(self, message: Dict[str, Any]) -> bool:
        """Check if this route should handle the given message"""
        if not self.enabled:
            return False
        
        # Check format filter
        if self.format_filter and message.get("format") not in self.format_filter:
            return False
        
        # Check order type filter
        if self.order_type_filter:
            order_type = message.get("data", {}).get("order_type")
            if order_type not in self.order_type_filter:
                return False
        
        return True
    
    def deliver(self, message: Dict[str, Any], delivery_handler) -> bool:
        """Deliver message using the configured method"""
        try:
            success = delivery_handler.deliver_message(
                message, self.destination, self.method, **self.kwargs
            )
            
            if success:
                self.message_count += 1
                self.last_delivery = datetime.now()
            else:
                self.errors += 1
            
            return success
        except Exception as e:
            self.errors += 1
            print(f"❌ Error delivering to {self.name}: {e}")
            return False

class MessageRouter:
    """Routes order messages to different restaurant applications"""
    
    def __init__(self):
        self.routes: Dict[str, MessageRoute] = {}
        self.message_queue = Queue()
        self.delivery_handler = None
        self.running = False
        self.worker_thread = None
        
    def register_delivery_handler(self, handler):
        """Register a message delivery handler"""
        self.delivery_handler = handler
    
    def add_route(self, route: MessageRoute):
        """Add a message route"""
        self.routes[route.name] = route
        print(f"✅ Added route: {route.name} -> {route.destination} ({route.method})")
    
    def remove_route(self, route_name: str):
        """Remove a message route"""
        if route_name in self.routes:
            del self.routes[route_name]
            print(f"✅ Removed route: {route_name}")
    
    def route_message(self, message: Dict[str, Any]) -> List[str]:
        """Route a message to all applicable routes"""
        if not self.delivery_handler:
            print("❌ No delivery handler registered")
            return []
        
        routed_to = []
        
        for route_name, route in self.routes.items():
            if route.should_route(message):
                if self.running:
                    # Add to queue for async processing
                    self.message_queue.put((route, message))
                else:
                    # Process synchronously
                    if route.deliver(message, self.delivery_handler):
                        routed_to.append(route_name)
        
        return routed_to
    
    def start_async_processing(self):
        """Start async message processing"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_message_queue)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        print("🔄 Started async message processing")
    
    def stop_async_processing(self):
        """Stop async message processing"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        print("🛑 Stopped async message processing")
    
    def _process_message_queue(self):
        """Process messages from the queue"""
        while self.running:
            try:
                route, message = self.message_queue.get(timeout=1)
                route.deliver(message, self.delivery_handler)
                self.message_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"❌ Error processing message: {e}")
    
    def get_route_statistics(self) -> Dict[str, Any]:
        """Get statistics for all routes"""
        stats = {}
        for name, route in self.routes.items():
            stats[name] = {
                "destination": route.destination,
                "method": route.method,
                "enabled": route.enabled,
                "message_count": route.message_count,
                "errors": route.errors,
                "last_delivery": route.last_delivery.isoformat() if route.last_delivery else None,
                "success_rate": (route.message_count / (route.message_count + route.errors)) * 100 if (route.message_count + route.errors) > 0 else 0
            }
        return stats

class RestaurantApplicationConfig:
    """Configuration for different restaurant applications"""
    
    @staticmethod
    def get_pos_system_config() -> Dict[str, Any]:
        """Configuration for POS system integration"""
        return {
            "name": "pos_system",
            "destination": "pos_orders",
            "method": "file",
            "format_filter": ["pos", "json"],
            "order_type_filter": ["drive_thru", "dine_in"],
            "enabled": True,
            "file_extension": "json",
            "directory": "pos_orders"
        }
    
    @staticmethod
    def get_kitchen_display_config() -> Dict[str, Any]:
        """Configuration for kitchen display system"""
        return {
            "name": "kitchen_display",
            "destination": "kitchen_orders",
            "method": "file",
            "format_filter": ["kitchen", "json"],
            "order_type_filter": [],  # All order types
            "enabled": True,
            "file_extension": "json",
            "directory": "kitchen_orders"
        }
    
    @staticmethod
    def get_delivery_service_config() -> Dict[str, Any]:
        """Configuration for delivery service integration"""
        return {
            "name": "delivery_service",
            "destination": "delivery_orders",
            "method": "file",
            "format_filter": ["delivery", "json"],
            "order_type_filter": ["uber_eats", "grubhub", "doordash"],
            "enabled": True,
            "file_extension": "json",
            "directory": "delivery_orders"
        }
    
    @staticmethod
    def get_inventory_system_config() -> Dict[str, Any]:
        """Configuration for inventory management system"""
        return {
            "name": "inventory_system",
            "destination": "inventory_updates",
            "method": "file",
            "format_filter": ["csv", "json"],
            "order_type_filter": [],  # All order types
            "enabled": True,
            "file_extension": "csv",
            "directory": "inventory_updates"
        }
    
    @staticmethod
    def get_analytics_system_config() -> Dict[str, Any]:
        """Configuration for analytics system"""
        return {
            "name": "analytics_system",
            "destination": "analytics_data",
            "method": "file",
            "format_filter": ["json"],
            "order_type_filter": [],  # All order types
            "enabled": True,
            "file_extension": "json",
            "directory": "analytics_data"
        }

class MessageRouterBuilder:
    """Builder class for creating message routers with common configurations"""
    
    def __init__(self):
        self.router = MessageRouter()
    
    def add_pos_system_route(self, **overrides) -> 'MessageRouterBuilder':
        """Add POS system route"""
        config = RestaurantApplicationConfig.get_pos_system_config()
        config.update(overrides)
        route = MessageRoute(**config)
        self.router.add_route(route)
        return self
    
    def add_kitchen_display_route(self, **overrides) -> 'MessageRouterBuilder':
        """Add kitchen display route"""
        config = RestaurantApplicationConfig.get_kitchen_display_config()
        config.update(overrides)
        route = MessageRoute(**config)
        self.router.add_route(route)
        return self
    
    def add_delivery_service_route(self, **overrides) -> 'MessageRouterBuilder':
        """Add delivery service route"""
        config = RestaurantApplicationConfig.get_delivery_service_config()
        config.update(overrides)
        route = MessageRoute(**config)
        self.router.add_route(route)
        return self
    
    def add_inventory_system_route(self, **overrides) -> 'MessageRouterBuilder':
        """Add inventory system route"""
        config = RestaurantApplicationConfig.get_inventory_system_config()
        config.update(overrides)
        route = MessageRoute(**config)
        self.router.add_route(route)
        return self
    
    def add_analytics_system_route(self, **overrides) -> 'MessageRouterBuilder':
        """Add analytics system route"""
        config = RestaurantApplicationConfig.get_analytics_system_config()
        config.update(overrides)
        route = MessageRoute(**config)
        self.router.add_route(route)
        return self
    
    def add_custom_route(self, name: str, destination: str, method: str = "file",
                        format_filter: List[str] = None, order_type_filter: List[str] = None,
                        **kwargs) -> 'MessageRouterBuilder':
        """Add a custom route"""
        route = MessageRoute(
            name=name,
            destination=destination,
            method=method,
            format_filter=format_filter,
            order_type_filter=order_type_filter,
            **kwargs
        )
        self.router.add_route(route)
        return self
    
    def build(self) -> MessageRouter:
        """Build and return the configured router"""
        return self.router

def create_standard_restaurant_router() -> MessageRouter:
    """Create a standard restaurant router with common routes"""
    return (MessageRouterBuilder()
            .add_pos_system_route()
            .add_kitchen_display_route()
            .add_delivery_service_route()
            .add_inventory_system_route()
            .add_analytics_system_route()
            .build())
