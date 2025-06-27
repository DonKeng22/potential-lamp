**IMPORTANT:** For project status, progress, and issues, refer to the `../../../docs/project_status/progress_log.md` file. Any changes implemented should be logged there with a brief description and the reason for the change.

# Training Interface

This module provides a web-based interface for uploading training data and training AI models for the field hockey broadcasting platform.

## 🎯 Features

### Data Management
- **Video Upload**: Upload field hockey match videos for training
- **Annotation Upload**: Upload labeled training data
- **Data Validation**: Validate uploaded data format and quality
- **Data Organization**: Organize training data by categories

### Model Training
- **Computer Vision Models**: Train YOLOv8 models for object detection
- **NLP Models**: Train commentary generation models
- **Audio Models**: Train TTS models for voice synthesis
- **Training Monitoring**: Real-time training progress and metrics

### Model Management
- **Model Versioning**: Track different model versions
- **Performance Comparison**: Compare model performance
- **Model Deployment**: Deploy trained models to production
- **Model Rollback**: Rollback to previous model versions

## 🧠 Supported Models

### Computer Vision
- **YOLOv8**: Object detection (players, ball, referee, goals, cards)
- **Custom Classifiers**: Event-specific classifiers
- **Player Recognition**: Facial recognition and jersey number OCR

### Natural Language Processing
- **Commentary Generator**: GPT-based sports commentary
- **Event Classifier**: Classify match events from text
- **Sentiment Analysis**: Analyze commentary tone and emotion

### Audio Processing
- **Text-to-Speech**: Generate audio commentary
- **Speech Recognition**: Convert audio to text
- **Audio Enhancement**: Improve audio quality

## 📁 Structure

```
training_interface/
├── web/                    # Web interface
│   ├── static/            # CSS, JS, images
│   ├── templates/         # HTML templates
│   └── app.py             # Flask web application
├── api/                   # Training API endpoints
│   ├── data_upload.py     # Data upload handlers
│   ├── model_training.py  # Training job management
│   └── model_management.py # Model versioning and deployment
├── utils/                 # Utility functions
│   ├── data_validator.py  # Data validation utilities
│   ├── model_evaluator.py # Model evaluation tools
│   └── file_processor.py  # File processing utilities
└── config/                # Configuration files
    ├── training_config.py # Training parameters
    └── model_configs.py   # Model-specific configurations
```

## 🚀 Usage

### Web Interface
1. Start the training interface server:
```bash
cd training_interface/web
python app.py
```

2. Open browser and navigate to `http://localhost:5000`

3. Upload training data and start training jobs

### API Usage
```python
from training_interface.api import TrainingAPI

api = TrainingAPI()

# Upload training data
api.upload_video("path/to/video.mp4", "field_hockey_match")
api.upload_annotations("path/to/annotations.json")

# Start training
job_id = api.start_training("yolov8", "hockey_detector")

# Monitor training
status = api.get_training_status(job_id)
```

## 📊 Data Formats

### Video Data
- **Supported Formats**: MP4, AVI, MOV, MKV
- **Resolution**: 720p minimum, 1080p recommended
- **Duration**: 5-90 minutes per match
- **Quality**: Clear, well-lit footage

### Annotation Data
```json
{
  "video_id": "match_001",
  "annotations": [
    {
      "frame_number": 150,
      "objects": [
        {
          "bbox": [x, y, width, height],
          "class": "player",
          "player_id": "player_001",
          "confidence": 0.95
        }
      ],
      "events": [
        {
          "type": "goal",
          "timestamp": "00:02:30",
          "description": "Goal scored by player_001"
        }
      ]
    }
  ]
}
```

### Training Configuration
```yaml
model:
  name: "yolov8_hockey_detector"
  type: "object_detection"
  base_model: "yolov8n.pt"
  
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

## 🔧 Configuration

### Training Parameters
- **Epochs**: 50-200 depending on dataset size
- **Batch Size**: 8-32 based on GPU memory
- **Learning Rate**: 0.001-0.0001 with scheduling
- **Validation Split**: 20% for validation

### Hardware Requirements
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **RAM**: 16GB+ system memory
- **Storage**: SSD for fast data loading
- **Network**: High-speed internet for data upload

## 📈 Monitoring

### Training Metrics
- **Loss**: Training and validation loss curves
- **Accuracy**: Detection accuracy and mAP
- **Performance**: FPS and inference time
- **Resource Usage**: GPU, CPU, and memory utilization

### Real-time Monitoring
- **Live Dashboard**: Real-time training progress
- **Log Streaming**: Live training logs
- **Alert System**: Notifications for training issues
- **Performance Tracking**: Model performance over time

## 🔄 Workflow

### 1. Data Preparation
1. Upload video files
2. Upload or create annotations
3. Validate data quality
4. Organize into training sets

### 2. Model Training
1. Select model type and configuration
2. Start training job
3. Monitor training progress
4. Evaluate model performance

### 3. Model Deployment
1. Validate model on test data
2. Compare with previous models
3. Deploy to production
4. Monitor production performance

### 4. Continuous Improvement
1. Collect feedback and new data
2. Retrain models with new data
3. Validate improvements
4. Deploy updated models

## 🧪 Testing

### Unit Tests
```bash
pytest training_interface/tests/
```

### Integration Tests
```bash
python training_interface/tests/test_integration.py
```

### Performance Tests
```bash
python training_interface/benchmark.py
```

## 📚 Documentation

### API Documentation
- **Swagger UI**: `/docs` endpoint
- **OpenAPI Spec**: `/openapi.json`
- **Code Examples**: See `examples/` directory

### User Guide
- **Getting Started**: Basic setup and usage
- **Advanced Features**: Advanced training options
- **Troubleshooting**: Common issues and solutions

## 🤝 Contributing

1. Follow the existing code structure
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Validate training workflows before merging

## 📞 Support

For training-related issues:
- Check the troubleshooting guide
- Review training logs
- Contact the ML team
- Create an issue in the repository 