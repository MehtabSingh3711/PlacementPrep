/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'khaki-beige': '#c3a995',
        'dusty-taupe': '#ab947e',
        'ash-brown': '#6f5e53',
        'dusty-taupe-dark': '#8a7968',
        'chocolate-plum': '#593d3b',
      },
      boxShadow: {
        'key-unpressed': '4px 4px 6px #593d3b, -2px -2px 4px #ab947e',
        'key-pressed': 'inset 3px 3px 6px #593d3b, inset -3px -3px 6px #ab947e',
        'wood-relief': '2px 2px 4px rgba(0,0,0,0.3), -2px -2px 4px rgba(255,255,255,0.1)',
      }
    },
  },
  plugins: [],
}
