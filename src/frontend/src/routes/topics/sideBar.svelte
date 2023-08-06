<script lang="ts">
	import { joinedTopics } from '$lib/stores/';
</script>


<div class="sidebar">
	{#each $joinedTopics as topic (topic.slug)}
		<a href="/topics/{topic.slug}/posts" class="sidebar-icon">
			<div class="sidebar-icon-img-wrapper">
				<img
					src={topic.image}
					alt={topic.name}
					loading="lazy"
					class="sidebar-icon-img"
				/>
			</div>
			<span class="sidebar-tooltip">
				{topic.name}
			</span>
		</a>
	{/each}
</div>

<style lang="scss">
	.sidebar {
		@apply sticky left-0 bottom-0 top-0 flex flex-col items-center gap-2 grow-0
			  bg-discordDark-860 h-[100%] w-16 overflow-y-scroll;
		// @apply bg-[#E3E5E8];
	}

	.sidebar-icon {
		// @apply relative flex items-center justify-center mx-2 w-16;
		@apply relative flex items-center justify-center 
		h-12 w-12 mt-2 mb-2 mx-auto  
		bg-white dark:bg-gray-800 dark:hover:bg-[#5865F2]
		text-black hover:text-white dark:text-white dark:hover:text-black
		hover:rounded-xl rounded-3xl
		transition-all duration-300 ease-linear
		cursor-pointer shadow-sm;

		.sidebar-icon-img-wrapper {
			// @apply relative overflow-hidden rounded-[100%] transition-all delay-[10ms];
			// @apply max-w-[100%] max-h-[100%];

			.sidebar-icon-img {
				// @apply inline rounded-[100%] my-[-10%] h-full w-full;
				@apply rounded-3xl
					transition-all duration-300 ease-linear w-12 h-12;
			}
		}

		&:hover {
			.sidebar-icon-img {
				// @apply inline rounded-[100%] my-[-10%] h-full w-full;
				@apply rounded-xl
					transition-all duration-300 ease-linear w-12 h-12;
			}	
		}

		// &:active {
		// 	@apply translate-y-[2px]
		// }
	}

	.sidebar-tooltip {
		@apply absolute w-auto p-2 m-2 min-w-max left-16 rounded-md shadow-md
			 text-white bg-discordDark-900 text-xs font-semibold
			   transition-all duration-100 scale-0 origin-left;


		.sidebar-icon:hover > & {
			// Scale the tooltip up when the icon is hovered
			@apply scale-100;
		}
	}
</style>
