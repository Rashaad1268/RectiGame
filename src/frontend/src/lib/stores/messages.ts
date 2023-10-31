import { writable } from 'svelte/store';
import type { TopicChatChannelInterface, TopicChatMessageInterface } from '../types';


interface ChannelStoreInterface {
    // topic_id: Array<channels>
	[key: number]: Array<TopicChatChannelInterface>;
}

interface MessageStoreInterface {
    // channel_id: Array<messages>
	[key: number]: Array<TopicChatMessageInterface>;
}

export const channels = writable<ChannelStoreInterface>({});

export const messages = writable<MessageStoreInterface>({});
