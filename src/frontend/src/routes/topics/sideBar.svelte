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
		@apply sticky left-0 bottom-0 top-20 flex flex-col items-center gap-2 grow-0
			  bg-discordDark-860 min-h-screen max-h-screen w-20;
	}

	.sidebar-icon {
		@apply relative flex items-center justify-center mx-2 w-16;

		.sidebar-icon-img-wrapper {
			@apply relative overflow-hidden rounded-[100%] transition-all delay-[10ms];

			.sidebar-icon-img {
				@apply inline rounded-[100%] my-[-10%] h-full w-full;
			}
		}

		&:hover {
			.sidebar-icon-img-wrapper {
				@apply rounded-[40%];
			}
		}

		&:active {
			@apply translate-y-[2px]
		}
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
