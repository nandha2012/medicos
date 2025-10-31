"""
Infant template strategy implementation
"""
from typing import List, Dict, Any
from .base_template_strategy import BaseTemplateStrategy


class InfantTemplateStrategy(BaseTemplateStrategy):
    """
    Strategy for processing infant medical record requests.

    This strategy handles template selection, record type configuration,
    and data validation specific to infant records.
    """

    def get_template_path(self) -> str:
        """
        Get the absolute path to the infant template file

        Returns:
            Absolute path to infant_template.docx
        """
        return self._get_absolute_template_path()

    def get_record_types(self) -> List[str]:
        """
        Get Datavant record types specific to infant records

        Returns:
            List of record types for infant medical records
        """
        return self.config.record_types

    def configure_datavant_builder(self, builder: Any) -> None:
        """
        Configure Datavant request builder with infant-specific parameters

        Args:
            builder: DatavantRequestBuilder instance
        """
        # Set record types from configuration
        builder.set_record_types(self.get_record_types())

        # Set additional Datavant parameters from config
        params = self.get_datavant_params()

        if 'certification_required' in params:
            # Builder will handle this in the build() method
            pass

        if 'business_type' in params and 'api_code' in params:
            # These will be set through the builder's reason configuration
            pass

    def validate_data(self, data: Any) -> bool:
        """
        Validate that data contains required fields for infant template

        Args:
            data: RedcapResponseSecond or RedcapResponseFirst object

        Returns:
            True if all required fields are present and valid
        """
        required_fields = self.get_required_fields()

        missing_fields = []
        for field in required_fields:
            value = getattr(data, field, None)
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)

        if missing_fields:
            print(f"⚠️ Infant template validation failed. Missing fields: {missing_fields}")
            return False

        print(f"✅ Infant template validation passed")
        return True

    def customize_record_needs(self, item: Any) -> None:
        """
        Customize record needs checkboxes for infant records

        Sets all infant-specific medical record needs checkboxes to "1" (checked)

        Args:
            item: RedcapResponseSecond object to customize
        """
        # Set infant-specific record needs
        item.mr_rec_needs_inf___1 = "1"   # Infant record need 1
        item.mr_rec_needs_inf___2 = "1"   # Infant record need 2
        item.mr_rec_needs_inf___3 = "1"   # Infant record need 3
        item.mr_rec_needs_inf___4 = "1"   # Infant record need 4
        item.mr_rec_needs_inf___5 = "1"   # Infant record need 5
        item.mr_rec_needs_inf___6 = "1"   # Infant record need 6
        item.mr_rec_needs_inf___7 = "1"   # Infant record need 7
        item.mr_rec_needs_inf___8 = "1"   # Infant record need 8
        item.mr_rec_needs_inf___9 = "1"   # Infant record need 9
        item.mr_rec_needs_inf___10 = "1"  # Infant record need 10
        item.mr_rec_needs_inf___11 = "1"  # Infant record need 11
        item.mr_rec_needs_inf___12 = "1"  # Infant record need 12
        item.mr_rec_needs_inf___13 = "1"  # Infant record need 13

        # Also set some general maternal records that are relevant for infant delivery
        item.mr_rec_needs___1 = "1"   # Maternal record need 1
        item.mr_rec_needs___2 = "1"   # Maternal record need 2
        item.mr_rec_needs___3 = "1"   # Maternal record need 3
        item.mr_rec_needs___4 = "1"   # Maternal record need 4
        item.mr_rec_needs___6 = "1"   # Maternal record need 6
        item.mr_rec_needs___7 = "1"   # Maternal record need 7
        item.mr_rec_needs___8 = "1"   # Maternal record need 8
        item.mr_rec_needs___9 = "1"   # Maternal record need 9
        item.mr_rec_needs___10 = "1"  # Maternal record need 10
        item.mr_rec_needs___11 = "1"  # Maternal record need 11
        item.mr_rec_needs___12 = "1"  # Maternal record need 12
        item.mr_rec_needs___13 = "1"  # Maternal record need 13
        item.mr_rec_needs___14 = "1"  # Maternal record need 14
        item.mr_rec_needs___15 = "1"  # Maternal record need 15

    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get field mappings specific to infant template

        Returns:
            Dictionary mapping RedCap fields to template placeholders
        """
        return {
            'bc_childnamefirst': 'infant_first_name',
            'bc_childnamelast': 'infant_last_name',
            'dob_inf': 'infant_dob',
            'bc_childssn': 'infant_ssn',
            'hos_name': 'hospital_name',
            # Add more mappings as needed
        }
