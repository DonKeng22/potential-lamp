import React, { useState, useEffect, useCallback } from 'react';
import { ApiService, Task } from '../api';
import './TaskMonitor.css';

const TaskMonitor: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [typeFilter, setTypeFilter] = useState<string>('');
  const [currentPage, setCurrentPage] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [error, setError] = useState<string>('');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  const pageSize = 10;

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response = await ApiService.getTasks(
        currentPage * pageSize,
        pageSize,
        statusFilter || undefined,
        typeFilter || undefined
      );
      setTasks(response.tasks);
      setTotalCount(response.count);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }, [currentPage, statusFilter, typeFilter]);

  // Auto-refresh effect
  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(loadTasks, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, [autoRefresh, loadTasks]);

  const handleTaskSelect = async (taskId: string) => {
    try {
      const task = await ApiService.getTaskStatus(taskId);
      setSelectedTask(task);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load task details');
    }
  };

  const handleCancelTask = async (taskId: string) => {
    try {
      await ApiService.cancelTask(taskId);
      setSelectedTask(null);
      await loadTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to cancel task');
    }
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString();
  };

  const getStatusColor = (status: string): string => {
    switch (status.toLowerCase()) {
      case 'pending': return '#f39c12';
      case 'queued': return '#3498db';
      case 'running': return '#9b59b6';
      case 'completed': return '#27ae60';
      case 'failed': return '#e74c3c';
      case 'cancelled': return '#95a5a6';
      default: return '#95a5a6';
    }
  };

  const getStatusIcon = (status: string): string => {
    switch (status.toLowerCase()) {
      case 'pending': return '⏳';
      case 'queued': return '📋';
      case 'running': return '⚙️';
      case 'completed': return '✅';
      case 'failed': return '❌';
      case 'cancelled': return '🚫';
      default: return '❓';
    }
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <div className="task-monitor">
      <div className="section">
        <div className="section-header">
          <h2>⚙️ Task Monitor</h2>
          <div className="controls">
            <label className="auto-refresh-toggle">
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
              />
              Auto-refresh (5s)
            </label>
            
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setCurrentPage(0);
              }}
              className="filter-select"
            >
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="queued">Queued</option>
              <option value="running">Running</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
              <option value="cancelled">Cancelled</option>
            </select>

            <select
              value={typeFilter}
              onChange={(e) => {
                setTypeFilter(e.target.value);
                setCurrentPage(0);
              }}
              className="filter-select"
            >
              <option value="">All Types</option>
              <option value="analysis">Analysis</option>
              <option value="annotation">Annotation</option>
              <option value="training">Training</option>
            </select>

            <button onClick={loadTasks} disabled={loading} className="refresh-btn">
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
            Loading tasks...
          </div>
        )}

        {!loading && tasks.length === 0 && (
          <div className="empty-state">
            <p>📭 No tasks found. Process a video to see tasks here!</p>
          </div>
        )}

        {!loading && tasks.length > 0 && (
          <div className="task-grid">
            {tasks.map((task) => (
              <div 
                key={task.task_id} 
                className={`task-card ${selectedTask?.task_id === task.task_id ? 'selected' : ''}`}
                onClick={() => handleTaskSelect(task.task_id)}
              >
                <div className="task-header">
                  <div className="task-id">
                    {getStatusIcon(task.status)} {task.task_id.slice(0, 8)}...
                  </div>
                  <span
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(task.status) }}
                  >
                    {task.status}
                  </span>
                </div>

                <div className="task-progress">
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${task.progress}%`,
                        backgroundColor: getStatusColor(task.status),
                      }}
                    ></div>
                  </div>
                  <span className="progress-text">{task.progress.toFixed(1)}%</span>
                </div>

                <div className="task-details">
                  <p><strong>Created:</strong> {formatDate(task.created_at)}</p>
                  <p><strong>Updated:</strong> {formatDate(task.updated_at)}</p>
                  {task.error_message && (
                    <p className="error-text">
                      <strong>Error:</strong> {task.error_message}
                    </p>
                  )}
                </div>

                {task.status === 'running' && (
                  <button
                    className="cancel-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCancelTask(task.task_id);
                    }}
                  >
                    🚫 Cancel
                  </button>
                )}
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
              Page {currentPage + 1} of {totalPages} ({totalCount} total tasks)
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

      {selectedTask && (
        <div className="section">
          <div className="section-header">
            <h3>📋 Task Details: {selectedTask.task_id.slice(0, 8)}...</h3>
            <button
              onClick={() => setSelectedTask(null)}
              className="close-btn"
            >
              ✖️ Close
            </button>
          </div>

          <div className="task-details-full">
            <div className="detail-row">
              <strong>Task ID:</strong> 
              <code>{selectedTask.task_id}</code>
            </div>
            <div className="detail-row">
              <strong>Status:</strong>
              <span
                className="status-badge"
                style={{ backgroundColor: getStatusColor(selectedTask.status) }}
              >
                {getStatusIcon(selectedTask.status)} {selectedTask.status}
              </span>
            </div>
            <div className="detail-row">
              <strong>Progress:</strong>
              <div className="progress-container">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{
                      width: `${selectedTask.progress}%`,
                      backgroundColor: getStatusColor(selectedTask.status),
                    }}
                  ></div>
                </div>
                <span>{selectedTask.progress.toFixed(1)}%</span>
              </div>
            </div>
            <div className="detail-row">
              <strong>Created:</strong>
              <span>{formatDate(selectedTask.created_at)}</span>
            </div>
            <div className="detail-row">
              <strong>Last Updated:</strong>
              <span>{formatDate(selectedTask.updated_at)}</span>
            </div>

            {selectedTask.result && (
              <div className="detail-section">
                <strong>Result:</strong>
                <pre className="result-json">
                  {JSON.stringify(selectedTask.result, null, 2)}
                </pre>
              </div>
            )}

            {selectedTask.error_message && (
              <div className="detail-section">
                <strong>Error Message:</strong>
                <div className="error-detail">
                  {selectedTask.error_message}
                </div>
              </div>
            )}

            {selectedTask.status === 'running' && (
              <div className="task-actions">
                <button
                  className="cancel-btn"
                  onClick={() => handleCancelTask(selectedTask.task_id)}
                >
                  🚫 Cancel Task
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskMonitor;