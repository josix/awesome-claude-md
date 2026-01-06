import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://josix.github.io',
  base: '/awesome-claude-md',
  integrations: [tailwind()],
  build: {
    format: 'directory'
  }
});
