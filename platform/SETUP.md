# 🏑 Field Hockey Broadcasting Platform - Setup Guide

This guide will help you set up the complete field hockey broadcasting platform on your local machine.

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+
- **RAM**: 16GB+ (32GB recommended for AI model training)
- **Storage**: 50GB+ free space
- **GPU**: NVIDIA GPU with 8GB+ VRAM (recommended for AI models)

### Software Requirements
- **Python**: 3.9+ with pip
- **Node.js**: 18+ with npm
- **PostgreSQL**: 13+
- **Redis**: 6+
- **FFmpeg**: Latest version
- **Git**: Latest version

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd potential-lamp/platform
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Database Setup
```bash
# Install PostgreSQL (if not already installed)
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# Create database
createdb field_hockey_broadcast

# Set up environment variables
cp .env.example .env
```

Edit `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost/field_hockey_broadcast
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production
```

#### Start Backend Services
```bash
# Start Redis (in a new terminal)
redis-server

# Start Celery worker (in a new terminal)
celery -A backend.celery_app worker --loglevel=info

# Start FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend/web
npm install
```

#### Configure Environment
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME=Field Hockey Broadcasting
```

#### Start Development Server
```bash
npm run dev
```

### 4. Training Interface Setup

#### Install Training Dependencies
```bash
cd training_interface
pip install -r requirements.txt
```

#### Start Training Interface
```bash
python web/app.py
```

## 🔧 Detailed Setup

### Backend Configuration

#### Database Migration
```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

#### AI Model Setup
```bash
# Download pre-trained models
mkdir -p models
cd models

# Download YOLOv8 base model
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# Download other models (if available)
# wget <model-urls>
```

#### Video Processing Setup
```bash
# Install FFmpeg
# Windows: Download from https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg

# Verify installation
ffmpeg -version
```

### Frontend Configuration

#### Build Configuration
```bash
# Development build
npm run build:dev

# Production build
npm run build

# Preview production build
npm run preview
```

#### Environment Variables
```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Application
VITE_APP_NAME=Field Hockey Broadcasting
VITE_APP_VERSION=1.0.0

# Features
VITE_ENABLE_CHAT=true
VITE_ENABLE_POLLS=true
VITE_ENABLE_ANALYTICS=true

# External Services
VITE_GOOGLE_ANALYTICS_ID=
VITE_SENTRY_DSN=
```

### Training Interface Configuration

#### Data Directory Setup
```bash
# Create data directories
mkdir -p data/raw_videos
mkdir -p data/annotations
mkdir -p data/processed

# Set permissions (Linux/macOS)
chmod 755 data/
```

#### Model Training Configuration
```yaml
# config/training_config.yaml
model:
  name: "yolov8_hockey_detector"
  type: "object_detection"
  base_model: "models/yolov8n.pt"
  
training:
  epochs: 100
  batch_size: 16
  learning_rate: 0.001
  validation_split: 0.2
  
data:
  input_size: [640, 640]
  augmentation: true
  mixup: 0.1
  mosaic: 0.5
```

## 🧪 Testing Setup

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend/web
npm run test
npm run test:coverage
```

### Integration Tests
```bash
# Run full integration test suite
python tests/integration/test_full_pipeline.py
```

## 📊 Monitoring Setup

### Application Monitoring
```bash
# Install monitoring tools
pip install prometheus-client grafana-api

# Start monitoring services
python monitoring/prometheus_exporter.py
```

### Log Management
```bash
# Configure structured logging
export LOG_LEVEL=INFO
export LOG_FORMAT=json

# View logs
tail -f logs/application.log
```

## 🔒 Security Setup

### SSL/TLS Configuration
```bash
# Generate SSL certificates (development)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configure HTTPS
export SSL_CERT_FILE=cert.pem
export SSL_KEY_FILE=key.pem
```

### Authentication Setup
```bash
# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set environment variable
export JWT_SECRET_KEY=your-generated-secret
```

## 🚀 Production Deployment

### Docker Setup
```bash
# Build Docker images
docker build -t field-hockey-backend ./backend
docker build -t field-hockey-frontend ./frontend/web
docker build -t field-hockey-training ./training_interface

# Run with Docker Compose
docker-compose up -d
```

### Kubernetes Setup
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/database.yaml
```

### Cloud Deployment
```bash
# AWS ECS deployment
aws ecs create-cluster --cluster-name field-hockey-cluster
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster field-hockey-cluster --service-name field-hockey-service --task-definition field-hockey:1
```

## 🔧 Troubleshooting

### Common Issues

#### Backend Issues
```bash
# Database connection error
# Check PostgreSQL is running
sudo systemctl status postgresql

# Redis connection error
# Check Redis is running
redis-cli ping

# Import errors
# Check virtual environment is activated
which python
pip list
```

#### Frontend Issues
```bash
# Build errors
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# API connection errors
# Check backend is running
curl http://localhost:8000/health
```

#### AI Model Issues
```bash
# CUDA errors
# Check GPU drivers
nvidia-smi

# Memory errors
# Reduce batch size in training config
# Increase system RAM or use smaller models
```

### Performance Optimization

#### Backend Optimization
```bash
# Enable GPU acceleration
export CUDA_VISIBLE_DEVICES=0

# Optimize database
# Add indexes for frequently queried columns
# Configure connection pooling

# Enable caching
# Configure Redis for session and data caching
```

#### Frontend Optimization
```bash
# Enable code splitting
# Configure lazy loading for routes
# Optimize bundle size with tree shaking

# Enable CDN
# Configure static asset delivery
# Enable gzip compression
```

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

### Community
- [GitHub Issues](https://github.com/your-repo/issues)
- [Discord Server](https://discord.gg/your-server)
- [Documentation Wiki](https://github.com/your-repo/wiki)

### Support
- **Email**: support@fieldhockeybroadcasting.com
- **Slack**: #field-hockey-platform
- **Office Hours**: Every Tuesday 2-4 PM UTC

## 🎯 Next Steps

### Phase 1: Basic Setup ✅
- [x] Backend API running
- [x] Frontend development server
- [x] Database connection
- [x] Basic video upload

### Phase 2: AI Integration
- [ ] Computer vision models
- [ ] NLP commentary generation
- [ ] Player tracking
- [ ] Event detection

### Phase 3: Advanced Features
- [ ] Real-time streaming
- [ ] Interactive features
- [ ] Analytics dashboard
- [ ] Mobile app

### Phase 4: Production
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Monitoring setup
- [ ] Deployment automation

---

**Happy coding! 🏑⚽** 