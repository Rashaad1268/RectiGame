<script lang="ts">
	import { fetchApi, formatApiErrors } from '$lib/api';
	import { Form, TextArea, TextField } from '$lib/components/forms';

	import { Modal, ModalActionButton, ModalActions, ModalTitle } from '$lib/components/modals';
	import { topicPosts } from '$lib/stores';
	import type { TopicInterface } from '$lib/types';

	export let isModalOpen: boolean;
	export let topic: TopicInterface;

	let title: string = '';
	let content: string = '';
	let errorMessages: string[] = [];

	async function handlePostCreate() {
		if (!title || !content) {
			errorMessages = [...errorMessages, 'The title and content cannot be empty'];
		}

		fetchApi(`posts/`, {
			method: 'POST',
			body: JSON.stringify({
				topic: topic.slug,
				title,
				content
			})
		}).then((response) => {
			response.json().then((newPostData) => {
				if (response.ok) {
					topicPosts.update((oldTopicPosts) => {
						const newTopicPosts = { ...oldTopicPosts };
						newTopicPosts[newPostData.topic].results = [
							newPostData,
							...newTopicPosts[newPostData.topic].results
						];

						return newTopicPosts;
					});

					isModalOpen = false;
					// Clear all the related state when a post is successfully created
					title = '';
					content = '';
					errorMessages = [];
				} else {
					// If the creation failed, show the errors returned from the api
					errorMessages = formatApiErrors(newPostData);
				}
			});
		});
	}
</script>

<Modal bind:isOpen={isModalOpen}>
	<ModalTitle>Create a post</ModalTitle>

	<Form bind:errorMessages>
		<label for="title">Title</label>
		<TextField
			id="title"
			bind:value={title}
			name="title"
			type="text"
			placeholder="Title"
			required
		/>

		<label for="content">Content</label>
		<TextArea
			id="content"
			bind:value={content}
			name="content"
			type="text"
			placeholder="Content"
			required
		/>
	</Form>

	<ModalActions>
		<ModalActionButton isDestructive on:click={() => (isModalOpen = false)}
			>Cancel</ModalActionButton
		>
		<ModalActionButton on:click={handlePostCreate}>Submit</ModalActionButton>
	</ModalActions>
</Modal>
