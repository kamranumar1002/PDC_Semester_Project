import React from 'react';
import { motion } from 'framer-motion';

const CoreVisualizer = ({ mode, status, coreCount = 8 }) => {
  // Determine how many cores are "active" based on mode
  const activeCores = status === 'PROCESSING' 
    ? (mode === 'PARALLEL' ? coreCount : 1) 
    : 0;

  return (
    <div className="bg-hpc-panel border border-hpc-border p-6 rounded-lg shadow-xl">
      <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-4 font-semibold">
        CPU Core Utilization Simulation
      </h3>
      
      <div className="grid grid-cols-4 gap-4">
        {Array.from({ length: coreCount }).map((_, i) => (
          <div key={i} className="flex flex-col items-center">
            <motion.div
              className={`w-12 h-12 rounded-md border-2 ${
                i < activeCores 
                  ? 'bg-cyan-900/50 border-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.5)]' 
                  : 'bg-slate-800 border-slate-700'
              }`}
              animate={i < activeCores ? { scale: [1, 1.1, 1] } : {}}
              transition={{ repeat: Infinity, duration: 0.8, delay: i * 0.1 }}
            >
              {i < activeCores && (
                <div className="w-full h-full flex items-center justify-center text-cyan-400 text-xs font-mono font-bold">
                  ACT
                </div>
              )}
            </motion.div>
            <span className="text-xs text-gray-500 mt-2 font-mono">Core {i}</span>
          </div>
        ))}
      </div>
      
      <div className="mt-4 flex justify-between text-xs text-gray-400 font-mono">
        <span>Mode: <span className="text-white">{mode || 'IDLE'}</span></span>
        <span>Active Threads: <span className="text-white">{activeCores}</span></span>
      </div>
    </div>
  );
};

export default CoreVisualizer;