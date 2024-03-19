import { writable } from "svelte/store";
import type { PaginatorInterface, TopicInterface, TopicRoomInterface, UserInterface } from "../types";
export { toastStore, addToast, removeToast } from "./toast";

export { topicPosts } from "./posts";
export { messageStore } from "./messages";

export const userData = writable<UserInterface | null>(null);

export const topics = writable<PaginatorInterface<TopicInterface> | null>(null);

interface JoinedTopicsInterface {
    [key: string]: TopicInterface;
}


export const joinedTopics = writable<JoinedTopicsInterface>({});

interface JoinedTopicRoomsInterface {
    [key: string]: TopicRoomInterface[];
}

export const joinedTopicRooms = writable<JoinedTopicRoomsInterface>({});

export interface WS extends WebSocket {
    sendQueued: (data: string | ArrayBufferLike | Blob | ArrayBufferView) => void;
}

export const socket = writable<WS | null>(null);

export function clearData() {
    userData.set(null);
    joinedTopics.set({});
    topics.set(null);
    joinedTopicRooms.set({});
}
