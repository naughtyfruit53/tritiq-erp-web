# Tritiq ERP Web Application

A complete FastAPI-based ERP (Enterprise Resource Planning) system migrated from PySide6 desktop application to a modern web interface.

## Features

### Core ERP Modules
- **User Management & Authentication**: Role-based access control
- **Company Details Management**: Complete company setup with GST/PAN integration
- **Customer & Vendor Management**: Comprehensive contact management
- **Product Management**: With HSN codes, pricing, and inventory tracking
- **Manufacturing Management**: BOM (Bill of Materials) and Work Orders
- **Stock Management**: Real-time inventory tracking
- **Voucher System**: Dynamic voucher types for Sales, Purchase, GRN, etc.
- **Backup & Restore**: Complete data management with auto-backup
- **Document Sequencing**: Automatic numbering for all vouchers

### Technical Features
- **FastAPI Framework**: Modern, fast, async web framework
- **SQLAlchemy ORM**: With async support and proper session management
- **Database Support**: SQLite for development, PostgreSQL for production
- **Responsive UI**: Bootstrap-based interface
- **API Documentation**: Auto-generated with FastAPI/Swagger
- **Alembic Migrations**: Database schema version control

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (for production) or SQLite (for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/naughtyfruit53/tritiq-erp-web.git
   cd tritiq-erp-web
   ```

2. **Install dependencies**
   ```bash
   cd src
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

4. **Initialize database**
   ```bash
   alembic upgrade head
   ```

5. **Run the application**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

6. **Access the application**
   - Open http://localhost:8000 in your browser
   - Complete first-time setup by creating an admin user
   - Login and start using the ERP system

## Database Configuration

### Development (SQLite)
```bash
DATABASE_URL=sqlite+aiosqlite:///./tritiq_erp.db
```

### Production (PostgreSQL/Supabase)
```bash
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database
```

## Project Structure

```
src/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── auth.py                # Authentication utilities
├── db/                    # Database layer
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── crud/             # Database operations
│   ├── migrations/       # Alembic migrations
│   └── session.py        # Database session management
├── api/                   # API endpoints
│   └── v1/               # API version 1
├── web_routes/           # Web interface routes
├── services/             # Business logic
├── templates/            # Jinja2 templates
└── static/               # Static files (CSS, JS, images)
```

## Migration from PySide6

This web application is a complete migration from the PySide6 desktop ERP application with the following improvements:

### Fixed Issues
- **Session Management**: Resolved voucher saving issues through proper async session handling
- **Scalability**: Web-based architecture supports multiple concurrent users
- **Deployment**: Easy deployment to cloud platforms like Supabase
- **Accessibility**: Browser-based interface accessible from any device

### Preserved Features
- All business logic and workflows from the desktop application
- Complete data model with all entity relationships
- Manufacturing workflows (BOM, Work Orders)
- Comprehensive voucher system
- User permission management
- Backup and restore functionality

## API Documentation

Once the application is running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### Supabase Deployment
1. Create a Supabase project
2. Get your database connection string
3. Update the DATABASE_URL in your environment
4. Deploy using your preferred platform (Vercel, Heroku, etc.)

### Environment Variables for Production
```bash
DATABASE_URL=your_supabase_connection_string
SECRET_KEY=your_strong_secret_key
ENVIRONMENT=production
DEBUG=False
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is proprietary software developed for Tritiq ERP system.

## Support

For support and questions, please contact the development team or create an issue in the repository.