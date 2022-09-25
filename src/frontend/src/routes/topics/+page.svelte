<script lang="ts">
	import { fetchApi } from '$lib/api';
	import { topics } from '$lib/stores';
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

<div class="grid gap-3 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-7">
	{#each $topics?.results || [] as topic}
		<TopicCard {topic} />
	{:else}
		<button class="btn loading">Loading topics</button>
	{/each}
</div>

<style global lang="postcss">
@media (max-width: 320px) {
	.grid {
		grid-template-columns: 1fr;
	}
}
</style>
