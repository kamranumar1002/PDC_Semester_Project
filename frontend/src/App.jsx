import React, { useState, useEffect } from 'react';
import { Activity, Zap, Server, Play, ArrowDownToLine, FileAudio, BarChart2, RefreshCw, Trash2, Check, Clock } from 'lucide-react';
import FileUploader from './components/FileUploader';
import CoreVisualizer from './components/CoreVisualizer';
import MetricsChart from './components/MetricsChart';
import { uploadBatch, startExperiment, getExperimentStatus } from './api';

// --- Sub-Component: Result Card (Handles A/B Audio Comparison) ---
const AudioResultCard = ({ result }) => {
  // Helper to ensure URLs are absolute
  const getUrl = (path) => {
    if (!path) return '';
    // If it's already a full URL, return it
    if (path.startsWith('http')) return path;
    // Otherwise construct it (adjust port if needed)
    const cleanPath = path.startsWith('/') ? path.substring(1) : path;
    return `http://127.0.0.1:8000/media/${cleanPath}`; 
    // Note: If you updated your serializer to use_url=True, the backend might 
    // already be sending the full URL. This helper handles both cases safely.
  };

  const processedUrl = getUrl(result.processed_file);
  const originalUrl = getUrl(result.original_file_url); 

  const fileName = result.processed_file.split('/').pop();

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 transition-all hover:border-slate-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
        
        {/* File Info */}
        <div className="flex items-center gap-3">
          <div className="bg-cyan-900/30 p-2 rounded text-cyan-400">
            <FileAudio size={20} />
          </div>
          <div>
            <h4 className="text-white font-medium text-sm truncate max-w-[200px]" title={fileName}>
              {fileName}
            </h4>
            <span className="text-xs text-emerald-400 font-mono">
              Process Time: {result.processing_time_ms.toFixed(1)}ms
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <a 
            href={processedUrl}
            download
            target="_blank"
            rel="noreferrer"
            className="p-2 bg-slate-700 hover:bg-emerald-600 text-white rounded transition-colors"
            title="Download Result"
          >
            <ArrowDownToLine size={16} />
          </a>
        </div>
      </div>

      {/* A/B Comparison Players */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900/50 p-3 rounded-lg border border-slate-700/50">
        <div>
          <span className="text-[10px] uppercase tracking-wider text-gray-500 font-bold mb-1 block">Original Input</span>
          <audio controls src={originalUrl} className="w-full h-8 block" />
        </div>
        <div>
          <span className="text-[10px] uppercase tracking-wider text-emerald-500 font-bold mb-1 block">Processed Output</span>
          <audio controls src={processedUrl} className="w-full h-8 block" />
        </div>
      </div>
    </div>
  );
};


