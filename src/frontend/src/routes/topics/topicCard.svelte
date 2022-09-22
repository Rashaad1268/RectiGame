<script lang="ts">
	import type { TopicInterface } from '$lib/types';

	export let topic: TopicInterface;
</script>

<!-- <a href="/topics/{topic.slug}">
	<div class="card card-bordered card-compact w-52 z-0 shadow-xl border-base-300">
		<figure><img src={topic.image} class="image-full" alt="{topic.name} img" /></figure>
		<div class="card-body border-red-500">
			<h2 class="card-title">
				{topic.name}
			</h2>

			<p class="text-ellipsis">{topic.description}</p>

			<div class="card-actions">
				{#each topic.tags as tag}
					<a class="badge badge-outline" href="/topics/tag/{tag.slug}">{tag.name}</a>
				{/each}
			</div>
		</div>
	</div>
</a> -->
<a href="/topics/{topic.slug}">
	<div class="w-full border rounded-lg overflow-hidden shadow-lg">
		<img class="w-full" src={topic.image} alt="{topic.image} img" />
		<div class="px-6 py-4">
			<div class="font-bold text-xl mb-1">{topic.name}</div>
			<p class="text-base truncate-overflow">
				{topic.description}
			</p>
		</div>
		<div class="px-6 pt-0 pb-0">
			{#each topic.tags as tag}
				<a
					class="inline-block bg-gray-200 rounded-full px-1 py-[2px] text-sm font-semibold text-gray-700 mr-1 mb-1"
					href="/topics/tag/{tag.slug}">{tag.name}</a
				>
			{/each}
		</div>
	</div>
</a>

<style lang="postcss">
	@media (min-width: 370px) {
		.topic-card {
			@apply w-36;
		}
	}
	@media (min-width: 430px) {
		.topic-card {
			@apply w-44;
		}
	}

	.truncate-overflow {
		position: relative;
		max-height: 4.2em;
		overflow: hidden;
		z-index: -9999;
		/* text-overflow: -o-ellipsis-lastline; */
		padding-right: 5px; /* space for ellipsis */
	}
	.truncate-overflow::before {
		position: absolute;
		content: '...';
		inset-block-end: 0;
		inset-inline-end: 0;
	}
	.truncate-overflow::after {
		content: '';
		position: absolute;
		inset-inline-end: 0;
		width: 1rem;
		height: 1rem;
		background: transparent;
	}
</style>
