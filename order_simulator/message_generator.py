"""
Order Message Generator for Restaurant Applications

This module provides functionality to generate order messages in various formats
that can be delivered to standalone restaurant applications.
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import asdict
from .order_models import Order, OrderItem, OrderType, OrderStatus, Customer, MenuItem
from .order_processor import OrderProcessor
from .external_services import ExternalServiceManager
import uuid
import random

class OrderMessageGenerator:
    """Generates order messages in various formats for restaurant applications"""
    
    def __init__(self):
        self.order_processor = OrderProcessor()
        self.external_services = ExternalServiceManager()
        self.message_id_counter = 1
    
    def generate_order_message(self, order: Order, format_type: str = "json", 
                            include_metadata: bool = True) -> Dict[str, Any]:
        """
        Generate an order message in the specified format
        
        Args:
            order: The order to convert to a message
            format_type: Format type (json, xml, csv, pos, kitchen, delivery)
            include_metadata: Whether to include message metadata
        
        Returns:
            Dictionary containing the message data and format information
        """
        base_message = self._create_base_message(order, include_metadata)
        
        if format_type == "json":
            return self._format_as_json(base_message)
        elif format_type == "xml":
            return self._format_as_xml(base_message)
        elif format_type == "csv":
            return self._format_as_csv(base_message)
        elif format_type == "pos":
            return self._format_for_pos_system(base_message)
        elif format_type == "kitchen":
            return self._format_for_kitchen_display(base_message)
        elif format_type == "delivery":
            return self._format_for_delivery_service(base_message)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    def _create_base_message(self, order: Order, include_metadata: bool) -> Dict[str, Any]:
        """Create the base message structure"""
        message = {
            "order_id": order.id,
            "external_order_id": order.external_order_id,
            "order_type": order.order_type.value,
            "status": order.status.value,
            "order_time": order.order_time.isoformat(),
            "customer": {
                "id": order.customer.id,
                "name": order.customer.name,
                "phone": order.customer.phone,
                "email": order.customer.email,
                "loyalty_member": order.customer.loyalty_member
            },
            "items": [
                {
                    "menu_item_id": item.menu_item.id,
                    "name": item.menu_item.name,
                    "description": item.menu_item.description,
                    "category": item.menu_item.category.value,
                    "quantity": item.quantity,
                    "unit_price": item.menu_item.base_price,
                    "total_price": item.price,
                    "special_instructions": item.special_instructions,
                    "customizations": item.customizations,
                    "preparation_time": item.menu_item.preparation_time,
                    "allergens": item.menu_item.allergens
                }
                for item in order.items
            ],
            "totals": {
                "subtotal": sum(item.price for item in order.items),
                "tax_amount": order.tax_amount,
                "tip_amount": order.tip_amount,
                "total_amount": order.total_amount
            },
            "special_instructions": order.special_instructions,
            "estimated_ready_time": order.estimated_ready_time.isoformat() if order.estimated_ready_time else None
        }
        
        if include_metadata:
            message["metadata"] = {
                "message_id": f"MSG_{self.message_id_counter:06d}",
                "generated_at": datetime.now().isoformat(),
                "message_version": "1.0",
                "source": "order_simulator"
            }
            self.message_id_counter += 1
        
        return message
    
    def _format_as_json(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Format message as JSON"""
        return {
            "format": "json",
            "content": json.dumps(message, indent=2),
            "content_type": "application/json",
            "data": message
        }
    
    def _format_as_xml(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Format message as XML"""
        root = ET.Element("OrderMessage")
        
        # Order details
        order_elem = ET.SubElement(root, "Order")
        order_elem.set("id", message["order_id"])
        order_elem.set("type", message["order_type"])
        order_elem.set("status", message["status"])
        
        if message["external_order_id"]:
            order_elem.set("external_id", message["external_order_id"])
        
        # Customer
        customer_elem = ET.SubElement(order_elem, "Customer")
        customer_elem.set("id", message["customer"]["id"])
        customer_elem.set("name", message["customer"]["name"])
        if message["customer"]["phone"]:
            customer_elem.set("phone", message["customer"]["phone"])
        if message["customer"]["email"]:
            customer_elem.set("email", message["customer"]["email"])
        customer_elem.set("loyalty_member", str(message["customer"]["loyalty_member"]))
        
        # Items
        items_elem = ET.SubElement(order_elem, "Items")
        for item in message["items"]:
            item_elem = ET.SubElement(items_elem, "Item")
            item_elem.set("menu_id", item["menu_item_id"])
            item_elem.set("name", item["name"])
            item_elem.set("quantity", str(item["quantity"]))
            item_elem.set("unit_price", str(item["unit_price"]))
            item_elem.set("total_price", str(item["total_price"]))
            item_elem.set("category", item["category"])
            
            if item["special_instructions"]:
                item_elem.set("special_instructions", item["special_instructions"])
        
        # Totals
        totals_elem = ET.SubElement(order_elem, "Totals")
        totals_elem.set("subtotal", str(message["totals"]["subtotal"]))
        totals_elem.set("tax", str(message["totals"]["tax_amount"]))
        totals_elem.set("tip", str(message["totals"]["tip_amount"]))
        totals_elem.set("total", str(message["totals"]["total_amount"]))
        
        # Convert to string
        xml_str = ET.tostring(root, encoding='unicode')
        
        return {
            "format": "xml",
            "content": xml_str,
            "content_type": "application/xml",
            "data": message
        }
    
    def _format_as_csv(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Format message as CSV"""
        csv_lines = []
        
        # Header
        csv_lines.append("OrderID,ExternalID,OrderType,Status,CustomerName,Phone,Email,LoyaltyMember,ItemName,Quantity,UnitPrice,TotalPrice,SpecialInstructions,Subtotal,Tax,Tip,GrandTotal,OrderTime")
        
        # Data rows (one per item)
        for item in message["items"]:
            row = [
                message["order_id"],
                message["external_order_id"] or "",
                message["order_type"],
                message["status"],
                message["customer"]["name"],
                message["customer"]["phone"] or "",
                message["customer"]["email"] or "",
                str(message["customer"]["loyalty_member"]),
                item["name"],
                str(item["quantity"]),
                str(item["unit_price"]),
                str(item["total_price"]),
                item["special_instructions"] or "",
                str(message["totals"]["subtotal"]),
                str(message["totals"]["tax_amount"]),
                str(message["totals"]["tip_amount"]),
                str(message["totals"]["total_amount"]),
                message["order_time"]
            ]
            csv_lines.append(",".join(f'"{field}"' for field in row))
        
        return {
            "format": "csv",
            "content": "\n".join(csv_lines),
            "content_type": "text/csv",
            "data": message
        }
    
    def _format_for_pos_system(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Format message for POS system integration"""
        pos_message = {
            "transaction_id": message["order_id"],
            "transaction_type": "ORDER",
            "timestamp": message["order_time"],
            "customer": {
                "id": message["customer"]["id"],
                "name": message["customer"]["name"],
                "phone": message["customer"]["phone"],
                "loyalty_number": message["customer"]["id"] if message["customer"]["loyalty_member"] else None
            },
            "order_details": {
                "order_type": message["order_type"],
                "items": [
                    {
                        "sku": item["menu_item_id"],
                        "name": item["name"],
                        "qty": item["quantity"],
                        "price": item["unit_price"],
                        "line_total": item["total_price"],
                        "modifiers": item["customizations"],
                        "notes": item["special_instructions"]
                    }
                    for item in message["items"]
                ],
                "subtotal": message["totals"]["subtotal"],
                "tax": message["totals"]["tax_amount"],
                "tip": message["totals"]["tip_amount"],
                "total": message["totals"]["total_amount"]
            },
            "payment_info": {
                "method": "CARD",  # Default for POS
                "status": "PENDING"
            },
            "kitchen_notes": message["special_instructions"]
        }
        
        return {
            "format": "pos",
            "content": json.dumps(pos_message, indent=2),
            "content_type": "application/json",
            "data": pos_message
        }
    
    def _format_for_kitchen_display(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Format message for kitchen display system"""
        kitchen_message = {
            "order_number": message["order_id"][-6:],  # Last 6 chars
            "order_type": message["order_type"].upper(),
            "customer_name": message["customer"]["name"],
            "order_time": message["order_time"],
            "estimated_ready": message["estimated_ready_time"],
            "items": [
                {
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "prep_time": item["preparation_time"],
                    "instructions": item["special_instructions"],
                    "customizations": list(item["customizations"].keys()) if item["customizations"] else [],
                    "allergens": item["allergens"]
                }
                for item in message["items"]
            ],
            "priority": "HIGH" if message["order_type"] in ["drive_thru", "uber_eats"] else "NORMAL",
            "special_requests": message["special_instructions"]
        }
        
        return {
            "format": "kitchen",
            "content": json.dumps(kitchen_message, indent=2),
            "content_type": "application/json",
            "data": kitchen_message
        }
    
    def _format_for_delivery_service(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Format message for delivery service integration"""
        delivery_message = {
            "order_id": message["external_order_id"] or message["order_id"],
            "restaurant_id": "ACSP_001",
            "order_type": message["order_type"],
            "customer": {
                "name": message["customer"]["name"],
                "phone": message["customer"]["phone"],
                "email": message["customer"]["email"]
            },
            "items": [
                {
                    "item_id": item["menu_item_id"],
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": item["unit_price"],
                    "special_instructions": item["special_instructions"]
                }
                for item in message["items"]
            ],
            "order_total": message["totals"]["total_amount"],
            "delivery_fee": 2.99,  # Mock delivery fee
            "service_fee": round(message["totals"]["subtotal"] * 0.12, 2),
            "estimated_delivery_time": 30,  # minutes
            "special_instructions": message["special_instructions"]
        }
        
        return {
            "format": "delivery",
            "content": json.dumps(delivery_message, indent=2),
            "content_type": "application/json",
            "data": delivery_message
        }

class OrderMessageDelivery:
    """Handles delivery of order messages to various destinations"""
    
    def __init__(self):
        self.delivery_methods = {}
    
    def register_delivery_method(self, name: str, method_func):
        """Register a custom delivery method"""
        self.delivery_methods[name] = method_func
    
    def deliver_message(self, message: Dict[str, Any], destination: str, 
                       method: str = "file", **kwargs) -> bool:
        """
        Deliver a message to the specified destination
        
        Args:
            message: The message to deliver
            destination: Where to deliver the message
            method: How to deliver (file, http, mq, console)
            **kwargs: Additional parameters for the delivery method
        """
        try:
            if method == "file":
                return self._deliver_to_file(message, destination, **kwargs)
            elif method == "http":
                return self._deliver_to_http(message, destination, **kwargs)
            elif method == "mq":
                return self._deliver_to_message_queue(message, destination, **kwargs)
            elif method == "console":
                return self._deliver_to_console(message, **kwargs)
            elif method in self.delivery_methods:
                return self.delivery_methods[method](message, destination, **kwargs)
            else:
                raise ValueError(f"Unknown delivery method: {method}")
        except Exception as e:
            print(f"Error delivering message: {e}")
            return False
    
    def _deliver_to_file(self, message: Dict[str, Any], filepath: str, **kwargs) -> bool:
        """Deliver message to a file"""
        try:
            with open(filepath, 'w') as f:
                f.write(message["content"])
            print(f"✅ Message delivered to file: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error writing to file {filepath}: {e}")
            return False
    
    def _deliver_to_http(self, message: Dict[str, Any], url: str, **kwargs) -> bool:
        """Deliver message via HTTP POST"""
        try:
            import requests
            headers = {
                'Content-Type': message["content_type"],
                'User-Agent': 'OrderSimulator/1.0'
            }
            response = requests.post(url, data=message["content"], headers=headers)
            if response.status_code == 200:
                print(f"✅ Message delivered to HTTP endpoint: {url}")
                return True
            else:
                print(f"❌ HTTP delivery failed: {response.status_code}")
                return False
        except ImportError:
            print("❌ requests library not available for HTTP delivery")
            return False
        except Exception as e:
            print(f"❌ HTTP delivery error: {e}")
            return False
    
    def _deliver_to_message_queue(self, message: Dict[str, Any], queue_name: str, **kwargs) -> bool:
        """Deliver message to message queue (placeholder)"""
        print(f"📤 Message queued for delivery: {queue_name}")
        print(f"   Format: {message['format']}")
        print(f"   Order ID: {message['data']['order_id']}")
        return True
    
    def _deliver_to_console(self, message: Dict[str, Any], **kwargs) -> bool:
        """Deliver message to console output"""
        print(f"\n{'='*50}")
        print(f"ORDER MESSAGE - {message['format'].upper()}")
        print(f"{'='*50}")
        print(message["content"])
        print(f"{'='*50}\n")
        return True
