**IMPORTANT:** For project status, progress, and issues, refer to the `../../../docs/project_status/progress_log.md` file. Any changes implemented should be logged there with a brief description and the reason for the change.

# Computer Vision Models

This module contains computer vision models for field hockey event detection and player tracking.

## 🎯 Features

### Event Detection
- **Goal Detection**: Identify when a goal is scored
- **Card Detection**: Detect yellow/red cards shown by referees
- **Corner Detection**: Identify penalty corners and short corners
- **Player Detection**: Track individual players on the field
- **Ball Tracking**: Follow the ball throughout the match

### Player Analytics
- **Facial Recognition**: Identify players by face
- **Jersey Number OCR**: Read player jersey numbers
- **Movement Tracking**: Track player positions and movements
- **Action Recognition**: Identify player actions (pass, shoot, tackle)

## 🧠 Models

### YOLOv8 Implementation
- **Base Model**: YOLOv8n (nano) for real-time processing
- **Custom Training**: Fine-tuned on field hockey data
- **Multi-class Detection**: Players, ball, referee, goals, cards

### Model Classes
1. **Player** (class 0): Individual players
2. **Ball** (class 1): Field hockey ball
3. **Referee** (class 2): Match officials
4. **Goal** (class 3): Goal posts
5. **Card** (class 4): Yellow/red cards
6. **Corner** (class 5): Corner markers

## 📁 Structure

```
cv_models/
├── main.py              # Main CV pipeline
├── detector.py          # YOLOv8 detection wrapper
├── tracker.py           # Object tracking
├── events.py            # Event detection logic
├── player_id.py         # Player identification
├── utils.py             # Utility functions
└── models/              # Trained model files
    ├── yolov8n.pt       # Base YOLOv8 model
    └── hockey_detector.pt # Custom trained model
```

## 🚀 Usage

### Basic Detection
```python
from cv_models.detector import HockeyDetector

detector = HockeyDetector()
results = detector.detect(video_frame)
```

### Event Detection
```python
from cv_models.events import EventDetector

event_detector = EventDetector()
events = event_detector.detect_events(video_frames)
```

### Player Tracking
```python
from cv_models.player_id import PlayerIdentifier

identifier = PlayerIdentifier()
player_info = identifier.identify_player(player_roi)
```

## 📊 Training Data

### Data Sources
- Field hockey match videos (Olympics, World Cup, Pro League)
- Annotated training data in `../data/annotations/`
- Synthetic data generation for edge cases

### Annotation Format
```json
{
  "image_id": "frame_001.jpg",
  "annotations": [
    {
      "bbox": [x, y, width, height],
      "category_id": 0,
      "player_id": "player_001"
    }
  ]
}
```

## 🔧 Configuration

### Model Settings
- **Confidence Threshold**: 0.5
- **NMS Threshold**: 0.4
- **Input Size**: 640x640
- **Batch Size**: 16 (training)

### Performance Optimization
- **GPU Acceleration**: CUDA support
- **Model Quantization**: INT8 for mobile deployment
- **Batch Processing**: Real-time pipeline optimization

## 📈 Performance Metrics

### Detection Accuracy
- **mAP@0.5**: 0.85+
- **Precision**: 0.90+
- **Recall**: 0.80+

### Real-time Performance
- **FPS**: 30+ on GPU
- **Latency**: <33ms per frame
- **Memory Usage**: <2GB GPU memory

## 🧪 Testing

### Unit Tests
```bash
pytest cv_models/tests/
```

### Performance Tests
```bash
python cv_models/benchmark.py
```

### Validation
```bash
python cv_models/validate.py --data ../data/annotations/
```

## 🔄 Continuous Improvement

### Model Updates
1. Collect new training data
2. Retrain model with new data
3. Validate performance
4. Deploy updated model

### Feedback Loop
- User feedback on detection accuracy
- Manual annotation corrections
- Automated quality assessment

## 📚 References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Field Hockey Rules](https://www.fih.hockey/events/fih-pro-league)

## 🤝 Contributing

1. Follow the existing code structure
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Validate model performance before merging 