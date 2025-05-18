# Bacterial Classification System

A machine learning system for classifying bacteria as pathogenic or non-pathogenic based on their characteristics. This project uses data scraped from MiMeDB and applies ensemble learning techniques to differentiate between pathogenic and non-pathogenic bacteria in the human body.

## Features

- **Web Scraper**: Collects bacteria data from MiMeDB
- **Database**: Stores bacteria characteristics with PostgreSQL
- **API**: FastAPI backend with comprehensive endpoints
- **Ensemble Learning**: Uses Random Forest, AdaBoost, and XGBoost for classification
- **Standardized API Responses**: Consistent JSON format with pagination, error handling, and metadata
- **External Database Support**: Works with remote PostgreSQL databases (including Neon)

## Prerequisites

- Docker and Docker Compose
- PostgreSQL (local or remote)
- Python 3.12

## Quick Start

### 1. Set Up Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your database credentials
nano .env
```

### 2. Start Services

For local development with embedded PostgreSQL:

```bash
# Build and start all services
make build
make up
```

### 3. Initialize Database and Collect Data

```bash
# Initialize database schema
make init-db

# Run scraper to collect bacteria data
make scrape
```

### 4. Access API

The API is available at:

- API Base: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

## Authors

- Moh Fairuz Alauddin Yahya - 13522057
- Rayhan Fadhlan Azka - 13522095
- Rayendra Althaf Taraka Noor - 13522107
