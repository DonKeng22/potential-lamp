import React, { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import TrainingDashboard from './TrainingDashboard'
import AnnotatePage from './AnnotatePage'

function App() {
  const [count, setCount] = useState(0)
  const [page, setPage] = useState<'dashboard' | 'annotate'>('dashboard');

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <nav style={{ display: 'flex', gap: 16, padding: 16, background: '#222', color: '#fff' }}>
        <button onClick={() => setPage('dashboard')} style={{ color: page === 'dashboard' ? '#61dafb' : '#fff', background: 'none', border: 'none', fontSize: 18, cursor: 'pointer' }}>Dashboard</button>
        <button onClick={() => setPage('annotate')} style={{ color: page === 'annotate' ? '#61dafb' : '#fff', background: 'none', border: 'none', fontSize: 18, cursor: 'pointer' }}>Annotate</button>
      </nav>
      {page === 'dashboard' && <TrainingDashboard />}
      {page === 'annotate' && <AnnotatePage />}
    </>
  )
}

export default App
