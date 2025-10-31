"""
Template Factory for creating template strategy instances
"""
from typing import Dict, Type, Optional
from config.template_registry import TemplateRegistry
from models.template_config import TemplateConfig
from .base_template_strategy import BaseTemplateStrategy
from .infant_strategy import InfantTemplateStrategy
from .mother_strategy import MotherTemplateStrategy
from .combined_strategy import CombinedTemplateStrategy


class TemplateFactory:
    """
    Factory class for creating template strategy instances.

    This class implements the Factory Pattern, providing a centralized way
    to instantiate the appropriate template strategy based on template ID
    or mr_req_for value.

    The factory maintains a mapping between template IDs and strategy classes,
    making it easy to add new templates without modifying core logic.
    """

    def __init__(self, registry: Optional[TemplateRegistry] = None):
        """
        Initialize the template factory

        Args:
            registry: Optional TemplateRegistry instance. If None, creates a new one.
        """
        self.registry = registry if registry else TemplateRegistry()

        # Map template IDs to strategy classes
        self._strategy_map: Dict[str, Type[BaseTemplateStrategy]] = {
            "1": MotherTemplateStrategy,
            "2": InfantTemplateStrategy,
            "3": CombinedTemplateStrategy,
        }

        print(f"🏭 TemplateFactory initialized with {len(self._strategy_map)} strategy types")

    def register_strategy_class(self, template_id: str, strategy_class: Type[BaseTemplateStrategy]) -> None:
        """
        Register a custom strategy class for a template ID

        This allows dynamic registration of new template strategies without
        modifying the factory code.

        Args:
            template_id: Template ID to associate with the strategy
            strategy_class: Strategy class (must inherit from BaseTemplateStrategy)

        Raises:
            ValueError: If strategy_class is not a subclass of BaseTemplateStrategy
        """
        if not issubclass(strategy_class, BaseTemplateStrategy):
            raise ValueError(f"Strategy class must inherit from BaseTemplateStrategy")

        if template_id in self._strategy_map:
            print(f"⚠️ Warning: Overwriting existing strategy for template ID: {template_id}")

        self._strategy_map[template_id] = strategy_class
        print(f"✅ Registered strategy class {strategy_class.__name__} for template ID: {template_id}")

    def create_strategy(self, template_id: str) -> Optional[BaseTemplateStrategy]:
        """
        Create a template strategy instance for the given template ID

        Args:
            template_id: Template ID (e.g., "1", "2", "3")

        Returns:
            Instance of appropriate template strategy, or None if not found

        Raises:
            ValueError: If template configuration is invalid
        """
        # Get template configuration from registry
        config = self.registry.get_config(template_id)

        if config is None:
            print(f"❌ No configuration found for template ID: {template_id}")
            return None

        # Get strategy class for this template
        strategy_class = self._strategy_map.get(template_id)

        if strategy_class is None:
            print(f"❌ No strategy class registered for template ID: {template_id}")
            print(f"   Available strategies: {list(self._strategy_map.keys())}")
            return None

        try:
            # Instantiate strategy with configuration
            strategy = strategy_class(config)
            print(f"✅ Created {strategy_class.__name__} for template: {config.name}")
            return strategy

        except Exception as e:
            print(f"❌ Error creating strategy for template ID {template_id}: {e}")
            raise

    def get_strategy_for_request(self, mr_req_for: str) -> Optional[BaseTemplateStrategy]:
        """
        Get template strategy based on mr_req_for value (for backward compatibility)

        This method provides compatibility with the existing RedCap field naming.

        Args:
            mr_req_for: Request type value from RedCap ("1" for mother, "2" for infant, "3" for combined)

        Returns:
            Instance of appropriate template strategy, or None if not found
        """
        # mr_req_for directly maps to template ID in our system
        return self.create_strategy(mr_req_for)

    def list_available_strategies(self) -> Dict[str, str]:
        """
        Get list of available template strategies

        Returns:
            Dictionary mapping template IDs to strategy class names
        """
        return {
            template_id: strategy_class.__name__
            for template_id, strategy_class in self._strategy_map.items()
        }

    def supports_template(self, template_id: str) -> bool:
        """
        Check if factory supports creating a strategy for the given template ID

        Args:
            template_id: Template ID to check

        Returns:
            True if template is supported, False otherwise
        """
        return (
            template_id in self._strategy_map and
            self.registry.template_exists(template_id)
        )

    def reload_registry(self) -> None:
        """Reload the template registry from YAML configuration"""
        self.registry.reload()
        print("🔄 Template registry reloaded")

    def __repr__(self) -> str:
        """Detailed representation"""
        return f"TemplateFactory(strategies={list(self._strategy_map.keys())})"

    def __str__(self) -> str:
        """Human-readable string representation"""
        strategies = ', '.join([
            f"{tid}={cls.__name__}"
            for tid, cls in self._strategy_map.items()
        ])
        return f"TemplateFactory with strategies: {strategies}"


# Global factory instance for convenience
_global_factory: Optional[TemplateFactory] = None


def get_global_factory() -> TemplateFactory:
    """
    Get or create the global template factory instance

    Returns:
        Global TemplateFactory instance
    """
    global _global_factory

    if _global_factory is None:
        _global_factory = TemplateFactory()

    return _global_factory


def reset_global_factory() -> None:
    """Reset the global factory (useful for testing)"""
    global _global_factory
    _global_factory = None
