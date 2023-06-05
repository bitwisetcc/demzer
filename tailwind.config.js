/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#32659A", //Blue Color
        "color-secundary": "#E2A161", //Orange Color
        "main-color": "#E6E3E3", //Background Color
        "dark-gold": "#CD9028", //HOVER Color
        "light-gold": "#E8C17E", 
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}

