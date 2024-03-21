import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async function () {
    redirect(302, "/");
};

export const ssr = false;
