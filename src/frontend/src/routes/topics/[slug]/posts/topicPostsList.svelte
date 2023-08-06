<script lang="ts">
	import { fetchApi } from '$lib/api';
	import { topicPosts } from '$lib/stores/posts';
	import type { PostInterface, TopicInterface } from '$lib/types';
	import PostCard from './postCard.svelte';
	import {browser} from "$app/environment"


	export let topic: TopicInterface;

	$: postsPaginator = $topicPosts[topic.slug];

	$: {
		if (browser) {
			if (!postsPaginator && document) {
				fetchApi(`posts/?topic=${topic.slug}`).then(async (response) => {
					if (response.ok) {
						const data = await response.json();
						console.log('data', data);
						topicPosts.update((posts) => {
							return {
								...posts,
								[topic.slug]: data
							};
						});
					}
				});
			}
		}
	}
</script>

<div class="posts-list">
	{#each postsPaginator?.results || [] as post (post.id)}
		<PostCard {post} />
	{:else}
		<span class="text-center text-3xl font-semibold">There are no posts...for now</span>
	{/each}
</div>

<style lang="scss">
	.posts-list {
		@apply w-[55svw] flex gap-8 flex-col;
	}
</style>