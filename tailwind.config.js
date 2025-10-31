/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Apple-inspired color system (simplified)
        apple: {
          50: '#fafafa',
          100: '#f5f5f5', 
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
        },
        // Apple blue (signature color)
        'apple-blue': {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe', 
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#007AFF',
          600: '#0056d6',
          700: '#0040a0',
          800: '#1e3a8a',
          900: '#1e3a8a',
        },
        // Semantic colors
        'apple-success': '#34C759',
        'apple-warning': '#FF9500', 
        'apple-error': '#FF3B30',
        // Light theme colors
        'light-bg': '#f2f2f7',
        'light-card': '#ffffff',
        'light-text': '#000000',
        'light-text-secondary': '#3c3c43',
        'light-border': '#e5e5e5',
        // Dark theme colors
        'dark-bg': '#000000',
        'dark-card': '#1c1c1e',
        'dark-text': '#ffffff',
        'dark-text-secondary': '#ebebf5',
        'dark-border': '#3a3a3c',
      },
      animation: {
        // Apple-style refined animations
        'fade-in': 'fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        'slide-down': 'slideDown 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        'scale-in': 'scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        'apple-bounce': 'appleBounce 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
        'gentle-pulse': 'gentlePulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'loading-apple': 'loadingApple 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(16px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-16px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        appleBounce: {
          '0%': { transform: 'scale(0.95)' },
          '50%': { transform: 'scale(1.02)' },
          '100%': { transform: 'scale(1)' },
        },
        gentlePulse: {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '0.8' },
        },
        loadingApple: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        }
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        // Apple-style subtle shadows
        'apple-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'apple': '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
        'apple-md': '0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03)',
        'apple-lg': '0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02)',
        'apple-xl': '0 25px 50px -12px rgba(0, 0, 0, 0.08)',
        // Dark mode shadows
        'apple-dark': '0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1)',
        'apple-dark-lg': '0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2)',
        // Card shadows
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      // Apple-style font sizes and spacing
      fontSize: {
        'apple-xs': ['11px', { lineHeight: '16px', letterSpacing: '-0.005em' }],
        'apple-sm': ['13px', { lineHeight: '18px', letterSpacing: '-0.005em' }],
        'apple-base': ['15px', { lineHeight: '22px', letterSpacing: '-0.01em' }],
        'apple-lg': ['17px', { lineHeight: '24px', letterSpacing: '-0.01em' }],
        'apple-xl': ['19px', { lineHeight: '28px', letterSpacing: '-0.015em' }],
        'apple-2xl': ['22px', { lineHeight: '32px', letterSpacing: '-0.015em' }],
        'apple-3xl': ['28px', { lineHeight: '36px', letterSpacing: '-0.02em' }],
        'apple-4xl': ['34px', { lineHeight: '44px', letterSpacing: '-0.02em' }],
      },
      fontWeight: {
        'light': '300',
        'regular': '400', 
        'medium': '500',
        'semibold': '600',
        'bold': '700',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      }
    },
  },
  plugins: [],
}