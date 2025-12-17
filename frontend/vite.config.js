/* eslint-disable no-undef */
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd()); 

  return {
    plugins: [react(), svgr()],
    
    server: {
      port: parseInt(env.VITE_DEV_PORT) || 5173, 
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_DEV_PORT_BASE_URL || 'http://localhost:8000', 
          changeOrigin: true, 
        },
      },
    },
  }
});