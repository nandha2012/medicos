"""
Strategy pattern implementation for template processing
"""
from .base_template_strategy import BaseTemplateStrategy
from .infant_strategy import InfantTemplateStrategy
from .mother_strategy import MotherTemplateStrategy
from .combined_strategy import CombinedTemplateStrategy
from .template_factory import TemplateFactory

__all__ = [
    'BaseTemplateStrategy',
    'InfantTemplateStrategy',
    'MotherTemplateStrategy',
    'CombinedTemplateStrategy',
    'TemplateFactory'
]
