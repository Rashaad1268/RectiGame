<script lang="ts">
	import { joinedTopics } from '$lib/stores';
</script>

<div class="w-14 sm:w-16 flex flex-col items-center gap-2 grow-0 mx-1 mt-2">
	{#each $joinedTopics as topic}
		<a href="/topics/{topic.slug}" class="sidebar-icon group">
			<img
				src={topic.image}
				alt={topic.name}
				class="rounded-3xl group-hover:rounded-2xl transition-transform"
			/>
			<span class="sidebar-tooltip group-hover:scale-100">
				{topic.name}
			</span>
		</a>
	{/each}
</div>

<style lang="postcss">
	.sidebar-icon {
		@apply relative flex items-center justify-center w-14 sm:w-16;
	}

	.sidebar-tooltip {
		@apply absolute w-auto p-2 m-2 min-w-max left-16 rounded-md shadow-md
			 text-white bg-base-100 text-xs font-semibold transition-all
			   duration-100 scale-0 origin-left;
	}
</style>
