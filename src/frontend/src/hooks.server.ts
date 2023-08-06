import type { Handle } from '@sveltejs/kit';

import { parseCookies } from '$lib/api';

export const handle: Handle = async ({ event, resolve }) => {
	const url = event.url.pathname.slice();
	const authEndpoints = ['auth/', '/auth/login', '/auth/signup', '/welcome'];
	const sessionId = parseCookies(event.request.headers.get('cookie') || '', 'sessionid');

	const isLoggedIn = sessionId !== null && sessionId !== '';

	if (isLoggedIn) {
		if (authEndpoints.includes(url)) {
			event.url.pathname = '/';
			return Response.redirect(event.url);
		}
	} else {
		if (!authEndpoints.includes(url)) {
			event.url = new URL(`${event.url.origin}/welcome?from=${event.url.pathname}`);

			return Response.redirect(event.url);
		}
	}

	return await resolve(event);
};
