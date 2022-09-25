<script lang="ts">
	import type { TopicInterface } from '$lib/types';
	import type { PageData } from './$types';
	import {Modal, ModalTitle, ModalActions, ModalActionButton} from "$lib/components/modals";

	export let data: PageData;
	let isLeavingModalOpen = false;
	let leaveModalCancelBtn: any;

	$: topic = data.topic as TopicInterface;

	const dateTimeFormatting = new Intl.DateTimeFormat('en', {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});

	function handleTopicJoin() {
		if (topic.is_member) {
			isLeavingModalOpen = true
			return;
		}
	}
</script>

<svelte:head>
	<title>{topic.name}</title>
</svelte:head>

<div class="flex flex-1 justify-between px-5">
	<div class="flex gap-4 md:gap-8">
		<img src={topic.image} class="w-32 rounded self-start" alt="topic img" />

		<div class="mt-5">
			<div class="flex items-center">
			<h1 class="text-3xl">
				{topic.name}
			</h1>
			<button
				on:click={handleTopicJoin}
				class="btn btn-sm {topic.is_member
					? 'btn-error'
					: 'btn-accent'}  ml-5">{topic.is_member ? 'Leave Topic' : 'Join Topic'}</button
			>
		</div>
			<p class="mt-1">{topic.description}</p>
		</div>
	</div>

	<div class="border border-primary hidden md:w-56 lg:w-64 md:flex md:flex-col">
		<h1 class="bg-primary text-black text-center font-semibold p-2">More Information</h1>
		<div class="p-4">
			<p>Created at: {dateTimeFormatting.format(Date.parse(topic.created_at))}</p>

			<div class="w-full flex-wrap mt-4">
				{#each topic.tags as tag}
					<a
						class="inline-block bg-zinc-700 rounded-full px-2 py-1 text-sm font-semibold mr-1 mb-1"
						href="/topics/tag/{tag.slug}">{tag.name}</a
					>
				{/each}
			</div>
		</div>
	</div>
</div>

<Modal bind:isOpen={isLeavingModalOpen} textAlign="center" initialFocus={leaveModalCancelBtn}>
	<ModalTitle>Are you sure that you want to leave the topic?</ModalTitle>

	<p>
		If you leave this topic you can re-join it later but you'll lose access
		to all the content that is only available to members
	</p>
	<ModalActions>

		<ModalActionButton isDestructive>Leave</ModalActionButton>
		<ModalActionButton on:click={() => isLeavingModalOpen = false} bind:this={leaveModalCancelBtn}>Cancel</ModalActionButton>

	</ModalActions>
</Modal>
