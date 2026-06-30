import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from core.connector import OdooConnector

class OdooIntrospection:
    """Handles discovery and caching of Odoo model schemas."""

    def __init__(self, connector: OdooConnector):
        self.connector = connector
        self.cache_dir = Path(__file__).parent.parent / ".cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.schema_file = self.cache_dir / "schema.json"
        
        self.schema = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        """Loads schema from local cache if it exists."""
        if self.schema_file.exists():
            try:
                with open(self.schema_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {}

    def _save_cache(self):
        """Saves current schema to local cache."""
        with open(self.schema_file, "w") as f:
            json.dump(self.schema, f, indent=2)

    def get_all_models(self) -> List[Dict[str, Any]]:
        """Fetches a list of all models in the Odoo instance."""
        # Using ir.model to get all models
        models = self.connector.execute_kw(
            "ir.model", 
            "search_read", 
            [[]], 
            {"fields": ["model", "name"]}
        )
        return models

    def get_model_schema(self, model_name: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Fetches the fields (schema) for a specific model."""
        if not force_refresh and model_name in self.schema:
            return self.schema[model_name]

        # Use fields_get to fetch the schema
        fields = self.connector.execute_kw(
            model_name,
            "fields_get",
            [],
            {"attributes": ["string", "help", "type", "required", "readonly", "relation"]}
        )
        
        self.schema[model_name] = fields
        self._save_cache()
        
        return fields

    def search_models(self, query: str) -> List[Dict[str, Any]]:
        """Searches for models by name or technical model name."""
        return self.connector.execute_kw(
            "ir.model",
            "search_read",
            [[
                "|", 
                ("model", "ilike", query), 
                ("name", "ilike", query)
            ]],
            {"fields": ["model", "name"]}
        )
