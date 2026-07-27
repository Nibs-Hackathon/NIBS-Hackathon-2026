import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const apiTarget = process.env.VITE_API_PROXY || 'http://127.0.0.1:8080';
const wsTarget = process.env.VITE_WS_PROXY || 'ws://127.0.0.1:8080';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true,
      },
      '/ws': {
        target: wsTarget,
        ws: true,
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    // Epic 6 performance budget — warn above this; prefer route chunks under ~150kb gzip
    chunkSizeWarningLimit: 450,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return undefined;
          if (id.includes('react-dom') || id.includes('/react/') || id.includes('react-router')) {
            return 'vendor-react';
          }
          if (id.includes('@mui') || id.includes('@emotion')) {
            return 'vendor-mui';
          }
          if (id.includes('motion') || id.includes('animejs')) {
            return 'vendor-motion';
          }
          if (id.includes('axios') || id.includes('react-hot-toast')) {
            return 'vendor-utils';
          }
          return 'vendor';
        },
      },
    },
  },
})
