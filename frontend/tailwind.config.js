/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#165DFF',
          light: '#4080FF',
          dark: '#0E42D2',
        },
        success: {
          DEFAULT: '#00B42A',
          light: '#23C343',
          dark: '#009A29',
        },
        warning: {
          DEFAULT: '#FF7D00',
          light: '#FF9A2E',
          dark: '#D25F00',
        },
        danger: {
          DEFAULT: '#F53F3F',
          light: '#F76560',
          dark: '#CB2634',
        },
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false, // 禁用Tailwind的基础样式重置，避免与ArcoDesign冲突
  },
}
