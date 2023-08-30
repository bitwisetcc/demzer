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
      },
    },
    screens: {
      md: "768px",
      sm: "640px",
      md2: { max: "767px" },
      sm2: { max: "375px" },
      ultrawide: "2500px",
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
