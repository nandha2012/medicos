# Medicos - Medical Records Request System

A comprehensive medical records request management system integrating with Datavant API for automated medical record retrieval.

## Overview

Medicos is a FastAPI-based application that automates the process of requesting and managing medical records through the Datavant API. It supports multiple template types (mother, infant, combined) and provides a flexible, configuration-driven architecture for handling various medical record request scenarios.

## Key Features

- **Multiple Template Support**: Handles mother, infant, and combined medical record requests
- **Datavant API Integration**: Automated medical record retrieval through Datavant's platform
- **Configuration-Driven**: YAML-based template configuration for easy customization
- **Design Patterns**: Built with Strategy, Factory, Builder, Facade, and Registry patterns
- **PDF Generation**: Automatic document generation from templates
- **Email Integration**: SendGrid integration for automated notifications
- **REDCap Integration**: Direct integration with REDCap for data collection
- **Dashboard Interface**: Web-based dashboard for monitoring and managing medical record requests

## Architecture

The system is built using modern design patterns:

- **Strategy Pattern**: Different template types as interchangeable strategies
- **Factory Pattern**: Template factory creates appropriate strategy instances
- **Builder Pattern**: Fluent interface for complex Datavant request construction
- **Facade Pattern**: Unified interface for workflow orchestration
- **Registry Pattern**: YAML-based configuration management

See [docs/current/ARCHITECTURE.md](docs/current/ARCHITECTURE.md) for detailed architecture documentation.

## Project Structure

```
medicos/
├── app/
│   ├── builders/           # Builder pattern implementations
│   ├── config/             # Configuration files and registry
│   ├── facades/            # Facade pattern implementations
│   ├── models/             # Pydantic models for data validation
│   ├── services/           # Business logic and API integrations
│   ├── strategies/         # Strategy pattern implementations
│   └── main.py             # FastAPI application entry point
├── assets/
│   └── templates/          # DOCX template files
├── docs/
│   ├── current/            # Current documentation
│   ├── dashboard/          # Dashboard documentation
│   └── archive/            # Archived documentation
├── tests/
│   └── archive/            # Archived test files
└── requirements.txt        # Python dependencies
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd medicos
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Running Tests

```bash
# Test facility integration
python test_facility_integration.py

# Test email functionality
python test_email_with_fax.py
```

## Configuration

### Templates

Templates are configured in `app/config/templates.yaml`. Each template defines:

- Template path
- Record types to request
- Datavant API parameters
- Validation rules

Example:
```yaml
templates:
  mother:
    id: "1"
    name: "Mother Template"
    template_path: "assets/templates/mother_template.docx"
    record_types:
      - "Laboratory and Hematology"
      - "Labor and Delivery Records"
    datavant_params:
      certification_required: false
      business_type: "ATTY"
```

### Environment Variables

Key environment variables (see `.env.example`):

- `DATAVANT_API_KEY`: Datavant API authentication key
- `DATAVANT_BASE_URL`: Datavant API base URL
- `SENDGRID_API_KEY`: SendGrid API key for email
- `REDCAP_API_URL`: REDCap API endpoint
- `REDCAP_API_TOKEN`: REDCap API token

## API Endpoints

- `POST /api/medical-records/request`: Create new medical record request
- `GET /api/medical-records/status/{request_id}`: Check request status
- `GET /health`: Health check endpoint

See API documentation at `http://localhost:8000/docs` when running.

## Dashboard

The Medicos dashboard provides a web-based interface for:

- Monitoring medical record request status
- Viewing request history and analytics
- Managing facility configurations
- Tracking API integration health

For complete dashboard setup and usage instructions, see:
- [Dashboard Guide](docs/dashboard/DASHBOARD_GUIDE.md)
- [Dashboard Setup](docs/dashboard/DASHBOARD_SETUP.md)

## Adding New Templates

To add a new template:

1. Add template configuration to `app/config/templates.yaml`
2. Create strategy class in `app/strategies/`
3. Register strategy in `app/strategies/template_factory.py`

See [docs/current/REFACTORING_SUMMARY.md](docs/current/REFACTORING_SUMMARY.md) for detailed instructions.

## Recent Updates

### Fax Removal (2025-01-31)
- Removed fax field from Datavant facility model
- Maintained backward compatibility with existing data
- See [docs/current/FAX_REMOVAL_NOTES.md](docs/current/FAX_REMOVAL_NOTES.md)

### Architecture Refactoring (2025-01-31)
- Implemented design patterns for maintainability
- Reduced template addition process from 7+ files to 3 steps
- Added comprehensive configuration system
- See [docs/current/ARCHITECTURE.md](docs/current/ARCHITECTURE.md)

## Documentation

### Core Documentation
- [Architecture Documentation](docs/current/ARCHITECTURE.md) - System architecture and design patterns
- [Refactoring Summary](docs/current/REFACTORING_SUMMARY.md) - Recent refactoring changes
- [Fax Removal Notes](docs/current/FAX_REMOVAL_NOTES.md) - Fax field removal documentation

### Dashboard Documentation
- [Dashboard Guide](docs/dashboard/DASHBOARD_GUIDE.md) - Dashboard usage and features
- [Dashboard Setup](docs/dashboard/DASHBOARD_SETUP.md) - Dashboard configuration and installation

### Additional Resources
- [Archived Documentation](docs/archive/) - Historical documentation and old integration guides

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Document functions with docstrings
- Keep functions focused and single-purpose

### Testing

- Write unit tests for new features
- Test integration points with external APIs
- Validate template generation
- Test configuration loading

## Support

For issues and questions, please refer to the documentation in `docs/current/`.

## License

[Add license information]

## Contributors

[Add contributor information]
