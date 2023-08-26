import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	const url = event.url.pathname.slice();
	const authEndpoints = ['auth/', '/auth/login', '/auth/signup', '/welcome'];
	const sessionId = event.cookies.get('sessionId');

	const isLoggedIn = sessionId !== null && sessionId !== '';

	if (isLoggedIn) {
		// If the user is logged in and he visits the authentication pages, redirect him to the home page
		if (authEndpoints.includes(url)) {
			event.url.pathname = '/';
			return Response.redirect(event.url);
		}
	} else {
		// If the user is not logged in and visits any othe
		if (!authEndpoints.includes(url)) {
			event.url = new URL(`${event.url.origin}/welcome?from=${event.url.pathname}`);

			return Response.redirect(event.url);
		}
	}

	return await resolve(event);
};
