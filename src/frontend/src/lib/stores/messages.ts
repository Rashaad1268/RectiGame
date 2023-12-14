import { writable } from "svelte/store";
import type { TopicChatChannelInterface, TopicChatMessageInterface } from "../types";

interface ChannelStoreInterface {
    // topic_slug: Array<channels>
    [key: string]: Array<TopicChatChannelInterface> | undefined;
}

interface MessageStoreInterface {
    // channel_id: Array<messages>
    [key: number]: { count: number; results: Array<TopicChatMessageInterface> | undefined };
}

export const channelStore = writable<ChannelStoreInterface>({});

export const messageStore = writable<MessageStoreInterface>({});
