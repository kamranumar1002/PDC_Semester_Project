/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        hpc: {
          bg: '#0f172a',       // Deep slate background
          panel: '#1e293b',    // Lighter panel
          accent: '#06b6d4',   // Cyan (Serial)
          success: '#10b981',  // Green (Parallel)
          border: '#334155',
        }
      },
      animation: {
        'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}