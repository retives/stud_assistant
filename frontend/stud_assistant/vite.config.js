import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';

// NOTE: `vite-plugin-vue-devtools` (and its dependency @vue/devtools-kit)
// may access `localStorage` at module initialization which fails during
// a Node build (no browser APIs). To avoid that, dynamically import the
// devtools plugin only in development mode inside the config function.
export default defineConfig(async ({ mode }) => {
    const plugins = [vue(), vueJsx()];

    if (mode === 'development') {
        try {
            const { default: vueDevTools } = await import('vite-plugin-vue-devtools');
            plugins.push(vueDevTools());
        } catch (e) {
            // If dynamic import fails, log and continue without the plugin.
            // This keeps production builds stable.
            // eslint-disable-next-line no-console
            console.warn('Could not load vite-plugin-vue-devtools:', e && e.message ? e.message : e);
        }
    }

    return {
        base: '/stud_assistant/',
        plugins,
        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url))
            },
        },
    };
});
//# sourceMappingURL=vite.config.js.map