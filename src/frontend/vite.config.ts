import { sveltekit } from '@sveltejs/kit/vite';
import type { UserConfig } from 'vite';

const config: UserConfig = {
	plugins: [sveltekit()],
	server: {
		proxy: {
		  '/api/': {
			// Backend API Proxy
			target: 'http://127.0.0.1:8000/',
			changeOrigin: true,
		},
		'/static/': {
			// Staticfiles Proxy
			target: 'http://127.0.0.1:8000/',
			changeOrigin: true,
		  }
		}
	  }
};

export default config;
