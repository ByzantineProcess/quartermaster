/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './ui/**/*.{html,js}',
    './ui/*.{html,js}',
  ],
  theme: {
    extend: {
      colors: {
        'base': '#3a0e6f',
        'black': '#000000',
        'some-accent': '#21a86b'
      },
    },
  },
  plugins: [],
}


