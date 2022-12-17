<script lang="ts">
	import { fetchApi, getCookie } from '$lib/api';
	import { topicPosts } from '$lib/stores/';
	import type { TopicInterface } from '$lib/types';
	import { onMount } from 'svelte';
	import PostCard from './postCard.svelte';

	export let topic: TopicInterface;

	$: postsPaginator = $topicPosts[topic.slug];
    let csrfToken: string | null = null

    onMount(() => {
        csrfToken = getCookie("csrftoken")
    })

	$: {
		onMount(() => {
			if (!postsPaginator && document) {
				fetchApi(`posts/?topic=${topic.slug}`).then(async (response) => {
					if (response.ok) {
						const data = await response.json();
						console.log('data', data);
						topicPosts.update((posts) => {
							return {
								...posts,
								[topic.slug]: data
							};
						});
					}
				});
			}
		});
	}
</script>

<div class="pt-10 flex flex-col items-center">
	{#each postsPaginator?.results || [] as post}
		<PostCard {post} />
	{/each}
</div>
