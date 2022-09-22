import { writable } from "svelte/store";
import type { PaginatorInterface, TopicInterface, UserInterface } from "./types";


export const userData = writable<UserInterface | null>(null);

export const topics = writable<PaginatorInterface<TopicInterface> | null>(null);

export const joinedTopics = writable<Array<TopicInterface>>([]);
