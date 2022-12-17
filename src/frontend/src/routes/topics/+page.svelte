<script lang="ts">
	import { fetchApi } from '$lib/api';
	import { topics } from '$lib/stores/';
	import { onMount } from 'svelte';

	import TopicCard from './topicCard.svelte';

	onMount(async () => {
		if (!$topics) {
			const response = await fetchApi('topics/');
			if (response.ok) {
				topics.set(await response.json());
			}
		}
	});
</script>

<svelte:head>
	<title>Topics</title>
</svelte:head>

<div class="grid gap-3 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-7 mr-2">
	{#each $topics?.results || [] as topic (topic.slug)}
		<TopicCard {topic} />
	{:else}
		<button class="btn loading">Loading topics</button>
	{/each}
</div>

<style lang="postcss">
	.grid {
		/* @apply grid-cols-2; */
	}

	@media (max-width: 320px) {
		.grid {
			@apply grid-cols-1 mr-4;
		}
	}
</style>
