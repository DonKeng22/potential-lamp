# 🏑 Multi-Platform Field Hockey Broadcasting and Engagement Application

An AI-powered multi-platform application for live field hockey broadcasting, real-time commentary generation, community engagement, and advanced player analytics.

## 🎯 Features

### Core Broadcasting
- **Live Streaming**: Real-time field hockey match broadcasting
- **Video Upload**: Support for direct file uploads and YouTube links
- **Multi-Platform Support**: Web, mobile, and desktop interfaces
- **HLS Streaming**: High-quality video delivery using FFmpeg

### AI-Powered Commentary
- **Real-time Commentary**: AI-generated play-by-play commentary
- **Computer Vision**: Event detection (goals, cards, corners, etc.)
- **NLP Models**: Sports commentary generation trained on cricket/football/hockey
- **TTS Integration**: Text-to-speech for audio commentary

### Player Analytics & Profiles
- **Facial Recognition**: Player identification via facial/jersey detection
- **Match Statistics**: Comprehensive player performance tracking
- **Historical Data**: Player career statistics and trends
- **Real-time Tracking**: Live player movement and action analysis

### Interactive Viewer Experience
- **Live Chat**: Real-time community engagement
- **Interactive Polls**: Viewer participation and predictions
- **Gamification**: Trivia, predictions, and rewards system
- **Event Animations**: Goal celebrations, card alerts, and highlights

### Global Support
- **Multi-language UI**: Starting with English (expandable)
- **English Commentary**: AI-generated English commentary
- **Responsive Design**: Mobile-first approach with desktop optimization

### Admin & Training
- **Model Training Interface**: Upload and train AI models
- **Admin Panel**: Stream management and monitoring
- **Data Management**: Training data organization and versioning

## 🧠 Tech Stack

### Backend
- **Framework**: Python FastAPI
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Streaming**: HLS, FFmpeg, AWS IVS (or open-source equivalent)

### AI/ML
- **Computer Vision**: PyTorch, OpenCV, YOLOv8, Ultralytics
- **NLP**: HuggingFace Transformers, GPT-based models
- **Audio Processing**: Whisper (OpenAI), Coqui TTS
- **Model Training**: Custom training pipelines

### Frontend
- **Web**: React.js with TypeScript
- **Mobile**: Flutter (cross-platform)
- **Styling**: TailwindCSS
- **State Management**: Redux/Zustand

### Infrastructure
- **Cloud**: AWS/Google Cloud/Azure
- **CDN**: Cloudflare/Fastly
- **Monitoring**: Prometheus, Grafana
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

This guide will help you set up and run the Field Hockey Broadcasting Platform locally.

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd potential-lamp
    ```

2.  **Run with Docker Compose**
    ```bash
    docker-compose up --build
    ```

    This will:
    - Build the backend and frontend Docker images.
    - Start PostgreSQL, Redis, backend, and frontend services.

    The backend will be accessible at `http://localhost:8000` and the frontend at `http://localhost:3000`.

## 📊 Initial Data

To get started quickly, you can populate your database with some sample data. This includes:
-   **Sample Users**: For testing authentication and user-specific features.
-   **Sample Streams**: Pre-defined live or past match streams with placeholder HLS URLs.
-   **Sample Players**: Basic profiles for field hockey players with placeholder images and initial statistics.

You can find scripts or instructions for generating this initial data in the `data/scripts` directory (to be implemented). Alternatively, you can manually add data via the API or database client.


## 📁 Project Structure

```
platform/
├── backend/
│   ├── api/                 # FastAPI routes and endpoints
│   ├── video_streaming/     # HLS streaming and video processing
│   ├── cv_models/          # Computer vision models and pipelines
│   ├── audio_models/       # Audio processing and TTS
│   ├── nlp_models/         # NLP models for commentary
│   ├── player_profiles/    # Player tracking and analytics
│   ├── community/          # Chat, polls, engagement features
│   └── data/              # Database models and migrations
├── frontend/
│   ├── web/               # React web application
│   └── mobile/            # Flutter mobile application
├── training_interface/    # Model training and data management
├── data/
│   ├── raw_videos/        # Training video data
│   └── annotations/       # Model training annotations
└── assets/
    ├── ui_images/         # UI assets and images
    └── example_streams/   # Sample video content
```

## 🧪 Development Phases

### Phase 1: Core Infrastructure ✅
- [x] Project structure setup
- [ ] FastAPI backend with PostgreSQL
- [ ] Basic video upload and HLS streaming
- [ ] Frontend scaffolding (React + Flutter)

### Phase 2: Computer Vision Integration
- [ ] YOLOv8 player/ball/referee detection
- [ ] Event detection pipeline (goals, cards, corners)
- [ ] Training data annotation system

### Phase 3: AI Commentary and NLP
- [ ] Commentary transcript collection
- [ ] GPT-based commentary generation
- [ ] TTS integration for audio commentary

### Phase 4: Player Analytics
- [ ] Facial recognition and jersey OCR
- [ ] Player profile management
- [ ] Real-time statistics tracking

### Phase 5: UI/UX and Engagement
- [ ] Interactive dashboard with live stats
- [ ] Chat, polls, and gamification features
- [ ] Mobile-first responsive design

### Phase 6: Training Portal
- [ ] Model training interface
- [ ] Performance monitoring
- [ ] Continuous model improvement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation in each module's README

## 🎯 Roadmap

- [ ] Real-time multi-camera support
- [ ] Advanced analytics dashboard
- [ ] Mobile app optimization
- [ ] Integration with professional leagues
- [ ] AR/VR viewing experiences
- [ ] Automated highlight generation
- [ ] Social media integration
- [ ] Advanced monetization features

---

**Built with ❤️ for the field hockey community**
