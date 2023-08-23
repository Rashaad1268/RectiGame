import { get } from 'svelte/store';
import { error } from '@sveltejs/kit';
import type { PageLoad } from '../$types';
import { topics } from '$lib/stores/';

export const load: PageLoad = async function ({ fetch, params }) {
	const topic = get(topics)?.results.filter((topic) => topic.slug === params.slug)[0];
	console.log('t', topic)
	console.log('tee', get(topics))

	if (topic) {
		return {
			topic
		};
	} else {
		const response = await fetch(`/api/topics/${params.slug}/`);
		if (response.ok) {
			return {
				topic: await response.json()
			};
		} else {
			throw error(response.status, response.statusText);
		}
	}
};
