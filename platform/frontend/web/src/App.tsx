import React, { useState, useEffect } from 'react';
import './App.css';
import VideoManager from './components/VideoManager';
import TaskMonitor from './components/TaskMonitor';
import { ApiService } from './api';

function App() {
  const [currentPage, setCurrentPage] = useState<'videos' | 'tasks'>('videos');
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [apiInfo, setApiInfo] = useState<any>(null);

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const health = await ApiService.healthCheck();
      setApiInfo(health);
      setApiStatus('online');
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('offline');
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🏑 Field Hockey Broadcasting Platform</h1>
          <div className="api-status">
            <span className={`status-indicator ${apiStatus}`}></span>
            <span className="status-text">
              {apiStatus === 'checking' && 'Checking API...'}
              {apiStatus === 'online' && `API Online - ${apiInfo?.service || 'Unknown'} v${apiInfo?.version || '1.0.0'}`}
              {apiStatus === 'offline' && 'API Offline - Please check backend'}
            </span>
            <button onClick={checkApiHealth} className="refresh-btn">
              🔄
            </button>
          </div>
        </div>
        
        <nav className="nav-tabs">
          <button 
            className={`nav-tab ${currentPage === 'videos' ? 'active' : ''}`}
            onClick={() => setCurrentPage('videos')}
          >
            📹 Video Management
          </button>
          <button 
            className={`nav-tab ${currentPage === 'tasks' ? 'active' : ''}`}
            onClick={() => setCurrentPage('tasks')}
          >
            ⚙️ Task Monitor
          </button>
        </nav>
      </header>

      <main className="main-content">
        {apiStatus === 'offline' && (
          <div className="alert alert-error">
            <h3>⚠️ Backend Connection Failed</h3>
            <p>
              Make sure the backend is running on port 8000. 
              You can start it with: <code>docker compose up backend</code>
            </p>
            <button onClick={checkApiHealth} className="retry-btn">
              Retry Connection
            </button>
          </div>
        )}

        {apiStatus === 'online' && (
          <>
            {currentPage === 'videos' && <VideoManager />}
            {currentPage === 'tasks' && <TaskMonitor />}
          </>
        )}

        {apiStatus === 'checking' && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Connecting to backend...</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Field Hockey Broadcasting Platform - AI-powered video analysis and annotation</p>
      </footer>
    </div>
  );
}

export default App;
