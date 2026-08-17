/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ocean: {
          50: "#eef7fb",
          100: "#d3ecf4",
          500: "#0e7fa3",
          600: "#0b6884",
          700: "#0a5268",
          900: "#083344",
        },
      },
    },
  },
  plugins: [],
};
