# Field Hockey Broadcasting Platform - Web Frontend

A modern React-based web application for the AI-powered field hockey broadcasting platform.

## 🎯 Features

### Live Streaming
- **HLS Video Player**: High-quality live streaming with adaptive bitrate
- **Multi-camera Support**: Switch between different camera angles
- **Real-time Controls**: Play, pause, seek, and quality selection
- **Mobile Responsive**: Optimized for all device sizes

### AI Commentary
- **Real-time Commentary**: AI-generated play-by-play commentary
- **Commentary Toggle**: Enable/disable AI commentary
- **Voice Controls**: Adjust commentary volume and speed
- **Multi-language Support**: English commentary with expandable language support

### Interactive Features
- **Live Chat**: Real-time community chat during matches
- **Interactive Polls**: Viewer participation and predictions
- **Gamification**: Trivia, predictions, and rewards system
- **Event Alerts**: Animated notifications for goals, cards, and highlights

### Player Analytics
- **Player Profiles**: Detailed player statistics and information
- **Real-time Stats**: Live match statistics and analytics
- **Heat Maps**: Player movement and positioning visualization
- **Performance Metrics**: Goals, assists, and other key metrics

### Admin Panel
- **Stream Management**: Create, edit, and manage live streams
- **User Management**: Administer user accounts and permissions
- **Analytics Dashboard**: View platform usage and performance metrics
- **Model Training**: Monitor AI model training progress

## 🧠 Tech Stack

### Core Framework
- **React 18**: Latest React with concurrent features
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and development server

### State Management
- **Zustand**: Lightweight state management
- **React Query**: Server state management and caching
- **React Hook Form**: Form handling and validation

### UI/UX
- **TailwindCSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **React Icons**: Comprehensive icon library
- **React Hot Toast**: Toast notifications

### Video & Media
- **HLS.js**: HLS video streaming
- **React Player**: Video player component
- **Socket.io**: Real-time communication

### Development Tools
- **ESLint**: Code linting and formatting
- **Vitest**: Unit testing framework
- **Testing Library**: React component testing

## 📁 Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── ui/              # Basic UI components
│   ├── video/           # Video player components
│   ├── chat/            # Chat and community components
│   ├── analytics/       # Analytics and stats components
│   └── admin/           # Admin panel components
├── pages/               # Page components
│   ├── Home.tsx         # Landing page
│   ├── Stream.tsx       # Live stream page
│   ├── Analytics.tsx    # Analytics dashboard
│   └── Admin.tsx        # Admin panel
├── hooks/               # Custom React hooks
│   ├── useStream.ts     # Stream management hook
│   ├── useChat.ts       # Chat functionality hook
│   └── useAnalytics.ts  # Analytics data hook
├── stores/              # Zustand stores
│   ├── streamStore.ts   # Stream state management
│   ├── userStore.ts     # User state management
│   └── uiStore.ts       # UI state management
├── services/            # API services
│   ├── api.ts           # Base API configuration
│   ├── streamService.ts # Stream-related API calls
│   └── authService.ts   # Authentication API calls
├── utils/               # Utility functions
│   ├── constants.ts     # Application constants
│   ├── helpers.ts       # Helper functions
│   └── types.ts         # TypeScript type definitions
├── styles/              # Global styles
│   └── globals.css      # Global CSS and Tailwind imports
└── App.tsx              # Main application component
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm 8+
- Backend API running (see backend setup)

### Installation

1. **Clone the repository**
```bash
cd platform/frontend/web
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env.local
```

Edit `.env.local` with your configuration:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME=Field Hockey Broadcasting
```

4. **Start development server**
```bash
npm run dev
```

5. **Open browser**
Navigate to `http://localhost:3000`

### Building for Production

1. **Build the application**
```bash
npm run build
```

2. **Preview production build**
```bash
npm run preview
```

## 🎨 Design System

### Color Palette
- **Primary**: Hockey green (#2E7D32)
- **Secondary**: Field blue (#1976D2)
- **Accent**: Goal orange (#FF9800)
- **Background**: Dark theme (#121212)
- **Surface**: Card background (#1E1E1E)

### Typography
- **Headings**: Inter font family
- **Body**: System font stack
- **Monospace**: JetBrains Mono for code

### Components
- **Buttons**: Primary, secondary, and ghost variants
- **Cards**: Elevated surfaces with hover effects
- **Inputs**: Form inputs with validation states
- **Modals**: Overlay dialogs and confirmations

## 📱 Responsive Design

### Breakpoints
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px+

### Mobile-First Features
- Touch-friendly controls
- Swipe gestures for navigation
- Optimized video player for mobile
- Responsive chat interface

## 🔧 Configuration

### Environment Variables
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

### Feature Flags
- **Chat**: Enable/disable live chat functionality
- **Polls**: Enable/disable interactive polls
- **Analytics**: Enable/disable analytics dashboard
- **Admin**: Enable/disable admin panel access

## 🧪 Testing

### Unit Tests
```bash
npm run test
```

### UI Tests
```bash
npm run test:ui
```

### Coverage Report
```bash
npm run test:coverage
```

### E2E Tests
```bash
npm run test:e2e
```

## 📊 Performance

### Optimization Strategies
- **Code Splitting**: Route-based code splitting
- **Lazy Loading**: Component lazy loading
- **Image Optimization**: WebP format with fallbacks
- **Bundle Analysis**: Regular bundle size monitoring

### Performance Metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🔒 Security

### Security Measures
- **HTTPS Only**: Secure connections in production
- **Content Security Policy**: XSS protection
- **Input Validation**: Client-side validation
- **API Security**: JWT token authentication

### Data Protection
- **User Privacy**: GDPR compliance
- **Data Encryption**: End-to-end encryption for sensitive data
- **Access Control**: Role-based access control

## 🌐 Internationalization

### Supported Languages
- **English** (default)
- **Spanish** (planned)
- **French** (planned)
- **German** (planned)

### Localization Features
- **RTL Support**: Right-to-left language support
- **Date/Time Formatting**: Locale-specific formatting
- **Number Formatting**: Currency and number formatting
- **Cultural Adaptations**: Sport-specific terminology

## 🤝 Contributing

### Development Workflow
1. Create feature branch from `main`
2. Implement feature with tests
3. Run linting and tests
4. Create pull request
5. Code review and merge

### Code Standards
- **TypeScript**: Strict type checking
- **ESLint**: Code quality enforcement
- **Prettier**: Code formatting
- **Conventional Commits**: Commit message format

## 📚 Documentation

### API Documentation
- **OpenAPI Spec**: `/api/docs`
- **Type Definitions**: Generated from API spec
- **Error Handling**: Standardized error responses

### Component Documentation
- **Storybook**: Component library and examples
- **Props Documentation**: Detailed prop descriptions
- **Usage Examples**: Code examples and patterns

## 🆘 Support

### Getting Help
- **Documentation**: Check the docs first
- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub discussions for questions
- **Community**: Join our Discord server

### Common Issues
- **Video Playback**: Check HLS.js compatibility
- **Performance**: Monitor bundle size and loading times
- **Mobile Issues**: Test on various devices and browsers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the field hockey community** 