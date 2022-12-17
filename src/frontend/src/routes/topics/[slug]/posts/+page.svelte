<script lang="ts">
	import { fetchApi } from '$lib/api';
	import { joinedTopics } from '$lib/stores/';
	import type { TopicInterface } from '$lib/types';
	import TopicLeaveModal from '../topicLeaveModal.svelte';
	import type { PageData } from './$types';
	import TopicPostsList from './topicPostsList.svelte';

	export let data: PageData;
	let isLeavingModalOpen = false;

	$: topic = data.topic as TopicInterface;

	const dateTimeFormatting = new Intl.DateTimeFormat('en', {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});

	function handleTopicJoin() {
		if (topic.is_member) {
			isLeavingModalOpen = true;
			return;
		} else {
			fetchApi(`topics/${topic.slug}/join/`, {
				method: 'POST'
			}).then((response) => {
				if (response.ok) {
					topic.is_member = true;
					joinedTopics.update((topics) => {
						return [...topics, topic];
					});
				}
			});
		}
	}
</script>

<svelte:head>
	<title>{topic.name}</title>
</svelte:head>

<div class="w-full">
	<div class="flex">
		<div class="flex flex-col items-start">
			<div class="flex gap-4 md:gap-8">
				<img src={topic.image} class="w-32 rounded self-start" alt="topic img" />

				<div class="mt-5">
					<div class="flex items-center">
						<h1 class="text-3xl">
							{topic.name}
						</h1>
						<button
							on:click={handleTopicJoin}
							class="btn btn-sm {topic.is_member ? 'btn-error' : 'btn-accent'} ml-5"
						>
							{topic.is_member ? 'Leave Topic' : 'Join Topic'}
						</button>
					</div>

					<p class="mt-1">{topic.description}</p>
					<div class="mt-3">
						<a href="/topics/{topic.slug}" class="link link-hover">View topic chat</a>
					</div>
				</div>
			</div>

			<div class="ml-10">
				<TopicPostsList bind:topic />
			</div>
		</div>

		<!-- Hide this if the screen is larger than medium size -->
		<div
			class="border border-primary hidden md:w-56 lg:w-64 lg:flex flex-col min-h-[70vh] absolute right-1"
		>
			<h1 class="bg-primary text-black text-center font-semibold p-2">More Information</h1>
			<div class="p-4">
				<p>Created at: {dateTimeFormatting.format(Date.parse(topic.created_at))}</p>

				<div class="w-full flex-wrap mt-4">
					{#each topic.tags as tag (tag.slug)}
						<a
							class="inline-block bg-zinc-700 rounded-full px-2 py-1 text-sm font-semibold mr-1 mb-1"
							href="/topics/tag/{tag.slug}">{tag.name}</a>
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>

<TopicLeaveModal bind:isModalOpen={isLeavingModalOpen} bind:topic />
