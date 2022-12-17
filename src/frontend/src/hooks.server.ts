import type { Handle } from '@sveltejs/kit';

import { parseCookies } from '$lib/api';

export const handle: Handle = async ({ event, resolve }) => {
	const url = event.url.pathname;
	const authEndpoints = ['/login', '/signup', '/welcome'];
	const sessionId = parseCookies(event.request.headers.get('cookie') || '', 'sessionid');

	const isLoggedIn = sessionId !== null && sessionId !== '';

	if (isLoggedIn) {
		if (authEndpoints.includes(url)) {
			event.url.pathname = '/';
			return Response.redirect(event.url);
		}
	} else {
		if (!authEndpoints.includes(url)) {
			event.url.pathname = '/welcome';
			return Response.redirect(event.url);
		}
	}

	return await resolve(event);
};
