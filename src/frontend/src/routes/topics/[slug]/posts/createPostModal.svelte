<script lang="ts">
	import { fetchApi } from '$lib/api';
	// import { joinedTopics } from '$lib/stores/';
	import { Modal, ModalActionButton, ModalActionTextArea, ModalActionTextField, ModalActions, ModalTitle } from '$lib/components/modals';
	import type { TopicInterface } from '$lib/types';

	export let isModalOpen: boolean;
	export let topic: TopicInterface;

    let title: string = "";
    let content: string = "";

	function handlePostCreate() {
		isModalOpen = false;

		fetchApi(`posts/`, {
			method: 'POST',
            body: JSON.stringify({
                topic: topic.slug,
                title,
                content
            })
		}).then((response) => {
			if (response.ok) {
				// append to posts
			}
		});
	}
</script>

<Modal bind:isOpen={isModalOpen}>
	<ModalTitle>Create a post</ModalTitle>

    Title
	<ModalActionTextField type="text" bind:value={title} />

    Content
    <ModalActionTextArea bind:value={content} />
	<ModalActions>
		<ModalActionButton isDestructive on:click={handlePostCreate}>Submit</ModalActionButton>
		<ModalActionButton on:click={() => (isModalOpen = false)}>Cancel</ModalActionButton>
	</ModalActions>
</Modal>
