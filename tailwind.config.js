/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#054499",
<<<<<<< HEAD
        "color-primary-dimm": "#0a3c6f",
        "color-secondary": "#E6A82E",
        "color-secondary-dimm": "#E8C17E" 
      },
      screens: {
      'sm': '640px',
      // => @media (min-width: 640px) { ... }

      'md': '768px',
      // => @media (min-width: 768px) { ... }

      'lg': '1024px',
      // => @media (min-width: 1024px) { ... }

      'xl': '1280px',
      // => @media (min-width: 1280px) { ... }

      '2xl': '1536px',
      // => @media (min-width: 1536px) { ... }
    }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}
=======
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
>>>>>>> main
