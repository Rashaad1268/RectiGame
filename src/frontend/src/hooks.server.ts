import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const urlEndpoint = event.url.pathname.slice();
    const authEndpoints = ["auth/", "/auth/login", "/auth/signup", "/welcome"];

    const isLoggedIn = !!event.cookies.get("sessionid"); // Check if the sessionid cookie exists

    if (isLoggedIn) {
        // If the user is logged in and he visits the authentication pages, redirect him to the home page
        if (authEndpoints.includes(urlEndpoint)) {
            event.url.pathname = "/";
            return Response.redirect(event.url);
        }
    } else {
        // If the user is not logged in and visits any othe
        if (!authEndpoints.includes(urlEndpoint)) {
            event.url = new URL(`${event.url.origin}/welcome?from=${event.url.pathname}`);

            return Response.redirect(event.url);
        }
    }

    return await resolve(event);
};
