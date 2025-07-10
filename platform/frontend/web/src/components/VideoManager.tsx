import React, { useState, useEffect, useCallback } from 'react';
import { ApiService, Video } from '../api';
import './VideoManager.css';

const VideoManager: React.FC = () => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [currentPage, setCurrentPage] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [error, setError] = useState<string>('');
  const [processingVideo, setProcessingVideo] = useState<number | null>(null);

  const pageSize = 10;

  const loadVideos = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response = await ApiService.getVideos(
        currentPage * pageSize, 
        pageSize, 
        statusFilter || undefined
      );
      setVideos(response.videos);
      setTotalCount(response.count);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load videos');
    } finally {
      setLoading(false);
    }
  }, [currentPage, statusFilter]);

  useEffect(() => {
    loadVideos();
  }, [loadVideos]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Check file type
      if (!file.type.startsWith('video/')) {
        setError('Please select a video file');
        return;
      }
      
      // Check file size (100MB limit)
      const maxSize = 100 * 1024 * 1024;
      if (file.size > maxSize) {
        setError('File size exceeds 100MB limit');
        return;
      }
      
      setSelectedFile(file);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError('');
    try {
      const response = await ApiService.uploadVideo(selectedFile);
      console.log('Upload successful:', response);
      setSelectedFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('video-upload') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      // Reload videos
      await loadVideos();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleProcessVideo = async (videoId: number) => {
    setProcessingVideo(videoId);
    setError('');
    try {
      const response = await ApiService.processVideo(videoId, 'analysis');
      console.log('Processing started:', response);
      
      // Reload videos to update status
      await loadVideos();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start processing');
    } finally {
      setProcessingVideo(null);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString();
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'uploaded': return '#3498db';
      case 'processing': return '#f39c12';
      case 'completed': return '#27ae60';
      case 'failed': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <div className="video-manager">
      <div className="section">
        <h2>📹 Video Upload</h2>
        <div className="upload-area">
          <div className="file-input-wrapper">
            <input
              id="video-upload"
              type="file"
              accept="video/*"
              onChange={handleFileSelect}
              disabled={uploading}
            />
            <label htmlFor="video-upload" className="file-input-label">
              {selectedFile ? selectedFile.name : 'Choose video file...'}
            </label>
          </div>
          
          {selectedFile && (
            <div className="file-info">
              <p><strong>File:</strong> {selectedFile.name}</p>
              <p><strong>Size:</strong> {formatFileSize(selectedFile.size)}</p>
              <p><strong>Type:</strong> {selectedFile.type}</p>
            </div>
          )}
          
          <button 
            className="upload-btn"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
          >
            {uploading ? '⏳ Uploading...' : '📤 Upload Video'}
          </button>
        </div>
      </div>

      <div className="section">
        <div className="section-header">
          <h2>📋 Video Library</h2>
          <div className="controls">
            <select 
              value={statusFilter} 
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setCurrentPage(0);
              }}
              className="filter-select"
            >
              <option value="">All Status</option>
              <option value="uploaded">Uploaded</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
            </select>
            
            <button onClick={loadVideos} disabled={loading} className="refresh-btn">
              {loading ? '⏳' : '🔄'} Refresh
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {loading && (
          <div className="loading-message">
            <div className="spinner"></div>
            Loading videos...
          </div>
        )}

        {!loading && videos.length === 0 && (
          <div className="empty-state">
            <p>📭 No videos found. Upload a video to get started!</p>
          </div>
        )}

        {!loading && videos.length > 0 && (
          <div className="video-grid">
            {videos.map((video) => (
              <div key={video.id} className="video-card">
                <div className="video-header">
                  <h3 className="video-title">{video.original_name}</h3>
                  <span 
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(video.status) }}
                  >
                    {video.status}
                  </span>
                </div>
                
                <div className="video-details">
                  <p><strong>ID:</strong> {video.id}</p>
                  <p><strong>Filename:</strong> {video.filename}</p>
                  {video.file_size && (
                    <p><strong>Size:</strong> {formatFileSize(video.file_size)}</p>
                  )}
                  <p><strong>Type:</strong> {video.content_type || 'Unknown'}</p>
                  <p><strong>Uploaded:</strong> {formatDate(video.created_at)}</p>
                  {video.updated_at !== video.created_at && (
                    <p><strong>Updated:</strong> {formatDate(video.updated_at)}</p>
                  )}
                </div>
                
                <div className="video-actions">
                  <button
                    className="process-btn"
                    onClick={() => handleProcessVideo(video.id)}
                    disabled={processingVideo === video.id || video.status === 'processing'}
                  >
                    {processingVideo === video.id ? '⏳ Starting...' : '🔬 Process Video'}
                  </button>
                  
                  <button
                    className="view-btn"
                    onClick={() => {
                      // TODO: Navigate to video details page
                      console.log('View video:', video.id);
                    }}
                  >
                    👁️ View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {totalPages > 1 && (
          <div className="pagination">
            <button 
              onClick={() => setCurrentPage(0)}
              disabled={currentPage === 0}
              className="page-btn"
            >
              ⏮️ First
            </button>
            <button 
              onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
              disabled={currentPage === 0}
              className="page-btn"
            >
              ⏪ Previous
            </button>
            
            <span className="page-info">
              Page {currentPage + 1} of {totalPages} ({totalCount} total videos)
            </span>
            
            <button 
              onClick={() => setCurrentPage(Math.min(totalPages - 1, currentPage + 1))}
              disabled={currentPage >= totalPages - 1}
              className="page-btn"
            >
              Next ⏩
            </button>
            <button 
              onClick={() => setCurrentPage(totalPages - 1)}
              disabled={currentPage >= totalPages - 1}
              className="page-btn"
            >
              Last ⏭️
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoManager;