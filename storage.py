import json
import os
from datetime import datetime
from typing import Dict, List, Any

class LocalStorage:
    """Simple file-based storage for conversion history and stats"""
    
    def __init__(self):
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Storage files
        self.conversions_file = os.path.join(self.data_dir, 'conversions.json')
        self.stats_file = os.path.join(self.data_dir, 'stats.json')
        
        # Initialize files if they don't exist
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage files with empty data"""
        if not os.path.exists(self.conversions_file):
            self._save_json(self.conversions_file, [])
        
        if not os.path.exists(self.stats_file):
            self._save_json(self.stats_file, {
                'total_conversions': 0,
                'successful_conversions': 0,
                'failed_conversions': 0,
                'popular_formats': {},
                'last_updated': datetime.now().isoformat()
            })
    
    def _load_json(self, filepath: str) -> Any:
        """Load JSON data from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [] if 'conversions' in filepath else {}
    
    def _save_json(self, filepath: str, data: Any):
        """Save JSON data to file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
    
    def add_conversion(self, conversion_data: Dict[str, Any]):
        """Add a new conversion record"""
        conversions = self._load_json(self.conversions_file)
        
        # Add timestamp if not provided
        conversion_data['created_at'] = conversion_data.get('created_at', datetime.now().isoformat())
        conversion_data['id'] = len(conversions) + 1
        
        conversions.append(conversion_data)
        
        # Keep only last 100 conversions to prevent file from getting too large
        if len(conversions) > 100:
            conversions = conversions[-100:]
        
        self._save_json(self.conversions_file, conversions)
        self._update_stats(conversion_data)
    
    def get_recent_conversions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversion records"""
        conversions = self._load_json(self.conversions_file)
        return conversions[-limit:] if conversions else []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get conversion statistics"""
        stats = self._load_json(self.stats_file)
        conversions = self._load_json(self.conversions_file)
        
        # Update stats with current data
        stats['total_conversions'] = len(conversions)
        stats['successful_conversions'] = len([c for c in conversions if c.get('status') == 'completed'])
        stats['failed_conversions'] = len([c for c in conversions if c.get('status') == 'failed'])
        
        # Calculate success rate
        if stats['total_conversions'] > 0:
            stats['success_rate'] = round((stats['successful_conversions'] / stats['total_conversions']) * 100, 2)
        else:
            stats['success_rate'] = 0
        
        return stats
    
    def _update_stats(self, conversion_data: Dict[str, Any]):
        """Update statistics with new conversion data"""
        stats = self._load_json(self.stats_file)
        
        # Update popular formats
        file_ext = conversion_data.get('file_extension', 'unknown').lower()
        if 'popular_formats' not in stats:
            stats['popular_formats'] = {}
        
        stats['popular_formats'][file_ext] = stats['popular_formats'].get(file_ext, 0) + 1
        stats['last_updated'] = datetime.now().isoformat()
        
        self._save_json(self.stats_file, stats)

# Global storage instance
storage = LocalStorage()