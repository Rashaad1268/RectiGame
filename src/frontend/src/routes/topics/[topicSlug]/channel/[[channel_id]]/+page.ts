import { browser } from "$app/environment";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { channelStore } from "$lib/stores";
import { error, type NumericRange } from "@sveltejs/kit";

export const load: PageLoad = async (event) => {
    const topicSlug = event.params.topicSlug;
    const channel_id = event.params.channel_id;

    if (!channel_id) {
        return;
    }

    if (browser) {
        // first check if the channel is cached in the channelStore
        const channel = (get(channelStore)[topicSlug] || []).find(
            (channel) => channel.id === parseInt(channel_id)
        );

        if (channel) {
            return { channel: channel };
        }
    }

    const response = await event.fetch(`/api/channels/${channel_id}/`);
    if (response.ok) {
        return { channel: await response.json() };
    } else {
        error(response.status as NumericRange<400, 599>, response.statusText);
    }
};
