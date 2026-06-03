/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50:  '#eef2ff',
          100: '#dce5fd',
          200: '#b8cafb',
          300: '#849ef7',
          400: '#5a76f0',
          500: '#3b51e8',
          600: '#2a3ad5',
          700: '#232cb0',
          800: '#1e2589',
          900: '#1a1f6e',
          950: '#0f1244',
        },
        accent: {
          50:  '#fefce8',
          100: '#fef9c3',
          200: '#fdf08a',
          300: '#fce351',
          400: '#f9d326',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        },
        surface: {
          light: '#f8f9fb',
          card:  '#ffffff',
          dark:  '#111827',
        },
        chart: {
          blue:   '#3b82f6',
          green:  '#22c55e',
          red:    '#ef4444',
          orange: '#f97316',
          purple: '#a855f7',
          teal:   '#14b8a6',
        },
      },
      fontFamily: {
        sans: ['"Noto Sans SC"', '"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
        display: ['"Playfair Display"', 'Georgia', 'serif'],
      },
      spacing: {
        'sidebar': '240px',
        'toc':     '220px',
        'content': '720px',
      },
      borderRadius: {
        'card': '0.75rem',
      },
      boxShadow: {
        'card':  '0 1px 3px 0 rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.06)',
        'card-hover': '0 4px 12px 0 rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.06)',
        'nav': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            'h1, h2, h3, h4': {
              color: 'inherit',
              fontWeight: '600',
            },
            'code::before': { content: 'none' },
            'code::after':  { content: 'none' },
            'blockquote': {
              borderLeftColor: '#eab308',
              backgroundColor: 'rgb(254 252 232 / 0.5)',
              fontWeight: 'normal',
            },
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};