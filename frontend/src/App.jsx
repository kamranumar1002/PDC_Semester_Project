import React, { useState, useEffect } from 'react';
import { Activity, Zap, Clock, Server, Play, ArrowDownToLine } from 'lucide-react';
import FileUploader from './components/FileUploader';
import CoreVisualizer from './components/CoreVisualizer';
import MetricsChart from './components/MetricsChart';
import { uploadBatch, startExperiment, getExperimentStatus } from './api';

const App = () => {
  const [batch, setBatch] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Experiment States
  const [serialStatus, setSerialStatus] = useState('PENDING'); // PENDING, PROCESSING, COMPLETED
  const [parallelStatus, setParallelStatus] = useState('PENDING');
  
  const [serialData, setSerialData] = useState(null);
  const [parallelData, setParallelData] = useState(null);

  // Helper to handle upload
  const handleUpload = async (files) => {
    setLoading(true);
    try {
      const data = await uploadBatch(files);
      setBatch(data);
      // Reset experiments on new upload
      setSerialStatus('PENDING');
      setParallelStatus('PENDING');
      setSerialData(null);
      setParallelData(null);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Upload failed. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
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
      }, 1000); // Check every 1 second
      
    } catch (error) {
      console.error(error);
      setStatus('FAILED');
    }
  };

  // Calculate Speedup
  const speedup = (serialData?.duration_seconds && parallelData?.duration_seconds)
    ? (serialData.duration_seconds / parallelData.duration_seconds).toFixed(2)
    : null;

  return (
    <div className="min-h-screen bg-hpc-bg p-8 font-sans">
      {/* Header */}
      <header className="mb-10 border-b border-hpc-border pb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <Activity className="text-cyan-400" />
            PDC Audio Processor
          </h1>
          <p className="text-gray-400 mt-1">High-Performance Computing & Audio Analytics Dashboard</p>
        </div>
        <div className="flex gap-4">
            {batch && (
                <span className="bg-slate-800 px-4 py-2 rounded text-sm text-gray-300 font-mono">
                    Batch ID: {batch.id} | Files: {batch.files.length}
                </span>
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
            <section className="bg-hpc-panel p-6 rounded-lg border border-hpc-border">
              <h2 className="text-white font-semibold mb-4">Execution Control</h2>
              <div className="space-y-4">
                
                {/* Serial Button */}
                <div className="flex items-center justify-between p-3 bg-slate-800 rounded border border-slate-700">
                  <div className="flex flex-col">
                    <span className="text-cyan-400 font-bold">Serial Processing</span>
                    <span className="text-xs text-gray-500">Single Core Execution</span>
                  </div>
                  <button 
                    onClick={() => runExperiment('SERIAL')}
                    disabled={serialStatus === 'PROCESSING'}
                    className={`px-4 py-2 rounded font-bold text-sm transition-all ${
                      serialStatus === 'PROCESSING' ? 'bg-gray-600 cursor-not-allowed' : 'bg-cyan-600 hover:bg-cyan-500 text-white'
                    }`}
                  >
                    {serialStatus === 'PROCESSING' ? 'Running...' : 'START'}
                  </button>
                </div>

                {/* Parallel Button */}
                <div className="flex items-center justify-between p-3 bg-slate-800 rounded border border-slate-700">
                  <div className="flex flex-col">
                    <span className="text-emerald-400 font-bold">Parallel Processing</span>
                    <span className="text-xs text-gray-500">Multi-Core / Distributed</span>
                  </div>
                  <button 
                    onClick={() => runExperiment('PARALLEL')}
                    disabled={parallelStatus === 'PROCESSING'}
                    className={`px-4 py-2 rounded font-bold text-sm transition-all ${
                      parallelStatus === 'PROCESSING' ? 'bg-gray-600 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-500 text-white'
                    }`}
                  >
                    {parallelStatus === 'PROCESSING' ? 'Running...' : 'START'}
                  </button>
                </div>

              </div>
            </section>
          )}

          {/* Speedup Metric Highlight */}
          {speedup && (
            <div className="bg-gradient-to-r from-cyan-900 to-emerald-900 p-6 rounded-lg border border-cyan-700 text-center shadow-lg shadow-cyan-900/20">
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
             <div className="bg-hpc-panel border border-hpc-border p-4 rounded-lg flex flex-col justify-center space-y-4">
                <h3 className="text-white border-b border-gray-700 pb-2">Execution Stats</h3>
                
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
                        {speedup ? `${((speedup / 8) * 100).toFixed(1)}%` : '--'} (est. 8 cores)
                    </span>
                </div>
             </div>
          </div>

          {/* Results List (Preview) */}
          {/* Results List */}
          {(serialData || parallelData) && (
             <div className="bg-hpc-panel border border-hpc-border rounded-lg p-6 mb-10">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-white font-semibold">Processed Audio Output</h3>
                  <span className="text-xs text-gray-500 italic">
                    {parallelData?.results?.length || serialData?.results?.length} files processed
                  </span>
                </div>
                
                <div className="overflow-x-auto max-h-96 overflow-y-auto custom-scrollbar">
                    <table className="w-full text-sm text-left text-gray-400">
                        <thead className="text-xs text-gray-200 uppercase bg-slate-800 sticky top-0">
                            <tr>
                                <th className="px-4 py-3">File Name</th>
                                <th className="px-4 py-3">Time</th>
                                <th className="px-4 py-3 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {/* Display results from the most recently finished experiment */}
                            {(parallelData?.results || serialData?.results || []).map((res) => {
    
                              // 1. Construct the correct URL with /media/ prefix
                              // We remove any leading slashes from res.processed_file just in case
                              const cleanPath = res.processed_file.startsWith('/') ? res.processed_file.substring(1) : res.processed_file;
                              const fileUrl = cleanPath
                              return (
                                  <tr key={res.id} className="border-b border-gray-700 hover:bg-slate-800/50 transition-colors">
                                      <td className="px-4 py-3 font-medium text-white">
                                          {res.processed_file.split('/').pop()}
                                      </td>
                                      <td className="px-4 py-3 font-mono text-cyan-400">
                                          {res.processing_time_ms.toFixed(0)} ms
                                      </td>
                                      <td className="px-4 py-3 flex justify-end gap-3">
                                          {/* Play Button - Opens in new tab */}
                                          <a 
                                              href={fileUrl} 
                                              target="_blank"
                                              rel="noreferrer"
                                              className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs text-white flex items-center gap-1 transition-colors"
                                          >
                                              <Play size={12} /> Play
                                          </a>

                                          {/* Download Button */}
                                          <a 
                                              href={fileUrl} 
                                              download
                                              target="_blank"
                                              className="px-3 py-1 bg-emerald-700 hover:bg-emerald-600 rounded text-xs text-white flex items-center gap-1 transition-colors"
                                          >
                                              <ArrowDownToLine size={12} /> Save
                                          </a>
                                      </td>
                                  </tr>
                              );
                          })}
                        </tbody>
                    </table>
                </div>
             </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;