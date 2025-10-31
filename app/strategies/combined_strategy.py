"""
Combined template strategy implementation
"""
from typing import List, Dict, Any
from .base_template_strategy import BaseTemplateStrategy


class CombinedTemplateStrategy(BaseTemplateStrategy):
    """
    Strategy for processing combined (mother + infant) medical record requests.

    This strategy handles template selection, record type configuration,
    and data validation for requests that include both maternal and infant records.
    """

    def get_template_path(self) -> str:
        """
        Get the absolute path to the combined template file

        Returns:
            Absolute path to combined_template.docx
        """
        return self._get_absolute_template_path()

    def get_record_types(self) -> List[str]:
        """
        Get Datavant record types for combined mother + infant records

        Returns:
            List of record types combining both maternal and infant records
        """
        return self.config.record_types

    def configure_datavant_builder(self, builder: Any) -> None:
        """
        Configure Datavant request builder with combined parameters

        Args:
            builder: DatavantRequestBuilder instance
        """
        # Set combined record types from configuration
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
        Validate that data contains required fields for combined template

        Requires both maternal AND infant fields to be present

        Args:
            data: RedcapResponseSecond or RedcapResponseFirst object

        Returns:
            True if all required fields (both mother and infant) are present and valid
        """
        required_fields = self.get_required_fields()

        missing_fields = []
        for field in required_fields:
            value = getattr(data, field, None)
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)

        if missing_fields:
            print(f"⚠️ Combined template validation failed. Missing fields: {missing_fields}")
            return False

        print(f"✅ Combined template validation passed")
        return True

    def customize_record_needs(self, item: Any) -> None:
        """
        Customize record needs checkboxes for combined (mother + infant) records

        Sets ALL medical record needs checkboxes to "1" (checked) for both
        maternal and infant records since this is a comprehensive request.

        Args:
            item: RedcapResponseSecond object to customize
        """
        # Set ALL maternal record needs
        item.mr_rec_needs___1 = "1"
        item.mr_rec_needs___2 = "1"
        item.mr_rec_needs___3 = "1"
        item.mr_rec_needs___4 = "1"
        item.mr_rec_needs___6 = "1"   # Note: skip 5 as per original logic
        item.mr_rec_needs___7 = "1"
        item.mr_rec_needs___8 = "1"
        item.mr_rec_needs___9 = "1"
        item.mr_rec_needs___10 = "1"
        item.mr_rec_needs___11 = "1"
        item.mr_rec_needs___12 = "1"
        item.mr_rec_needs___13 = "1"
        item.mr_rec_needs___14 = "1"
        item.mr_rec_needs___15 = "1"

        # Set ALL infant record needs
        item.mr_rec_needs_inf___1 = "1"
        item.mr_rec_needs_inf___2 = "1"
        item.mr_rec_needs_inf___3 = "1"
        item.mr_rec_needs_inf___4 = "1"
        item.mr_rec_needs_inf___5 = "1"
        item.mr_rec_needs_inf___6 = "1"
        item.mr_rec_needs_inf___7 = "1"
        item.mr_rec_needs_inf___8 = "1"
        item.mr_rec_needs_inf___9 = "1"
        item.mr_rec_needs_inf___10 = "1"
        item.mr_rec_needs_inf___11 = "1"
        item.mr_rec_needs_inf___12 = "1"
        item.mr_rec_needs_inf___13 = "1"

    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get field mappings specific to combined template

        Includes both mother and infant field mappings

        Returns:
            Dictionary mapping RedCap fields to template placeholders
        """
        return {
            # Mother fields
            'bc_momnamefirst': 'mother_first_name',
            'bc_momnamelast': 'mother_last_name',
            'bc_mom_dob': 'mother_dob',
            'bc_momssn': 'mother_ssn',
            'bc_momnamemaidenlast': 'mother_maiden_name',

            # Infant fields
            'bc_childnamefirst': 'infant_first_name',
            'bc_childnamelast': 'infant_last_name',
            'dob_inf': 'infant_dob',
            'bc_childssn': 'infant_ssn',

            # Common fields
            'hos_name': 'hospital_name',

            # Add more mappings as needed
        }
