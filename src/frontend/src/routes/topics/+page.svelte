<script lang="ts">
	import { fetchApi } from '$lib/api';
	import Button from '$lib/components/button.svelte';
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

<div id="topics-grid">
	{#if !!($topics?.results) && $topics?.results.length !== 0}
		{#each $topics?.results as topic (topic.slug)}
			<TopicCard {topic} />
		{:else}
			<Button aria-label="loading indicator button">Loading topics</Button>
		{/each}

	{:else}
		<p class="text-2xl font-semibold text-center">No topics...for now</p>
	{/if}
</div>

<style lang="scss">
	#topics-grid {
		@apply grid gap-3 gap-y-4 pt-4 pr-4 overflow-y-scroll h-full ml-4;
		max-width: 100%; /* DON'T TOUCH THIS!, WITHOUT THIS THE auto-fit DOESN'T WORK FOR SOME REASON */
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
	}

	@media (max-width: 380px) {
		#topics-grid > :global(div) {
			padding: 3rem;
		}
	}
</style>
