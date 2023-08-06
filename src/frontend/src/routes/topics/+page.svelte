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
	{#each $topics?.results || [] as topic (topic.slug)}
		<TopicCard {topic} />
		<TopicCard {topic} />
	{:else}
		<Button aria-label="loading indicator button">Loading topics</Button>
	{/each}
</div>

<style lang="scss">
	#topics-grid {
		@apply grid gap-3 gap-y-4 pt-4 pr-4 overflow-y-auto;
		max-width: 100%; /* DON'T TOUCH THIS!, WITHOUT THIS THE auto-fit DOESN'T WORK FOR SOME REASON */

		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
	}

	@media (max-width: 380px) {
		#topics-grid > :global(div) {
			padding: 3rem;
		}
	}
</style>
