import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      colors: {
        brand: {
          50: '#eef8ff',
          100: '#d7edff',
          200: '#b5ddff',
          300: '#84c6ff',
          400: '#4aa8ff',
          500: '#1f85ff',  // light mode link color
          600: '#3b9eff',  // brighter for dark backgrounds
          700: '#60adff',
          800: '#8ec3ff',
          900: '#b8d7ff',
        },
      },
      boxShadow: {
        soft: '0 10px 30px rgba(0,0,0,.08)',
      },
    },
  },
  plugins: [],
} satisfies Config
