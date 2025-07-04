import tailwindcss from '@tailwindcss/postcss';
import autoprefixer from 'autoprefixer';

/**
 * Standard PostCSS configuration for Tailwind CSS v4.
 * Uses the new `@tailwindcss/postcss` plugin so builds succeed.
 */
export default {
  plugins: {
    tailwindcss: tailwindcss(),
    autoprefixer: autoprefixer(),
  },
};