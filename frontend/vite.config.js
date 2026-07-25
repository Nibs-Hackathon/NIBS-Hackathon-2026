import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://nibs-hackathon-2026-production.up.railway.app',
        changeOrigin: true,
      },
      '/ws': {
        target: 'wss://nibs-hackathon-2026-production.up.railway.app',
        ws: true,
        changeOrigin: true,
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  }
})