<script lang="ts">
	import { page } from '$app/stores';
	import { fetchApi } from '$lib/api.js';
	import { channelStore, messageStore } from '$lib/stores/';
	import type { TopicChatChannelInterface, TopicChatMessageInterface } from '$lib/types';

	const timeFormatter = new Intl.DateTimeFormat('en', {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});

	export let data;

	$: selectedTopicSlug = $page.params.topicSlug as string;
	$: selectedChannelId = $page.params.channel_id;

	// Initialize it to undefined to specify that its loading
	let channel: TopicChatChannelInterface | undefined | null = undefined;

	$: {
		if (!selectedChannelId) {
			// This means that the user has not selected a channel to view
			channel = null;
			break $;
		}

		if (selectedTopicSlug && Object.keys($channelStore).length > 0) {
			// channel = null means that the channel is not found
			channel =
				($channelStore[selectedTopicSlug] || []).find(
					(channel: TopicChatChannelInterface) => channel.id === parseInt(selectedChannelId)
				) || null;

			if (!!channel) {
			}
		}
	}

	async function fetchMessages(): Promise<Array<TopicChatMessageInterface>> {
		const cachedMessages = $messageStore[channel!.id];

		if (!!cachedMessages) {
			return cachedMessages;
		}

		const messages = await (await fetchApi(`channels/${channel!.id}/messages/`)).json();

		messageStore.update((msgs) => {
			msgs[channel!.id] = messages;
			return msgs;
		});

		return messages;
	}

	function getPrevMessage(idx: number): TopicChatMessageInterface | undefined {
		return ($messageStore[channel!.id] ?? [])[idx - 1];
	}
</script>

{#if !selectedChannelId}
	<h1 class="text-3xl text-center font-semibold mt-[20dvh]">Select a channel to view</h1>
{:else if channel === undefined}
	Loading...
{:else if channel === null}
	404 channel not found
{:else}
	<div class="flex flex-col bg-discordDark-730 h-[calc(100vh-var(--navbar-height))]">
		<div
			class="flex border-b border-discordDark-600 items-center gap-2 text-lg font-medium pl-8 py-3"
		>
			<span>
				{data.topic.name}
			</span>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				height="14px"
				fill="currentColor"
				viewBox="0 0 384 512"
				><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
					d="M3.4 81.7c-7.9 15.8-1.5 35 14.3 42.9L280.5 256 17.7 387.4C1.9 395.3-4.5 414.5 3.4 430.3s27.1 22.2 42.9 14.3l320-160c10.8-5.4 17.7-16.5 17.7-28.6s-6.8-23.2-17.7-28.6l-320-160c-15.8-7.9-35-1.5-42.9 14.3z"
				/></svg
			>
			<span>
				{channel.name}
			</span>
		</div>

		<div class="channel-messages">
			{#await fetchMessages()}
				<h1>Loading...</h1>
			{:then messages}
				{#each messages || [] as message, idx (message.id)}
					<div class="message">
						{#if !!message.author}
							{@const prevMsgIsFromMe = getPrevMessage(idx)?.author?.id === message.author.id}
							<div class="profile-picture-wrapper">
								{#if !!message.author.profile.profile_picture && !prevMsgIsFromMe}
									<img
										src={message.author.profile.profile_picture}
										alt="{message.author.username} profile"
									/>
								{/if}
							</div>

							<div class="flex flex-col">
								{#if !prevMsgIsFromMe}
									<div>
										<span class="font-semibold">{message.author.username}</span>
										<!-- <span>{timeFormatter.format(new Date(message.created_at))}</span> -->
									</div>
								{/if}
								<span>{message.content}</span>
							</div>
						{/if}
					</div>
				{/each}
			{/await}
		</div>
	</div>
{/if}

<style lang="scss">
	.channel-messages {
		@apply overflow-y-scroll h-full p-2;
	}

	.message {
		@apply flex;

		.profile-picture-wrapper {
			@apply h-10 w-10 mr-3;

			img {
				@apply h-10 w-10 object-cover rounded-full mt-[4px];
			}
		}

		&:hover {
			@apply bg-discordDark-760;
		}
	}
</style>
