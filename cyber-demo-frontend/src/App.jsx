import { useState, useEffect } from 'react'

function App() {
  const [url, setUrl] = useState('https://example.com')
  const [status, setStatus] = useState('idle') // idle, processing, completed, error
  const [taskId, setTaskId] = useState(null)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  // 1. Submit the task to the queue
  const handleScan = async (e) => {
    e.preventDefault()
    setStatus('processing')
    setError(null)
    setResults(null)
    setTaskId(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/scan/headers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
      })

      if (!response.ok) throw new Error("Failed to connect to the API.")
      
      const data = await response.json()
      // Save the task_id so we can poll for it
      setTaskId(data.task_id) 
    } catch (err) {
      setError(err.message)
      setStatus('error')
    }
  }

  // 2. The Polling Mechanism (Checks status every 2 seconds)
  useEffect(() => {
    let pollInterval;

    if (taskId && status === 'processing') {
      pollInterval = setInterval(async () => {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/v1/scan/status/${taskId}`)
          const data = await response.json()

          // If Celery says it is done, stop polling and show results!
          if (data.status === 'success') {
            setResults(data.results)
            setStatus('completed')
            clearInterval(pollInterval) 
          }
        } catch (err) {
          console.error(err)
          setError("Lost connection to the scanning engine.")
          setStatus('error')
          clearInterval(pollInterval)
        }
      }, 2000) // 2000 milliseconds = 2 seconds
    }

    return () => clearInterval(pollInterval) // Cleanup when done
  }, [taskId, status])

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', fontFamily: 'system-ui, sans-serif' }}>
      <h1 style={{ borderBottom: '2px solid #eee', paddingBottom: '10px' }}>
        Cybersecurity Automation Demo <span style={{fontSize: '0.5em', color: 'gray'}}>(Async Edition)</span>
      </h1>

      {/* Control Panel */}
      <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
        <form onSubmit={handleScan} style={{ display: 'flex', gap: '10px' }}>
          <input 
            type="url" 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            style={{ flex: 1, padding: '10px', fontSize: '16px', borderRadius: '4px', border: '1px solid #ccc' }}
          />
          <button 
            type="submit" 
            disabled={status === 'processing'}
            style={{ 
              padding: '10px 20px', 
              background: status === 'processing' ? '#ccc' : '#0d6efd', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px', 
              cursor: status === 'processing' ? 'not-allowed' : 'pointer' 
            }}
          >
            {status === 'processing' ? 'Adding to Queue...' : 'Run Async Scan'}
          </button>
        </form>
      </div>

      {/* Async Loading State */}
      {status === 'processing' && taskId && (
        <div style={{ padding: '20px', textAlign: 'center', background: '#e9ecef', borderRadius: '8px' }}>
          <h3 style={{ color: '#0d6efd', margin: 0 }}>Scan running in background...</h3>
          <p style={{ margin: '10px 0 0 0', color: '#6c757d' }}>Task ID: {taskId}</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div style={{ background: '#f8d7da', color: '#842029', padding: '15px', borderRadius: '8px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Results Table */}
      {status === 'completed' && results && results.status === "success" && (
        <div>
          <h3>Scan Results for {results.target}</h3>
          <p>Found <strong>{results.findings_count}</strong> missing configurations.</p>
          
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
            <thead>
              <tr style={{ background: '#333', color: 'white', textAlign: 'left' }}>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Finding</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Severity</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Remediation</th>
              </tr>
            </thead>
            <tbody>
              {results.findings.map((item, index) => (
                <tr key={index} style={{ background: index % 2 === 0 ? '#fff' : '#f9f9f9' }}>
                  <td style={{ padding: '12px', border: '1px solid #ddd', fontWeight: 'bold' }}>{item.finding}</td>
                  <td style={{ 
                    padding: '12px', 
                    border: '1px solid #ddd',
                    color: item.severity === 'High' ? 'red' : item.severity === 'Medium' ? 'orange' : 'green',
                    fontWeight: 'bold'
                  }}>
                    {item.severity}
                  </td>
                  <td style={{ padding: '12px', border: '1px solid #ddd' }}>{item.remediation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default App