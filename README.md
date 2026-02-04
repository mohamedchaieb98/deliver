# Water Delivery Management System

A comprehensive internal management system for water delivery operations with responsive web interface.

## Features

- **Admin Interface**: Order management, inventory tracking, route planning, analytics
- **Mobile Interface**: Deliverer routes, delivery updates, expense logging
- **Real-time Updates**: Live tracking and notifications
- **Inventory Management**: Stock tracking with low-stock alerts
- **Payment Tracking**: Payment collection and outstanding balances

## Tech Stack

- **Backend**: FastAPI + PostgreSQL + Redis
- **Frontend**: React + TypeScript + Tailwind CSS
- **Architecture**: Single responsive web app (no authentication)

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repo-url>
   cd water-delivery-system
   ```

2. **Start with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Access Application**
   - Web App: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Setup
```bash
# Create database
docker-compose exec db createdb -U postgres water_delivery_db

# Run migrations
cd backend
alembic upgrade head

# Seed initial data
python -m app.seeds.initial_data
```

## Project Structure

```
water-delivery-system/
├── backend/                 # FastAPI backend
├── frontend/                # React frontend
├── database/               # Database scripts
├── docs/                   # Documentation
├── docker-compose.yml      # Development environment
└── README.md
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

MIT License