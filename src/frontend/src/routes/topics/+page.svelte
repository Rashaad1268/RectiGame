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

<div 
	class="grid grow gap-[1px]"
>
	{#each $topics?.results || [] as topic}
		<TopicCard {topic} />
		<!-- <TopicCard {topic} />
		<TopicCard {topic} /> -->
	{:else}
		<button class="btn loading">Loading topics</button>
	{/each}
</div>

<style global lang="postcss">
/* @media (min-width: 580px) { */
	.grid {
		grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
	}
/* } */
</style>
