import React, { useState } from 'react';
import { startTraining, fetchAnnotations, fetchInsights } from './api';

const TrainingDashboard = () => {
  const [videoLink, setVideoLink] = useState('');
type Annotation = { id: number; video: string; events: number; description?: string };
type Insights = { totalVideos: number; totalEvents: number; mostCommonEvent: string };
const [annotations, setAnnotations] = useState<Annotation[]>([]);
const [insights, setInsights] = useState<Insights | null>(null);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [pageSize] = useState(10);
  const [uploading, setUploading] = useState(false);

  // Handler to submit a video link for annotation/training
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await startTraining(videoLink);
    setLoading(false);
    alert('Training started for: ' + videoLink);
  };

  // Handler to fetch trained data/annotations
  const handleFetchAnnotations = async (q = '', skip = 0) => {
    setLoading(true);
    const params = new URLSearchParams();
    if (q) params.append('q', q);
    params.append('skip', skip.toString());
    params.append('limit', pageSize.toString());
    const res = await fetch(`/api/train/annotations?${params.toString()}`);
    setAnnotations(await res.json());
    setLoading(false);
  };

  const handleDeleteAnnotation = async (id: number) => {
    await fetch(`/api/train/annotations/${id}`, { method: 'DELETE' });
    handleFetchAnnotations(search, page * pageSize);
  };

  const handleEditAnnotation = async (id: number, updates: Partial<Annotation>) => {
    await fetch(`/api/train/annotations/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    handleFetchAnnotations(search, page * pageSize);
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.length) return;
    setUploading(true);
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    await fetch('/api/train/annotations/upload', {
      method: 'POST',
      body: formData
    });
    setUploading(false);
    handleFetchAnnotations(search, page * pageSize);
  };

  const handleDownload = () => {
    window.open('/api/train/annotations/download', '_blank');
  };

  // Handler to fetch insights
  const handleFetchInsights = async () => {
    setLoading(true);
    const data = await fetchInsights();
    setInsights(data);
    setLoading(false);
  };

  return (
    <div className="training-dashboard" style={{ padding: 32, maxWidth: 800, margin: '0 auto' }}>
      <h1>Model Training Dashboard</h1>
      <div style={{ marginBottom: 24 }}>
        <h2>1. Start Training with Video Link</h2>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8 }}>
          <input
            type="url"
            placeholder="Paste field hockey video link..."
            value={videoLink}
            onChange={e => setVideoLink(e.target.value)}
            style={{ flex: 1, padding: 8 }}
            required
          />
          <button type="submit" disabled={loading} style={{ padding: '8px 16px' }}>
            {loading ? 'Starting...' : 'Start Training'}
          </button>
        </form>
      </div>
      <div style={{ marginBottom: 24 }}>
        <h2>2. View Trained Data</h2>
        <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
          <input
            type="text"
            placeholder="Search..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ flex: 1, padding: 8 }}
          />
          <button onClick={() => handleFetchAnnotations(search, 0)} disabled={loading}>
            {loading ? 'Loading...' : 'Search'}
          </button>
          <button onClick={handleDownload} style={{ marginLeft: 8 }}>
            Download JSON
          </button>
          <label style={{ marginLeft: 8 }}>
            <input type="file" accept="application/json" style={{ display: 'none' }} onChange={handleUpload} />
            <span style={{ cursor: 'pointer', color: uploading ? 'gray' : 'blue' }}>{uploading ? 'Uploading...' : 'Upload JSON'}</span>
          </label>
        </div>
        <ul>
          {annotations.map(a => (
            <li key={a.id} style={{ marginBottom: 8 }}>
              <a href={a.video} target="_blank" rel="noopener noreferrer">Video {a.id}</a> - Events: {a.events} - {a.description}
              <button onClick={() => handleDeleteAnnotation(a.id)} style={{ marginLeft: 8 }}>Delete</button>
              <button onClick={() => {
                const newDesc = prompt('Edit description:', a.description || '');
                if (newDesc !== null) handleEditAnnotation(a.id, { description: newDesc });
              }} style={{ marginLeft: 4 }}>Edit</button>
            </li>
          ))}
        </ul>
        <div style={{ marginTop: 8 }}>
          <button onClick={() => { setPage(p => Math.max(0, p - 1)); handleFetchAnnotations(search, Math.max(0, (page - 1) * pageSize)); }} disabled={page === 0}>Prev</button>
          <span style={{ margin: '0 8px' }}>Page {page + 1}</span>
          <button onClick={() => { setPage(p => p + 1); handleFetchAnnotations(search, (page + 1) * pageSize); }}>Next</button>
        </div>
      </div>
      <div>
        <h2>3. Get Insights</h2>
        <button onClick={handleFetchInsights} disabled={loading} style={{ marginBottom: 8 }}>
          {loading ? 'Loading...' : 'Get Insights'}
        </button>
        {insights && (
          <div style={{ marginTop: 8 }}>
            <div>Total Videos: {insights.totalVideos}</div>
            <div>Total Events: {insights.totalEvents}</div>
            <div>Most Common Event: {insights.mostCommonEvent}</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrainingDashboard;
