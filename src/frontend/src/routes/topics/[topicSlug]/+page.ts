import { get } from 'svelte/store';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { topics } from '$lib/stores/';

export const load: PageLoad = async function ({ fetch, params }) {
	const topic = get(topics)?.results.filter((topic) => topic.slug === params.topicSlug)[0];

	if (topic) {
		return {
			topic
		};
	} else {
		const response = await fetch(`/api/topics/${params.topicSlug}/`);
		if (response.ok) {
			return {
				topic: await response.json()
			};
		} else {
			throw error(response.status, response.statusText);
		}
	}
};
