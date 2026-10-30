/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#0f172a',
          saffron: '#d97706',
          green: '#059669',
        },
      },
    },
  },
  plugins: [],
};

