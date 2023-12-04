<script lang="ts">
	import { page } from '$app/stores';
	import { fetchApi } from '$lib/api.js';
	import { channelStore, messageStore } from '$lib/stores/';
	import Message from './message.svelte';
	import type { TopicChatChannelInterface, TopicChatMessageInterface } from '$lib/types';
	import MessageInput from './messageInput.svelte';

	export let data;

	$: selectedTopicSlug = $page.params.topicSlug as string;
	$: selectedChannelId = $page.params.channel_id;

	$: messages = ($messageStore[channel?.id ?? -1] ?? {}).results;

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
		}
	}

	$: {
		if (channel && messages === undefined) {
			fetchApi(`channels/${channel!.id}/messages/`).then((response) => {
				response.json().then((fetchedMessages) => {
					messageStore.update((msgs) => {
						msgs[channel!.id] = fetchedMessages;
						return msgs;
					});
				});
			});
		}
	}

	let isFetchingNewMessages = false;

	function loadMessages(event: Event) {
		if (!channel || !messages) {
			return;
		}

		const element = event.target as HTMLDivElement;

		if (element.scrollHeight + element.scrollTop < 750) {
			if (!isFetchingNewMessages && messages.length !== $messageStore[channel!.id].count) {
				isFetchingNewMessages = true;
				fetchApi(
					`channels/${channel!.id}/messages/?before=${messages[messages.length - 1].id}`
				).then((response) => {
					if (response.ok) {
						response.json().then((data) => {
							messageStore.update((existingMessages) => {
								existingMessages[channel!.id].results?.push(...data.results);
								return existingMessages;
							});
							isFetchingNewMessages = false;
						});
					}
				});
			}
		}
	}

	function getPrevMessage(idx: number): TopicChatMessageInterface | undefined {
		return ($messageStore[channel!.id]?.results ?? [])[idx + 1];
	}

	let messageContent = '';

	async function sendMessage(event: Event) {
		event.preventDefault(); // If this is not called the input will lose focus

		const finalMessageContent = messageContent.trim();

		if (!!channel && finalMessageContent) {
			const response = await fetchApi(`channels/${channel.id}/messages/`, {
				method: 'POST',
				body: JSON.stringify({ content: finalMessageContent })
			});

			if (response.ok) {
				messageContent = '';
			}
		}
	}
</script>

{#if !selectedChannelId}
	<h1 class="text-3xl text-center font-semibold mt-[20dvh]">Select a channel to view</h1>
{:else if channel === undefined}
	Loading...
{:else if channel === null}
	404 channel not found
{:else}
	<div
		class="flex flex-col justify-end bg-discordDark-730 max-h-[calc(100vh-var(--navbar-height))] h-full scroll-smooth pb-1 w-full"
	>
		<div
			class="flex border-b border-discordDark-600 items-center gap-2 text-lg font-medium
				   pl-8 py-3 mb-auto"
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

		<div class="channel-messages" on:scroll={loadMessages}>
			{#each messages || [] as message, idx (message.id)}
				{@const isInlineMsg = getPrevMessage(idx)?.author?.id === message.author.id}
				<Message {message} isInline={isInlineMsg} />
			{/each}
		</div>

		<form on:submit={sendMessage} class="px-4">
			<MessageInput bind:value={messageContent} />
		</form>
	</div>
{/if}

<style lang="scss">
	.channel-messages {
		@apply overflow-y-scroll p-2 flex flex-col-reverse;
	}
</style>
