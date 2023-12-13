import { fetchApi } from './api';
import { joinedTopics, userData } from './stores';
import { channelStore } from './stores/';
import type { TopicInterface } from './types';

export function truncate(text: string, maxLen: number) {
	return text.length > maxLen ? text.slice(0, maxLen) + '...' : text;
}

export async function fetchUserData() {
	const response = await fetchApi('auth/users/me/');

	if (response.ok) {
		const data = await response.json();
		userData.set(data['user']);
		joinedTopics.set(data['joined_topics']);

		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const _channels: any = {};

		data['joined_topics'].forEach((topic: TopicInterface) => {
			_channels[topic.slug] = topic.channels;
		});

		channelStore.set(_channels);
	} else {
		console.error(`Failed to fetch user data (status: ${response.status} ${response.statusText})`);
	}
}
