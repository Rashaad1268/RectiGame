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
                // Static files Proxy
                target: SERVER_ADDR,
                changeOrigin: true
            },
            "/media/": {
                // Media files proxy, only for local testing
                target: SERVER_ADDR,
                changeOrigin: true
            }
        }
    }
};

export default config;
