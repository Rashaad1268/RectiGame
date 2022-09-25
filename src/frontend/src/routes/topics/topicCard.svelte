<script lang="ts">
	import { truncate } from '$lib/text';
	import type { TopicInterface } from '$lib/types';

	export let topic: TopicInterface;
</script>

<a href="/topics/{topic.slug}" class="group bg-base-300 shadow-lg">
	<div class="bg-secondary">
		<img
			class="w-full group-hover:translate-x-2 group-hover:-translate-y-2 transition-transform"
			src={topic.image}
			alt="{topic.image} img"
		/>
	</div>
	<div class="px-1 py-4">
		<div class="font-bold text-xl mb-1">{topic.name}</div>
		<p class="text-base">{truncate(topic.description, 60)}</p>
	</div>
	<div class="px-1 pt-0 pb-0">
		{#each topic.tags as tag}
			<a
				class="inline-block bg-zinc-700 rounded-full px-1 py-[2px] text-xs font-semibold mr-1 mb-1"
				href="/topics/tag/{tag.slug}">{tag.name}</a
			>
		{/each}
	</div>
</a>
