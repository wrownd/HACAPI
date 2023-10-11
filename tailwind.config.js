/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "background" : "#0000",
        "headline" : "#fff",
        "paragraph" : "#5f6c7b",
        "main" : "#fffffe",
        "secondary" : '#90b4ce',
      }
    },
  },
  plugins: [],
}