// --- Main Component ---
const App = () => {
  const [batch, setBatch] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Experiment States
  const [serialStatus, setSerialStatus] = useState('PENDING'); 
  const [parallelStatus, setParallelStatus] = useState('PENDING');
  
  const [serialData, setSerialData] = useState(null);
  const [parallelData, setParallelData] = useState(null);

  // --- Feature 1: Session Persistence ---
  useEffect(() => {
    // On Load: Check if we have a batch in LocalStorage
    const savedBatch = localStorage.getItem('pdc_batch');
    if (savedBatch) {
      try {
        const parsedBatch = JSON.parse(savedBatch);
        setBatch(parsedBatch);
        console.log("Restored session for batch:", parsedBatch.id);
      } catch (e) {
        console.error("Failed to restore session", e);
        localStorage.removeItem('pdc_batch');
      }
    }
  }, []);

  // Helper to handle upload
  const handleUpload = async (files) => {
    setLoading(true);
    try {
      const data = await uploadBatch(files);
      setBatch(data);
      // Save to LocalStorage
      localStorage.setItem('pdc_batch', JSON.stringify(data));
      
      // Reset experiments on new upload
      resetExperiments();
    } catch (error) {
      console.error("Upload failed", error);
      alert("Upload failed. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const resetExperiments = () => {
    setSerialStatus('PENDING');
    setParallelStatus('PENDING');
    setSerialData(null);
    setParallelData(null);
  };

  const clearSession = () => {
    localStorage.removeItem('pdc_batch');
    setBatch(null);
    resetExperiments();
  };

  // Helper to trigger processing
  const runExperiment = async (mode) => {
    if (!batch) return;
    
    const setStatus = mode === 'SERIAL' ? setSerialStatus : setParallelStatus;
    const setData = mode === 'SERIAL' ? setSerialData : setParallelData;
    
    setStatus('PROCESSING');
    
    try {
      const startRes = await startExperiment(batch.id, mode);
      const experimentId = startRes.id;
      
      // Polling logic
      const interval = setInterval(async () => {
        const statusRes = await getExperimentStatus(experimentId);
        
        if (statusRes.status === 'COMPLETED' || statusRes.status === 'FAILED') {
          clearInterval(interval);
          setStatus(statusRes.status);
          setData(statusRes);
        }
      }, 1000); 
      
    } catch (error) {
      console.error(error);
      setStatus('FAILED');
    }
  };

  // Calculate Speedup
  const speedup = (serialData?.duration_seconds && parallelData?.duration_seconds)
    ? (serialData.duration_seconds / parallelData.duration_seconds).toFixed(2)
    : null;

  // Determine which results to show (prefer parallel, fallback to serial)
  const resultsToShow = parallelData?.results || serialData?.results || [];

  return (
    <div className="min-h-screen bg-hpc-bg p-8 font-sans text-gray-200">
      {/* Header */}
      <header className="mb-10 border-b border-hpc-border pb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <Activity className="text-cyan-400" />
            PDC Audio Processor
          </h1>
          <p className="text-gray-400 mt-1">High-Performance Computing & Audio Analytics Dashboard</p>
        </div>
        <div className="flex gap-4 items-center">
            {batch && (
              <div className="flex items-center gap-3 bg-slate-800 px-4 py-2 rounded-lg border border-slate-700">
                 <div className="text-sm">
                    <span className="block text-gray-500 text-[10px] uppercase font-bold">Current Session</span>
                    <span className="font-mono text-white">Batch #{batch.id}</span>
                 </div>
                 <div className="h-8 w-px bg-slate-600 mx-1"></div>
                 <button 
                    onClick={clearSession}
                    className="text-gray-400 hover:text-red-400 transition-colors p-1"
                    title="Clear Session"
                 >
                    <Trash2 size={16} />
                 </button>
              </div>
            )}
        </div>
      </header>

      {/* Main Grid */}
      <main className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Controls & Upload */}
        <div className="lg:col-span-4 space-y-6">
          <section>
            <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
              <Server size={18} /> Input Data
            </h2>
            <FileUploader onUpload={handleUpload} isUploading={loading} />
          </section>

          {batch && (
            <section className="bg-hpc-panel p-6 rounded-lg border border-hpc-border shadow-lg">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-white font-semibold">Execution Control</h2>
                <button onClick={resetExperiments} className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1">
                   <RefreshCw size={12} /> Reset Runs
                </button>
              </div>
              
              <div className="space-y-4">
                
                {/* Serial Button */}
                <div className={`flex items-center justify-between p-3 rounded border transition-all ${
                    serialStatus === 'COMPLETED' ? 'bg-cyan-900/20 border-cyan-500/50' : 'bg-slate-800 border-slate-700'
                }`}>
                  <div className="flex flex-col">
                    <span className="text-cyan-400 font-bold">Serial Processing</span>
                    <span className="text-xs text-gray-500">Single Core Execution</span>
                  </div>
                  <button 
                    onClick={() => runExperiment('SERIAL')}
                    disabled={serialStatus === 'PROCESSING'}
                    className={`px-4 py-2 rounded font-bold text-sm transition-all min-w-[100px] ${
                      serialStatus === 'PROCESSING' 
                        ? 'bg-gray-600 cursor-wait' 
                        : serialStatus === 'COMPLETED'
                          ? 'bg-slate-700 text-cyan-400 border border-cyan-400' 
                          : 'bg-cyan-600 hover:bg-cyan-500 text-white'
                    }`}
                  >
                    {serialStatus === 'PROCESSING' ? 'Running...' : (serialStatus === 'COMPLETED' ? 'Done' : 'START')}
                  </button>
                </div>

                {/* Parallel Button */}
                <div className={`flex items-center justify-between p-3 rounded border transition-all ${
                    parallelStatus === 'COMPLETED' ? 'bg-emerald-900/20 border-emerald-500/50' : 'bg-slate-800 border-slate-700'
                }`}>
                  <div className="flex flex-col">
                    <span className="text-emerald-400 font-bold">Parallel Processing</span>
                    <span className="text-xs text-gray-500">Multi-Core / Distributed</span>
                  </div>
                  <button 
                    onClick={() => runExperiment('PARALLEL')}
                    disabled={parallelStatus === 'PROCESSING'}
                    className={`px-4 py-2 rounded font-bold text-sm transition-all min-w-[100px] ${
                      parallelStatus === 'PROCESSING' 
                        ? 'bg-gray-600 cursor-wait' 
                        : parallelStatus === 'COMPLETED'
                          ? 'bg-slate-700 text-emerald-400 border border-emerald-400' 
                          : 'bg-emerald-600 hover:bg-emerald-500 text-white'
                    }`}
                  >
                    {parallelStatus === 'PROCESSING' ? 'Running...' : (parallelStatus === 'COMPLETED' ? 'Done' : 'START')}
                  </button>
                </div>

              </div>
            </section>
          )}

          {/* Speedup Metric Highlight */}
          {speedup && (
            <div className="bg-gradient-to-r from-cyan-900 to-emerald-900 p-6 rounded-lg border border-cyan-700 text-center shadow-lg shadow-cyan-900/20 animate-in zoom-in duration-500">
              <h3 className="text-gray-300 uppercase text-xs font-bold tracking-widest mb-2">Speedup Factor</h3>
              <div className="text-5xl font-black text-white flex items-center justify-center gap-2">
                <Zap className="text-yellow-400 fill-yellow-400" size={32} />
                {speedup}x
              </div>
              <p className="text-xs text-cyan-200 mt-2">Parallel is {speedup} times faster than Serial</p>
            </div>
          )}
        </div>

        {/* Right Column: Visualization & Results */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Core Visualizer */}
          <CoreVisualizer 
            mode={serialStatus === 'PROCESSING' ? 'SERIAL' : (parallelStatus === 'PROCESSING' ? 'PARALLEL' : 'IDLE')}
            status={serialStatus === 'PROCESSING' || parallelStatus === 'PROCESSING' ? 'PROCESSING' : 'IDLE'} 
          />

          {/* Analytics Charts */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-64">
             <MetricsChart 
                serialTime={serialData?.duration_seconds} 
                parallelTime={parallelData?.duration_seconds} 
             />
             
             {/* Text Stats Panel */}
             <div className="bg-hpc-panel border border-hpc-border p-4 rounded-lg flex flex-col justify-center space-y-4 shadow-lg">
                <h3 className="text-white border-b border-gray-700 pb-2 font-bold flex items-center gap-2">
                   <Clock size={16} /> Execution Stats
                </h3>
                
                <div className="flex justify-between items-center">
                    <span className="text-gray-400 text-sm">Serial Time:</span>
                    <span className="text-cyan-400 font-mono text-xl">
                        {serialData ? `${serialData.duration_seconds.toFixed(3)}s` : '--'}
                    </span>
                </div>
                
                <div className="flex justify-between items-center">
                    <span className="text-gray-400 text-sm">Parallel Time:</span>
                    <span className="text-emerald-400 font-mono text-xl">
                        {parallelData ? `${parallelData.duration_seconds.toFixed(3)}s` : '--'}
                    </span>
                </div>

                <div className="flex justify-between items-center pt-2 border-t border-gray-700">
                    <span className="text-gray-400 text-sm">Efficiency:</span>
                    <span className="text-white font-mono">
                        {speedup ? `${((speedup / 8) * 100).toFixed(1)}%` : '--'} 
                        <span className="text-[10px] text-gray-500 ml-1">(est. 8 cores)</span>
                    </span>
                </div>
             </div>
          </div>

          {/* Feature 2 & 3: Enhanced Results List */}
          {resultsToShow.length > 0 && (
             <div className="bg-hpc-panel border border-hpc-border rounded-lg p-6 mb-10 shadow-xl">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-white font-semibold flex items-center gap-2">
                    <FileAudio size={18} /> Processed Audio Output
                  </h3>
                  <span className="text-xs text-gray-500 italic px-2 py-1 bg-slate-900 rounded">
                    {resultsToShow.length} results
                  </span>
                </div>
                
                {/* Replaced Table with Card Grid for better Spectrogram/Audio layout */}
                <div className="grid grid-cols-1 gap-4 max-h-[600px] overflow-y-auto custom-scrollbar pr-2">
                    {resultsToShow.map((res) => (
                        <AudioResultCard key={res.id} result={res} />
                    ))}
                </div>
             </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;