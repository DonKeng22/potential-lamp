// API Configuration and Services for Field Hockey Platform
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api/v1' 
  : 'http://localhost:8000/api/v1';

// API Response Types
export interface Video {
  id: number;
  filename: string;
  original_name: string;
  status: string;
  file_size?: number;
  content_type?: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  task_id: string;
  status: string;
  progress: number;
  result?: any;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface Detection {
  id: number;
  video_id: number;
  frame_number: number;
  objects: any[];
  timestamp: number;
  created_at: string;
}

export interface Event {
  id: number;
  video_id: number;
  event_type: string;
  frame_number: number;
  timestamp: number;
  confidence: number;
  details: any;
  created_at: string;
}

// API Functions
export class ApiService {
  private static async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ 
        error: 'Request failed', 
        detail: response.statusText 
      }));
      throw new Error(error.detail || error.error || 'Request failed');
    }

    return response.json();
  }

  // Health Check
  static async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    // Use base URL without /api/v1 for health endpoint
    const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }

  // Video Management
  static async uploadVideo(file: File): Promise<{ id: number; filename: string; status: string; message: string }> {
    const formData = new FormData();
    formData.append('file', file);

    return this.request('/videos/upload', {
      method: 'POST',
      headers: {}, // Remove Content-Type header for FormData
      body: formData,
    });
  }

  static async getVideos(skip = 0, limit = 100, status?: string): Promise<{ videos: Video[]; count: number }> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    
    if (status) {
      params.append('status_filter', status);
    }

    return this.request(`/videos/?${params.toString()}`);
  }

  static async getVideo(videoId: number): Promise<Video> {
    return this.request(`/videos/${videoId}`);
  }

  static async processVideo(videoId: number, processType = 'analysis'): Promise<{ task_id: string; status: string; message: string }> {
    return this.request(`/videos/${videoId}/process`, {
      method: 'POST',
      body: JSON.stringify({ process_type: processType }),
    });
  }

  static async getVideoDetections(
    videoId: number, 
    frameStart?: number, 
    frameEnd?: number
  ): Promise<{ video_id: number; detections: Detection[] }> {
    const params = new URLSearchParams();
    if (frameStart !== undefined) params.append('frame_start', frameStart.toString());
    if (frameEnd !== undefined) params.append('frame_end', frameEnd.toString());

    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request(`/videos/${videoId}/detections${query}`);
  }

  static async getVideoEvents(
    videoId: number, 
    eventType?: string
  ): Promise<{ video_id: number; events: Event[] }> {
    const params = new URLSearchParams();
    if (eventType) params.append('event_type', eventType);

    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request(`/videos/${videoId}/events${query}`);
  }

  // Task Management
  static async getTaskStatus(taskId: string): Promise<Task> {
    return this.request(`/tasks/${taskId}`);
  }

  static async getTasks(
    skip = 0, 
    limit = 100, 
    status?: string, 
    taskType?: string
  ): Promise<{ tasks: Task[]; count: number }> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    
    if (status) params.append('status_filter', status);
    if (taskType) params.append('task_type', taskType);

    return this.request(`/tasks/?${params.toString()}`);
  }

  static async cancelTask(taskId: string): Promise<{ message: string }> {
    return this.request(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }
}
