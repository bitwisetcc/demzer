/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#054499",
        "color-primary-dimm": "#4373b6",

        "color-secondary": "#CD9028",
        "color-hover": "#E8C17E",

        "color-bg-perfil": "#F5F5F5",
        "color-boletim": "#D7D4D4",
        "color-grey": "#EDECEC",
        "color-bg": "#e4e4e7",
        "color-bg-alt": "#d4d4d8",
        "color-bg-lighter": "#f4f4f5",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
