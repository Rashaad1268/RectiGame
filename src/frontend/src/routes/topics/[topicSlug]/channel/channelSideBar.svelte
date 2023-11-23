<script lang="ts">
	import { page } from '$app/stores';
	import { channelStore, joinedTopics } from '$lib/stores/';
	import type { TopicChatChannelInterface, TopicInterface } from '$lib/types';

	$: selectedTopicSlug = $page.params.topicSlug as string;

	$: topic = $joinedTopics.find((topic) => topic.slug === selectedTopicSlug) as TopicInterface;

	$: channels = $channelStore[selectedTopicSlug] as Array<TopicChatChannelInterface>;
</script>

<div class="channel-sidebar">
	{#if !!topic}
		<header class="mb-3 pl-2">
			<h1 class="text-3xl font-semibold font-monocraft text-white">{topic.name}</h1>
			<a href="/topics/{topic.slug}" class="block my-1 link">View posts</a>
		</header>

		<div class="w-full h-[1px] bg-discordDark-630 mb-2" />

		{#each channels || [] as channel (channel.id)}
			<a
				href="/topics/{topic.slug}/channel/{channel.id}"
				class="channel-tab"
				class:selected={parseInt($page.params.channel_id) === channel.id}
			>
				<svg xmlns="http://www.w3.org/2000/svg" height="15px" viewBox="0 0 448 512"
					><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
						d="M181.3 32.4c17.4 2.9 29.2 19.4 26.3 36.8L197.8 128h95.1l11.5-69.3c2.9-17.4 19.4-29.2 36.8-26.3s29.2 19.4 26.3 36.8L357.8 128H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H347.1L325.8 320H384c17.7 0 32 14.3 32 32s-14.3 32-32 32H315.1l-11.5 69.3c-2.9 17.4-19.4 29.2-36.8 26.3s-29.2-19.4-26.3-36.8l9.8-58.7H155.1l-11.5 69.3c-2.9 17.4-19.4 29.2-36.8 26.3s-29.2-19.4-26.3-36.8L90.2 384H32c-17.7 0-32-14.3-32-32s14.3-32 32-32h68.9l21.3-128H64c-17.7 0-32-14.3-32-32s14.3-32 32-32h68.9l11.5-69.3c2.9-17.4 19.4-29.2 36.8-26.3zM187.1 192L165.8 320h95.1l21.3-128H187.1z"
					/></svg
				>
				{channel.name}</a
			>
		{/each}
	{/if}
</div>

<style lang="scss">
	.channel-sidebar {
		@apply flex flex-col w-[260px] p-4 gap-[2px] bg-discordDark-800;

		height: calc(100vh - var(--navbar-height));
	}
	.channel-tab {
		@apply flex text-discordDark-360 fill-discordDark-360
			   pl-6 py-1 rounded-md items-center gap-2;

		&:hover {
			@apply bg-discordDark-660 text-discordDark-300;
		}
		
		&:not(.selected):active {
			// The effect when a tab which is not selected is :active
			@apply bg-discordDark-630 text-gray-200 brightness-90;
		}

		&.selected {
			@apply bg-discordDark-630 text-gray-200;
		}
	}
</style>
