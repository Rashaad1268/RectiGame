import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async function ({ params }) {
    redirect(302, `/topics/${params.topicSlug}/`);
};
