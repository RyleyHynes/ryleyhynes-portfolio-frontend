import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { viteCommonjs } from '@originjs/vite-plugin-commonjs'
import path from 'path'

export default defineConfig({
  base: '/',
  build: {
    manifest: true,
  },
  css: {
    preprocessorOptions: {
      scss: {
        // Add global SCSS imports here if needed
      },
    },
  },
  plugins: [react(), viteCommonjs()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@assets': path.resolve(__dirname, 'src/assets'),
      '@components': path.resolve(__dirname, 'src/components'),
    },
  },
  preview: {
    port: 3000,
  },
  server: {
    port: 3000,
    open: true,
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      include: ['src/**'],
      exclude: ['src/stories/**', 'src/components/archived/**', 'src/main.tsx'],
      provider: 'istanbul',
      reporter: ['html', 'json-summary', 'json'],
      thresholds: {
        lines: 80,
        branches: 70,
        functions: 80,
        statements: 80,
      }
    },
  },
})
