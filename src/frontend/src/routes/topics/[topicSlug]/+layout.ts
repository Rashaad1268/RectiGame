import { get } from "svelte/store";
import { error, type NumericRange } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";
import { topics } from "$lib/stores/";
import { browser } from "$app/environment";

export const load: LayoutLoad = async function ({ fetch, params }) {
    if (browser) {
        // Check if the topic data is already cached in the topics store
        const cachedTopic = get(topics)?.results.filter(
            (topic) => topic.slug === params.topicSlug
        )[0];

        // if it already exists in the cache, return it
        if (cachedTopic) {
            return {
                topic: cachedTopic
            };
        }
    }

    const response = await fetch(`/api/topics/${params.topicSlug}/`);

    if (response.ok) {
        return {
            topic: await response.json()
        };
    } else {
        error(response.status as NumericRange<400, 599>, response.statusText);
    }
};
