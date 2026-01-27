// tailwind.config.js
// Ubica este archivo en /frontend/tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
    // Busca clases dentro de tu carpeta src (app router y componentes)
    content: [
      './src/app/**/*.{js,ts,jsx,tsx}',
      './src/components/**/*.{js,ts,jsx,tsx}'
    ],
    theme: {
      extend: {
        colors: {
          primary: {
            DEFAULT: '#4773A1',
            light: '#6A90B4',
            lighter: '#8DADC7',
            subtle: '#B1CADA'
          },
          neutral: {
            bg: '#FCFCFC',
            lighter: '#F9FAFB',
            800: '#1F2937'
          },
          error: {
            DEFAULT: '#DC2626'
          },
          success: {
            DEFAULT: '#16A34A'
          },
          warning: {
            DEFAULT: '#D97706'
          },
          info: {
            DEFAULT: '#0EA5E9'
          }
        },
        spacing: {
          '1': '4px',
          '2': '8px',
          '3': '12px',
          '4': '16px',
          '6': '24px',
          '8': '32px',
          '10': '40px',
          '12': '48px',
          '16': '64px'
        },
        borderRadius: {
          sm: '0.25rem',
          md: '0.5rem',
          lg: '0.75rem',
          full: '9999px'
        },
        boxShadow: {
          sm: '0 1px 2px rgba(0,0,0,0.05)',
          md: '0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)',
          lg: '0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)',
          inner: 'inset 0 2px 4px rgba(0,0,0,0.06)'
        },
        fontFamily: {
          sans: ['Inter', 'sans-serif'],
          heading: ['Rubik', 'sans-serif']
        },
        fontSize: {
          sm: ['0.875rem', '1.25rem'],
          base: ['1rem', '1.5rem'],
          lg: ['1.125rem', '1.75rem'],
          xl: ['1.25rem', '1.75rem'],
          '2xl': ['1.5rem', '2rem'],
          '3xl': ['1.875rem', '2.25rem'],
          '4xl': ['2.25rem', '2.5rem']
        }
      }
    },
    plugins: []
  };
  