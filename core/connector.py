import json
import os
import xmlrpc.client
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

class OdooConnector:
    """Handles XML-RPC connections to an Odoo instance."""

    def __init__(self, profile_name: Optional[str] = None):
        self.config = self._load_profile(profile_name)
        self.url = self.config["url"]
        self.db = self.config["db"]
        self.username = self.config["username"]
        self.password = self.config["password"]
        
        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        
        # Authenticate and get user ID
        self.uid = self.authenticate()

    def _load_profile(self, profile_name: Optional[str] = None) -> Dict[str, Any]:
        """Loads connection settings from profiles.json."""
        project_root = Path(__file__).parent.parent
        profile_path = project_root / "profiles.json"
        
        if not profile_path.exists():
            raise FileNotFoundError(f"Profiles file not found at {profile_path}")
            
        with open(profile_path, "r") as f:
            data = json.load(f)
            
        target_profile = profile_name or data.get("default")
        if not target_profile or target_profile not in data.get("profiles", {}):
            raise ValueError(f"Profile '{target_profile}' not found in profiles.json")
            
        return data["profiles"][target_profile]

    def authenticate(self) -> int:
        """Authenticates with Odoo and returns the user ID."""
        try:
            uid = self.common.authenticate(self.db, self.username, self.password, {})
            if not uid:
                raise ValueError("Authentication failed. Check your database, username, and password.")
            return uid
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Odoo: {str(e)}")

    def execute_kw(self, model: str, method: str, args: list = None, kwargs: dict = None) -> Any:
        """Executes a method on an Odoo model via XML-RPC."""
        args = args or []
        kwargs = kwargs or {}
        
        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password,
                model, method, args, kwargs
            )
        except xmlrpc.client.Fault as e:
            raise RuntimeError(f"Odoo XML-RPC Error ({model}.{method}): {e.faultString}")
        except Exception as e:
            raise RuntimeError(f"Execution Error ({model}.{method}): {str(e)}")
