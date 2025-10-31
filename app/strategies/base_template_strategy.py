"""
Base template strategy abstract class
"""
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from models.template_config import TemplateConfig


class BaseTemplateStrategy(ABC):
    """
    Abstract base class for template processing strategies.

    Each template type (infant, mother, combined, etc.) implements this interface
    to provide template-specific behavior while sharing common workflow.

    This implements the Strategy Pattern, allowing different template processing
    algorithms to be interchangeable.
    """

    def __init__(self, config: TemplateConfig):
        """
        Initialize strategy with template configuration

        Args:
            config: TemplateConfig object containing template metadata
        """
        self.config = config
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate that the configuration is valid for this strategy"""
        if not self.config:
            raise ValueError("Template configuration cannot be None")

        if not self.config.template_path:
            raise ValueError(f"Template path is required for {self.config.name}")

        if not self.config.record_types:
            print(f"⚠️ Warning: No record types defined for {self.config.name}")

    @abstractmethod
    def get_template_path(self) -> str:
        """
        Get the absolute path to the template file

        Returns:
            Absolute path to the template DOCX file

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        pass

    @abstractmethod
    def get_record_types(self) -> List[str]:
        """
        Get the list of Datavant record types for this template

        Returns:
            List of record type names for Datavant API
        """
        pass

    @abstractmethod
    def configure_datavant_builder(self, builder: Any) -> None:
        """
        Configure the Datavant request builder with template-specific parameters

        Args:
            builder: DatavantRequestBuilder instance to configure
        """
        pass

    @abstractmethod
    def validate_data(self, data: Any) -> bool:
        """
        Validate that the data contains required fields for this template

        Args:
            data: RedcapResponseSecond or RedcapResponseFirst object

        Returns:
            True if data is valid, False otherwise
        """
        pass

    def customize_record_needs(self, item: Any) -> None:
        """
        Customize record needs checkboxes for this template type.

        This method can be overridden by concrete strategies to set template-specific
        checkbox values for mr_rec_needs and mr_rec_needs_inf fields.

        Args:
            item: RedcapResponseSecond object to customize

        Note:
            Default implementation does nothing. Override in concrete strategies
            if custom checkbox logic is needed.
        """
        pass

    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get field mappings for template data population

        Returns:
            Dictionary mapping RedCap field names to template placeholder names

        Note:
            Default implementation returns empty dict. Override if custom
            field mappings are needed.
        """
        return {}

    def get_validation_rules(self) -> Dict[str, Any]:
        """
        Get validation rules from configuration

        Returns:
            Dictionary containing validation rules
        """
        return self.config.validation_rules

    def get_required_fields(self) -> List[str]:
        """
        Get list of required fields for this template

        Returns:
            List of required field names
        """
        return self.config.get_required_fields()

    def get_optional_fields(self) -> List[str]:
        """
        Get list of optional fields for this template

        Returns:
            List of optional field names
        """
        return self.config.get_optional_fields()

    def get_datavant_params(self) -> Dict[str, Any]:
        """
        Get Datavant-specific parameters from configuration

        Returns:
            Dictionary of Datavant API parameters
        """
        return self.config.datavant_params

    def _get_absolute_template_path(self) -> str:
        """
        Helper method to convert relative template path to absolute

        Returns:
            Absolute path to template file

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        # Get project root (assuming we're in app/strategies/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))

        # Construct absolute path
        abs_path = os.path.join(project_root, self.config.template_path)

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Template file not found: {abs_path}")

        return abs_path

    def __str__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}(template={self.config.name})"

    def __repr__(self) -> str:
        """Detailed representation"""
        return (f"{self.__class__.__name__}(config={self.config.name}, "
                f"id={self.config.id}, record_types={len(self.config.record_types)})")
