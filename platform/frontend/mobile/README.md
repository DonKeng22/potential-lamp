**IMPORTANT:** For project status, progress, and issues, refer to the `../../../docs/project_status/progress_log.md` file. Any changes implemented should be logged there with a brief description and the reason for the change.

# Field Hockey Broadcasting Platform - Mobile Frontend

A cross-platform mobile application built with Flutter for the AI-powered field hockey broadcasting platform.

## 🎯 Features

### MVP Scope
- **Live Streaming**: View live field hockey matches.
- **Player Profiles**: Browse detailed player statistics and information.

### Planned Features
- **AI Commentary**: Toggle AI-generated commentary.
- **Interactive Features**: Live chat, polls, and gamification.
- **Notifications**: Real-time alerts for match events.

## 🧠 Tech Stack

- **Framework**: Flutter
- **Language**: Dart
- **State Management**: Provider or Riverpod (to be decided based on complexity)
- **Networking**: Dio
- **Video Player**: `video_player` or a more robust HLS-compatible player
- **UI/UX**: Material Design principles

## 📁 Project Structure

```
mobile/
├── lib/
│   ├── api/                # API service integrations
│   ├── models/             # Data models
│   ├── screens/            # Major screens/pages
│   │   ├── home/
│   │   ├── stream/
│   │   └── player_profile/
│   ├── widgets/            # Reusable UI widgets
│   ├── services/           # Background services (e.g., notifications)
│   ├── utils/              # Utility functions and helpers
│   └── main.dart           # Main application entry point
├── assets/
│   ├── images/             # UI images, logos, placeholders
│   └── fonts/              # Custom fonts
├── pubspec.yaml            # Project dependencies and metadata
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites
- Flutter SDK installed and configured.
- Android Studio or VS Code with Flutter plugins.
- Backend API running (see main `platform/README.md`).

### Installation

1.  **Navigate to the mobile directory**
    ```bash
    cd platform/frontend/mobile
    ```

2.  **Get Flutter dependencies**
    ```bash
    flutter pub get
    ```

3.  **Run the application**
    ```bash
    flutter run
    ```

## 🤝 Contributing

Contributions are welcome! Please follow the general project contribution guidelines.
