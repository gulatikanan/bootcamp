import threading
import time
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional

from metrics.metrics_store import MetricsStore

class Dashboard:
    """Web dashboard for system observability."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize the dashboard server.
        
        Args:
            host: Host to bind the server to
            port: Port to bind the server to
        """
        self.host = host
        self.port = port
        self.app = FastAPI(title="Stream Processing Dashboard")
        self.metrics_store = MetricsStore()
        self.server_thread = None
        self.setup_routes()
    
    def setup_routes(self):
        """Set up the FastAPI routes."""
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @self.app.get("/stats", response_model=Dict[str, Any])
        async def get_stats():
            """Get processor metrics."""
            return {
                "processors": self.metrics_store.get_metrics(),
                "timestamp": time.time()
            }
        
        @self.app.get("/trace", response_model=List[Dict[str, Any]])
        async def get_traces(limit: int = 100):
            """Get recent traces."""
            return self.metrics_store.get_traces(limit)
        
        @self.app.get("/errors", response_model=List[Dict[str, Any]])
        async def get_errors(limit: int = 100):
            """Get recent errors."""
            return self.metrics_store.get_errors(limit)
        
        @self.app.get("/files", response_model=Dict[str, Any])
        async def get_file_stats():
            """Get file processing statistics."""
            return self.metrics_store.get_file_stats()
        
        @self.app.get("/", response_class=HTMLResponse)
        async def get_dashboard():
            """Render the dashboard HTML."""
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Stream Processing Dashboard</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdn.tailwindcss.com"></script>
                <script>
                    // Refresh data every 2 seconds
                    function refreshData() {
                        fetchStats();
                        fetchTraces();
                        fetchErrors();
                        fetchFiles();
                        setTimeout(refreshData, 2000);
                    }
                    
                    async function fetchStats() {
                        const response = await fetch('/stats');
                        const data = await response.json();
                        const statsDiv = document.getElementById('stats');
                        
                        let html = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">';
                        
                        for (const [id, metrics] of Object.entries(data.processors)) {
                            html += `
                                <div class="bg-white p-4 rounded shadow">
                                    <h3 class="text-lg font-semibold">${id} (${metrics.type})</h3>
                                    <div class="mt-2 space-y-1">
                                        <p>Lines In: <span class="font-mono">${metrics.lines_in}</span></p>
                                        <p>Lines Out: <span class="font-mono">${metrics.lines_out}</span></p>
                                        <p>Processing Time: <span class="font-mono">${metrics.processing_time.toFixed(4)}s</span></p>
                                        <p>Errors: <span class="font-mono">${metrics.error_count}</span></p>
                                    </div>
                                </div>
                            `;
                        }
                        
                        html += '</div>';
                        statsDiv.innerHTML = html;
                    }
                    
                    async function fetchTraces() {
                        const response = await fetch('/trace');
                        const data = await response.json();
                        const tracesDiv = document.getElementById('traces');
                        
                        if (data.length === 0) {
                            tracesDiv.innerHTML = '<p class="text-gray-500">No traces available. Enable tracing with --trace flag.</p>';
                            return;
                        }
                        
                        let html = '<div class="space-y-4">';
                        
                        // Show only the last 10 traces
                        const recentTraces = data.slice(-10).reverse();
                        
                        for (const trace of recentTraces) {
                            html += `
                                <div class="bg-white p-4 rounded shadow">
                                    <h3 class="text-sm font-mono">${trace.line_id}</h3>
                                    <p class="text-sm text-gray-600 mt-1">${trace.original_line}</p>
                                    <div class="mt-2">
                                        <h4 class="text-xs text-gray-500">Path:</h4>
                                        <div class="flex flex-wrap items-center mt-1">
                            `;
                            
                            for (let i = 0; i < trace.path.length; i++) {
                                const step = trace.path[i];
                                const statusColor = step.status === 'error' ? 'bg-red-100 text-red-800' : 
                                                  step.status === 'drop' ? 'bg-yellow-100 text-yellow-800' : 
                                                  'bg-blue-100 text-blue-800';
                                
                                html += `
                                    <span class="text-xs ${statusColor} px-2 py-1 rounded mr-1 mb-1">
                                        ${step.processor_id}:${step.status}
                                    </span>
                                `;
                                
                                if (i < trace.path.length - 1) {
                                    html += `<span class="text-gray-400 mx-1">→</span>`;
                                }
                            }
                            
                            html += `
                                        </div>
                                    </div>
                                </div>
                            `;
                        }
                        
                        html += '</div>';
                        tracesDiv.innerHTML = html;
                    }
                    
                    async function fetchErrors() {
                        const response = await fetch('/errors');
                        const data = await response.json();
                        const errorsDiv = document.getElementById('errors');
                        
                        if (data.length === 0) {
                            errorsDiv.innerHTML = '<p class="text-gray-500">No errors recorded.</p>';
                            return;
                        }
                        
                        let html = '<div class="space-y-2">';
                        
                        // Show only the last 10 errors
                        const recentErrors = data.slice(-10).reverse();
                        
                        for (const error of recentErrors) {
                            const timestamp = new Date(error.timestamp * 1000).toLocaleTimeString();
                            
                            html += `
                                <div class="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                                    <div class="flex justify-between">
                                        <p class="text-sm font-semibold">${error.processor_id}</p>
                                        <p class="text-xs text-gray-500">${timestamp}</p>
                                    </div>
                                    <p class="text-sm mt-1">${error.message}</p>
                                </div>
                            `;
                        }
                        
                        html += '</div>';
                        errorsDiv.innerHTML = html;
                    }
                    
                    async function fetchFiles() {
                        const response = await fetch('/files');
                        const data = await response.json();
                        const filesDiv = document.getElementById('files');
                        
                        let html = `
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                                <div class="bg-white p-4 rounded shadow">
                                    <h3 class="text-lg font-semibold">Unprocessed</h3>
                                    <p class="text-2xl font-bold mt-2">${data.unprocessed}</p>
                                </div>
                                <div class="bg-white p-4 rounded shadow">
                                    <h3 class="text-lg font-semibold">Under Process</h3>
                                    <p class="text-2xl font-bold mt-2">${data.underprocess}</p>
                                </div>
                                <div class="bg-white p-4 rounded shadow">
                                    <h3 class="text-lg font-semibold">Processed</h3>
                                    <p class="text-2xl font-bold mt-2">${data.processed}</p>
                                </div>
                            </div>
                        `;
                        
                        if (data.current_file) {
                            html += `
                                <div class="bg-blue-50 p-4 rounded shadow mb-4">
                                    <h3 class="text-lg font-semibold">Currently Processing</h3>
                                    <p class="text-xl mt-2">${data.current_file}</p>
                                </div>
                            `;
                        }
                        
                        if (data.recent_files && data.recent_files.length > 0) {
                            html += `
                                <div class="bg-white p-4 rounded shadow">
                                    <h3 class="text-lg font-semibold">Recently Processed Files</h3>
                                    <div class="mt-2 space-y-2">
                            `;
                            
                            for (const file of data.recent_files) {
                                const timestamp = new Date(file.timestamp * 1000).toLocaleString();
                                html += `
                                    <div class="border-b pb-2">
                                        <p class="font-medium">${file.filename}</p>
                                        <p class="text-xs text-gray-500">${timestamp}</p>
                                    </div>
                                `;
                            }
                            
                            html += `
                                    </div>
                                </div>
                            `;
                        }
                        
                        filesDiv.innerHTML = html;
                    }
                    
                    // Start refreshing data when the page loads
                    window.onload = refreshData;
                </script>
            </head>
            <body class="bg-gray-100 min-h-screen">
                <div class="container mx-auto px-4 py-8">
                    <h1 class="text-2xl font-bold mb-6">Stream Processing Dashboard</h1>
                    
                    <div class="mb-8">
                        <h2 class="text-xl font-semibold mb-4">File Processing Status</h2>
                        <div id="files" class="animate-pulse">
                            <p class="text-gray-500">Loading file statistics...</p>
                        </div>
                    </div>
                    
                    <div class="mb-8">
                        <h2 class="text-xl font-semibold mb-4">Processor Metrics</h2>
                        <div id="stats" class="animate-pulse">
                            <p class="text-gray-500">Loading processor metrics...</p>
                        </div>
                    </div>
                    
                    <div class="mb-8">
                        <h2 class="text-xl font-semibold mb-4">Recent Traces</h2>
                        <div id="traces" class="animate-pulse">
                            <p class="text-gray-500">Loading traces...</p>
                        </div>
                    </div>
                    
                    <div class="mb-8">
                        <h2 class="text-xl font-semibold mb-4">Recent Errors</h2>
                        <div id="errors" class="animate-pulse">
                            <p class="text-gray-500">Loading errors...</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
    
    def start(self):
        """Start the dashboard server in a background thread."""
        if self.server_thread is not None and self.server_thread.is_alive():
            return  # Already running
        
        def run_server():
            uvicorn.run(self.app, host=self.host, port=self.port)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        print(f"Dashboard started at http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the dashboard server."""
        # uvicorn doesn't provide a clean way to stop from another thread
        # In a real application, you might want to use a more sophisticated approach
        pass