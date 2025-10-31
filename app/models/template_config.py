"""
Template configuration model for medical records system
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class TemplateConfig:
    """
    Configuration model for medical record templates

    Attributes:
        id: Unique identifier for the template (matches mr_req_for value)
        name: Human-readable name of the template
        description: Detailed description of the template's purpose
        template_path: Relative path to the template file
        active: Whether the template is currently active
        record_types: List of Datavant record types for this template
        datavant_params: Additional Datavant API parameters
        validation_rules: Rules for validating data before processing
    """
    id: str
    name: str
    description: str
    template_path: str
    active: bool = True
    record_types: List[str] = field(default_factory=list)
    datavant_params: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.id:
            raise ValueError("Template ID cannot be empty")
        if not self.template_path:
            raise ValueError(f"Template path is required for template '{self.name}'")
        if not self.record_types:
            print(f"⚠️ Warning: Template '{self.name}' has no record types defined")

    def get_required_fields(self) -> List[str]:
        """Get list of required fields for validation"""
        return self.validation_rules.get('required_fields', [])

    def get_optional_fields(self) -> List[str]:
        """Get list of optional fields"""
        return self.validation_rules.get('optional_fields', [])

    def get_datavant_param(self, key: str, default: Any = None) -> Any:
        """Safely get a Datavant parameter with default fallback"""
        return self.datavant_params.get(key, default)

    def is_active(self) -> bool:
        """Check if template is currently active"""
        return self.active

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template_path': self.template_path,
            'active': self.active,
            'record_types': self.record_types,
            'datavant_params': self.datavant_params,
            'validation_rules': self.validation_rules
        }

    def __str__(self) -> str:
        """String representation"""
        return f"TemplateConfig(id={self.id}, name={self.name}, active={self.active})"

    def __repr__(self) -> str:
        """Detailed representation"""
        return (f"TemplateConfig(id='{self.id}', name='{self.name}', "
                f"template_path='{self.template_path}', active={self.active}, "
                f"record_types={len(self.record_types)} types)")
