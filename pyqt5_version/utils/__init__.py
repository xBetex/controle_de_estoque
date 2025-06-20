"""
Utilities module for PyQt5 Inventory Management System
"""

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtGui import QPixmap, QIcon

def create_directory(path: str) -> bool:
    """
    Create a directory if it doesn't exist
    
    Args:
        path: Directory path to create
        
    Returns:
        True if created successfully or already exists, False otherwise
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False

def load_json_data(filename: str, default: Any = None) -> Any:
    """
    Load data from a JSON file
    
    Args:
        filename: JSON file name
        default: Default value if file doesn't exist
        
    Returns:
        Loaded data or default value
    """
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default if default is not None else []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return default if default is not None else []

def save_json_data(data: Any, filename: str) -> bool:
    """
    Save data to a JSON file
    
    Args:
        data: Data to save
        filename: JSON file name
        
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        # Create parent directory if it doesn't exist
        parent_dir = os.path.dirname(filename)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def validate_required_fields(data: Dict, required_fields: List[str]) -> Optional[str]:
    """
    Validate that all required fields are filled
    
    Args:
        data: Dictionary with data
        required_fields: List of required fields
        
    Returns:
        Name of first unfilled field or None if all are filled
    """
    for field in required_fields:
        if not data.get(field, "").strip():
            return field
    return None

def validate_numeric_fields(data: Dict, numeric_fields: Dict[str, type]) -> Optional[str]:
    """
    Validate that numeric fields have valid values
    
    Args:
        data: Dictionary with data
        numeric_fields: Dictionary with field->type mapping
        
    Returns:
        Name of first invalid field or None if all are valid
    """
    for field, field_type in numeric_fields.items():
        if field in data and data[field]:
            try:
                field_type(data[field])
            except (ValueError, TypeError):
                return field
    return None

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate Brazilian phone format
    
    Args:
        phone: Phone string to validate
        
    Returns:
        True if valid phone format, False otherwise
    """
    pattern = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    return bool(re.match(pattern, phone))

def format_currency(value: float, currency: str = "BRL") -> str:
    """
    Format a monetary value
    
    Args:
        value: Value to format
        currency: Currency (default BRL)
        
    Returns:
        Formatted value as string
    """
    if currency == "BRL":
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,.2f}"

def format_date(date_str: str, format_from: str = "%Y-%m-%dT%H:%M:%S.%f", 
                format_to: str = "%d/%m/%Y %H:%M") -> str:
    """
    Format a date
    
    Args:
        date_str: Original date string
        format_from: Original format
        format_to: Desired format
        
    Returns:
        Formatted date
    """
    try:
        # Try different ISO formats
        for fmt in ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime(format_to)
            except ValueError:
                continue
        return date_str
    except Exception:
        return date_str

def format_phone(phone: str) -> str:
    """
    Format a phone number to Brazilian standard
    
    Args:
        phone: Phone number string
        
    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format according to Brazilian standard
    if len(digits) == 11:  # Cell phone with area code
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) == 10:  # Landline with area code
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    else:
        return phone  # Return original if doesn't match expected length

def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to maximum length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def generate_id(existing_ids: List[int]) -> int:
    """
    Generate a new unique ID
    
    Args:
        existing_ids: List of existing IDs
        
    Returns:
        New unique ID
    """
    return max(existing_ids, default=0) + 1

def safe_float(value: Union[str, float, int], default: float = 0.0) -> float:
    """
    Safely convert value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    try:
        if isinstance(value, str):
            # Handle Brazilian decimal format
            value = value.replace(".", "").replace(",", ".")
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value: Union[str, int, float], default: int = 0) -> int:
    """
    Safely convert value to int
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value or default
    """
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

class MessageBox:
    """PyQt5 message box utilities"""
    
    @staticmethod
    def show_info(parent, title: str, message: str):
        """Show information message"""
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
    
    @staticmethod
    def show_success(parent, title: str, message: str):
        """Show success message"""
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
    
    @staticmethod
    def show_warning(parent, title: str, message: str):
        """Show warning message"""
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.exec_()
    
    @staticmethod
    def show_error(parent, title: str, message: str):
        """Show error message"""
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()
    
    @staticmethod
    def ask_confirmation(parent, title: str, message: str) -> bool:
        """Ask for user confirmation"""
        reply = QMessageBox.question(
            parent,
            title,
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes
    
    @staticmethod
    def ask_save_discard_cancel(parent, title: str, message: str) -> str:
        """Ask user to save, discard or cancel"""
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Question)
        
        save_btn = msg_box.addButton("Salvar", QMessageBox.AcceptRole)
        discard_btn = msg_box.addButton("Descartar", QMessageBox.DestructiveRole)
        cancel_btn = msg_box.addButton("Cancelar", QMessageBox.RejectRole)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == save_btn:
            return "save"
        elif msg_box.clickedButton() == discard_btn:
            return "discard"
        else:
            return "cancel"

class FileDialog:
    """PyQt5 file dialog utilities"""
    
    @staticmethod
    def get_save_filename(parent, title: str, default_name: str = "", 
                         file_filter: str = "All Files (*)") -> Optional[str]:
        """Get filename for saving"""
        filename, _ = QFileDialog.getSaveFileName(
            parent, title, default_name, file_filter
        )
        return filename if filename else None
    
    @staticmethod
    def get_open_filename(parent, title: str, 
                         file_filter: str = "All Files (*)") -> Optional[str]:
        """Get filename for opening"""
        filename, _ = QFileDialog.getOpenFileName(
            parent, title, "", file_filter
        )
        return filename if filename else None
    
    @staticmethod
    def get_directory(parent, title: str) -> Optional[str]:
        """Get directory path"""
        directory = QFileDialog.getExistingDirectory(parent, title)
        return directory if directory else None

def get_app_data_dir() -> str:
    """Get application data directory"""
    app_data = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not app_data:
        app_data = os.path.expanduser("~/.inventory_manager")
    
    create_directory(app_data)
    return app_data

def backup_file(source_path: str, backup_dir: str) -> bool:
    """Create a backup of a file"""
    try:
        if not os.path.exists(source_path):
            return False
        
        create_directory(backup_dir)
        
        filename = os.path.basename(source_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{timestamp}_{filename}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        import shutil
        shutil.copy2(source_path, backup_path)
        return True
    except Exception as e:
        print(f"Error backing up file {source_path}: {e}")
        return False

def get_file_size(filepath: str) -> str:
    """Get human-readable file size"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "Unknown"

def debounce(wait_time):
    """
    Decorator that will debounce a function so that it is called after wait_time seconds
    If it is called multiple times, will wait for the last call to be debounced and run only this one.
    """
    def decorator(function):
        def debounced(*args, **kwargs):
            def call_function():
                debounced._timer = None
                return function(*args, **kwargs)
            
            if hasattr(debounced, '_timer') and debounced._timer is not None:
                debounced._timer.cancel()
            
            from threading import Timer
            debounced._timer = Timer(wait_time, call_function)
            debounced._timer.start()
        
        return debounced
    return decorator 