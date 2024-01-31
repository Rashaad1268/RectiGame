import { browser } from "$app/environment";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { channelStore } from "$lib/stores";
import type { TopicChatChannelInterface } from "$lib/types";

export const load: PageLoad = async (event) => {
    const topicSlug = event.params.topicSlug;
    const channel_id = event.params.channel_id;

    if (!channel_id) {
        return;
    }

    if (browser) {
        const channel =
            (get(channelStore)[topicSlug] || []).find(
                (channel: TopicChatChannelInterface) => channel.id === parseInt(channel_id)
            ) || null;

        if (channel) {
            return { channel: channel };
        } else {
            console.log("sent req");
            return { channel: await (await event.fetch(`/api/channels/${channel_id}/`)).json() };
        }
    } else {
        console.log("sent req");
        return { channel: await (await event.fetch(`/api/channels/${channel_id}/`)).json() };
    }
};
