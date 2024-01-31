import { writable } from "svelte/store";
import type { PaginatorInterface, TopicInterface, UserInterface } from "../types";
export { toastStore, addToast, removeToast } from "./toast";

export { topicPosts } from "./posts";
export { channelStore, messageStore } from "./messages";

export const userData = writable<UserInterface | null>(null);

export const topics = writable<PaginatorInterface<TopicInterface> | null>(null);

export const joinedTopics = writable<Array<TopicInterface>>([]);

export interface WS extends WebSocket {
    sendQueued: (data: string | ArrayBufferLike | Blob | ArrayBufferView) => void;
}

export const socket = writable<WS | null>(null);

export function clearData() {
    userData.set(null);
    joinedTopics.set([]);
    topics.set(null);
}
