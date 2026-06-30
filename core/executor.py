from typing import List, Dict, Any, Optional
from core.connector import OdooConnector

class OdooExecutor:
    """Provides high-level abstraction for the 7 universal Odoo CRUD operations."""
    
    def __init__(self, connector: OdooConnector):
        self.connector = connector

    def search(self, model: str, domain: List[Any], offset: int = 0, limit: int = 0, order: str = None) -> List[int]:
        """Returns record IDs matching the domain."""
        kwargs = {}
        if offset: kwargs['offset'] = offset
        if limit: kwargs['limit'] = limit
        if order: kwargs['order'] = order
        
        return self.connector.execute_kw(model, 'search', [domain], kwargs)

    def read(self, model: str, ids: List[int], fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Reads specific fields for given record IDs."""
        kwargs = {}
        if fields:
            kwargs['fields'] = fields
            
        return self.connector.execute_kw(model, 'read', [ids], kwargs)

    def search_read(self, model: str, domain: List[Any], fields: Optional[List[str]] = None, 
                    offset: int = 0, limit: int = 0, order: str = None) -> List[Dict[str, Any]]:
        """Combines search and read for efficiency."""
        kwargs = {}
        if fields: kwargs['fields'] = fields
        if offset: kwargs['offset'] = offset
        if limit: kwargs['limit'] = limit
        if order: kwargs['order'] = order
        
        return self.connector.execute_kw(model, 'search_read', [domain], kwargs)

    def create(self, model: str, vals: Dict[str, Any]) -> int:
        """Creates a new record with the given values."""
        return self.connector.execute_kw(model, 'create', [vals])

    def write(self, model: str, ids: List[int], vals: Dict[str, Any]) -> bool:
        """Updates existing records with new values."""
        return self.connector.execute_kw(model, 'write', [ids, vals])

    def unlink(self, model: str, ids: List[int]) -> bool:
        """Deletes records."""
        return self.connector.execute_kw(model, 'unlink', [ids])

    def execute(self, model: str, method: str, *args, **kwargs) -> Any:
        """Executes a custom method on the model."""
        return self.connector.execute_kw(model, method, list(args), kwargs)
