import { sveltekit } from "@sveltejs/kit/vite";
import type { UserConfig } from "vite";

const SERVER_ADDR = "http://127.0.0.1:8000/";

const config: UserConfig = {
    plugins: [sveltekit()],
    server: {
        proxy: {
            "/api/ws/": {
                // Websocket Proxy
                target: SERVER_ADDR,
                changeOrigin: true,
                ws: true
            },
            "/api/": {
                // Backend API Proxy
                target: SERVER_ADDR,
                changeOrigin: true
            },
            "/static/": {
                // proxy the DRF static files, only needed for local testing
                target: SERVER_ADDR,
                changeOrigin: true
            },
            "/media/": {
                // proxy the user uploaded media files, only for local testing
                target: SERVER_ADDR,
                changeOrigin: true
            }
        }
    }
};

export default config;
