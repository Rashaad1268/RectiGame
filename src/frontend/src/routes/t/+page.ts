import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async function () {
    throw redirect(302, `/topics/`);
};
