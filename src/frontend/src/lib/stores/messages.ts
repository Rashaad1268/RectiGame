import { writable } from "svelte/store";
import type { TopicChatMessageInterface } from "../types";

interface MessageStoreInterface {
    // channel_id: Array<messages>
    [key: number]: { count: number; results: Array<TopicChatMessageInterface> | undefined };
}

export const messageStore = writable<MessageStoreInterface>({});
