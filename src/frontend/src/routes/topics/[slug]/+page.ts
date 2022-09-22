import { get } from 'svelte/store';
import { error } from '@sveltejs/kit';
import type {PageLoad} from './$types';
import {topics} from '$lib/stores';

export const load: PageLoad = async function ({ fetch, params }) {
    const topicsData = get(topics);
    const topic = topicsData?.results.filter((topic) => topic.slug === params.slug)[0];

    if (topic) {
        return {
            topic
        }
    } else {
        const response = await fetch(`/api/topics/${params.slug}/`);
        if (response.ok) {
            return {
                topic: await response.json()
            }
        } else {
            throw error(response.status, response.statusText);
        }
    }
}
