"""
Template Registry for managing template configurations
"""
import os
import yaml
from typing import Dict, List, Optional
from models.template_config import TemplateConfig


class TemplateRegistry:
    """
    Central registry for managing medical record template configurations.

    This class loads template configurations from YAML and provides methods
    to retrieve templates by ID or mr_req_for value.

    Attributes:
        _templates: Dictionary mapping template IDs to TemplateConfig objects
        _config_path: Path to the YAML configuration file
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the template registry

        Args:
            config_path: Optional path to YAML config file. If None, uses default.
        """
        self._templates: Dict[str, TemplateConfig] = {}

        if config_path is None:
            # Default path: app/config/templates.yaml
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, 'templates.yaml')

        self._config_path = config_path
        self._load_from_yaml()

    def _load_from_yaml(self) -> None:
        """Load template configurations from YAML file"""
        try:
            if not os.path.exists(self._config_path):
                raise FileNotFoundError(f"Template config file not found: {self._config_path}")

            with open(self._config_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

            if not data or 'templates' not in data:
                raise ValueError("Invalid template configuration: missing 'templates' key")

            templates_data = data['templates']

            for template_key, template_dict in templates_data.items():
                try:
                    config = TemplateConfig(
                        id=template_dict.get('id', template_key),
                        name=template_dict.get('name', template_key),
                        description=template_dict.get('description', ''),
                        template_path=template_dict.get('template_path', ''),
                        active=template_dict.get('active', True),
                        record_types=template_dict.get('record_types', []),
                        datavant_params=template_dict.get('datavant_params', {}),
                        validation_rules=template_dict.get('validation_rules', {})
                    )
                    self._templates[config.id] = config
                    print(f"✅ Loaded template: {config.name} (ID: {config.id})")

                except Exception as e:
                    print(f"❌ Error loading template '{template_key}': {e}")
                    continue

            print(f"📋 Template Registry initialized with {len(self._templates)} templates")

        except Exception as e:
            print(f"❌ Error loading template configuration from {self._config_path}: {e}")
            raise

    def get_config(self, template_id: str) -> Optional[TemplateConfig]:
        """
        Get template configuration by ID

        Args:
            template_id: Template ID to retrieve

        Returns:
            TemplateConfig object or None if not found
        """
        config = self._templates.get(template_id)

        if config is None:
            print(f"⚠️ Template not found for ID: {template_id}")
            return None

        if not config.is_active():
            print(f"⚠️ Template '{config.name}' (ID: {template_id}) is not active")
            return None

        return config

    def get_config_by_request_for(self, mr_req_for: str) -> Optional[TemplateConfig]:
        """
        Get template configuration by mr_req_for value (for backward compatibility)

        Args:
            mr_req_for: Request type value from RedCap ("1", "2", "3", etc.)

        Returns:
            TemplateConfig object or None if not found
        """
        return self.get_config(mr_req_for)

    def register_template(self, config: TemplateConfig) -> None:
        """
        Programmatically register a new template configuration

        Args:
            config: TemplateConfig object to register
        """
        if config.id in self._templates:
            print(f"⚠️ Warning: Overwriting existing template with ID: {config.id}")

        self._templates[config.id] = config
        print(f"✅ Registered template: {config.name} (ID: {config.id})")

    def list_active_templates(self) -> List[TemplateConfig]:
        """
        Get list of all active template configurations

        Returns:
            List of active TemplateConfig objects
        """
        return [config for config in self._templates.values() if config.is_active()]

    def list_all_templates(self) -> List[TemplateConfig]:
        """
        Get list of all template configurations (including inactive)

        Returns:
            List of all TemplateConfig objects
        """
        return list(self._templates.values())

    def template_exists(self, template_id: str) -> bool:
        """
        Check if a template exists and is active

        Args:
            template_id: Template ID to check

        Returns:
            True if template exists and is active, False otherwise
        """
        config = self._templates.get(template_id)
        return config is not None and config.is_active()

    def get_template_path(self, template_id: str) -> Optional[str]:
        """
        Get template file path for given ID

        Args:
            template_id: Template ID

        Returns:
            Template file path or None if not found
        """
        config = self.get_config(template_id)
        return config.template_path if config else None

    def get_record_types(self, template_id: str) -> List[str]:
        """
        Get record types for given template ID

        Args:
            template_id: Template ID

        Returns:
            List of record type names
        """
        config = self.get_config(template_id)
        return config.record_types if config else []

    def reload(self) -> None:
        """Reload configurations from YAML file"""
        self._templates.clear()
        self._load_from_yaml()
        print("🔄 Template registry reloaded")

    def __repr__(self) -> str:
        """String representation of the registry"""
        active_count = len(self.list_active_templates())
        total_count = len(self._templates)
        return f"TemplateRegistry({active_count}/{total_count} active templates)"

    def __str__(self) -> str:
        """Human-readable string representation"""
        templates = ', '.join([f"{c.name} ({c.id})" for c in self.list_active_templates()])
        return f"TemplateRegistry with templates: {templates}"


# Singleton instance for global access
_global_registry: Optional[TemplateRegistry] = None


def get_global_registry() -> TemplateRegistry:
    """
    Get or create the global template registry instance

    Returns:
        Global TemplateRegistry instance
    """
    global _global_registry

    if _global_registry is None:
        _global_registry = TemplateRegistry()

    return _global_registry


def reset_global_registry() -> None:
    """Reset the global registry (useful for testing)"""
    global _global_registry
    _global_registry = None
