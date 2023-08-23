/*	
	Right now there is a MAJOR issue where this endpoint sends a reques to the API every
	time it's visited. 
	FIX: Implement caching and reduce the number of API calls

	related file: ./+page.ts
*/

import { get } from 'svelte/store';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { topics } from '$lib/stores/';

export const load: PageLoad = async function ({ fetch, params }) {
	const topic = get(topics)?.results.filter((topic) => topic.slug === params.slug)[0];
	// get(store) always returns null for some reason???

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
