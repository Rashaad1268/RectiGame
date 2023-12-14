import { writable } from "svelte/store";
import type { PaginatorInterface, PostInterface } from "../types";

interface TopicPostsInterface {
    [key: string]: PaginatorInterface<PostInterface>;
}

export const topicPosts = writable<TopicPostsInterface>({});
