/** @type {import('tailwindcss').Config} */

const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
      minWidth: ({ theme }) => ({
        ...theme("width"),
      }),
      maxWidth: ({ theme }) => ({
        ...theme("width"),
      }),
      minHeight: ({ theme }) => ({
        ...theme("height"),
      }),
      maxHeight: ({ theme }) => ({
        ...theme("height"),
      }),
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
