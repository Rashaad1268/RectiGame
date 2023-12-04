<script lang="ts">
	import { fetchApi } from '$lib/api';
	import type { PostInterface } from '$lib/types';
	import { spring } from 'svelte/motion';

	export let post: PostInterface;

	const displayed_net_likes = spring();
	$: displayed_net_likes.set(post.like_count - post.dislike_count);
	$: offset = modulo($displayed_net_likes, 1);

	function modulo(n: number, m: number) {
		// Handle negative numbers
		return ((n % m) + m) % m;
	}

	async function handleLike() {
		if (post.is_disliked) {
			post.is_disliked = false;
			post.dislike_count--;
		}

		if (!post.is_liked) {
			// Like the post if it is not liked
			fetchApi(`posts/${post.id}/like/`, { method: 'POST' }).then((_) => {
				post.is_liked = true;
				post.like_count++;
			});
		} else {
			// Unlike the post if it is liked
			fetchApi(`posts/${post.id}/unlike/`, { method: 'POST' }).then((_) => {
				post.is_liked = false;
				post.like_count--;
			});
		}
	}

	async function handleDisike() {
		if (post.is_liked) {
			post.is_liked = false;
			post.like_count--;
		}

		if (!post.is_disliked) {
			// Dislike the post of it is not disliked
			fetchApi(`posts/${post.id}/dislike/`, { method: 'POST' }).then((_) => {
				post.is_disliked = true;
				post.dislike_count++;
			});
		} else {
			// Undo the dislike if it is already disliked
			fetchApi(`posts/${post.id}/undo-dislike/`, { method: 'POST' }).then((_) => {
				post.is_disliked = false;
				post.dislike_count--;
			});
		}
	}
</script>

<div class="post">
	<div class="body">
		<div class="post-like-dislike-bar">
			<button aria-label="like button" on:click={handleLike} id="like-btn">
					{#if post.is_liked}
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" id="already-liked"
							><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
								d="M313.4 32.9c26 5.2 42.9 30.5 37.7 56.5l-2.3 11.4c-5.3 26.7-15.1 52.1-28.8 75.2H464c26.5 0 48 21.5 48 48c0 18.5-10.5 34.6-25.9 42.6C497 275.4 504 288.9 504 304c0 23.4-16.8 42.9-38.9 47.1c4.4 7.3 6.9 15.8 6.9 24.9c0 21.3-13.9 39.4-33.1 45.6c.7 3.3 1.1 6.8 1.1 10.4c0 26.5-21.5 48-48 48H294.5c-19 0-37.5-5.6-53.3-16.1l-38.5-25.7C176 420.4 160 390.4 160 358.3V320 272 247.1c0-29.2 13.3-56.7 36-75l7.4-5.9c26.5-21.2 44.6-51 51.2-84.2l2.3-11.4c5.2-26 30.5-42.9 56.5-37.7zM32 192H96c17.7 0 32 14.3 32 32V448c0 17.7-14.3 32-32 32H32c-17.7 0-32-14.3-32-32V224c0-17.7 14.3-32 32-32z"
							/></svg
						>
						{:else}
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" id="like"
						><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
							d="M323.8 34.8c-38.2-10.9-78.1 11.2-89 49.4l-5.7 20c-3.7 13-10.4 25-19.5 35l-51.3 56.4c-8.9 9.8-8.2 25 1.6 33.9s25 8.2 33.9-1.6l51.3-56.4c14.1-15.5 24.4-34 30.1-54.1l5.7-20c3.6-12.7 16.9-20.1 29.7-16.5s20.1 16.9 16.5 29.7l-5.7 20c-5.7 19.9-14.7 38.7-26.6 55.5c-5.2 7.3-5.8 16.9-1.7 24.9s12.3 13 21.3 13L448 224c8.8 0 16 7.2 16 16c0 6.8-4.3 12.7-10.4 15c-7.4 2.8-13 9-14.9 16.7s.1 15.8 5.3 21.7c2.5 2.8 4 6.5 4 10.6c0 7.8-5.6 14.3-13 15.7c-8.2 1.6-15.1 7.3-18 15.2s-1.6 16.7 3.6 23.3c2.1 2.7 3.4 6.1 3.4 9.9c0 6.7-4.2 12.6-10.2 14.9c-11.5 4.5-17.7 16.9-14.4 28.8c.4 1.3 .6 2.8 .6 4.3c0 8.8-7.2 16-16 16H286.5c-12.6 0-25-3.7-35.5-10.7l-61.7-41.1c-11-7.4-25.9-4.4-33.3 6.7s-4.4 25.9 6.7 33.3l61.7 41.1c18.4 12.3 40 18.8 62.1 18.8H384c34.7 0 62.9-27.6 64-62c14.6-11.7 24-29.7 24-50c0-4.5-.5-8.8-1.3-13c15.4-11.7 25.3-30.2 25.3-51c0-6.5-1-12.8-2.8-18.7C504.8 273.7 512 257.7 512 240c0-35.3-28.6-64-64-64l-92.3 0c4.7-10.4 8.7-21.2 11.8-32.2l5.7-20c10.9-38.2-11.2-78.1-49.4-89zM32 192c-17.7 0-32 14.3-32 32V448c0 17.7 14.3 32 32 32H96c17.7 0 32-14.3 32-32V224c0-17.7-14.3-32-32-32H32z"
						/></svg>
					{/if}
			</button>

				<div class="net-likes-counter-viewport">
					<div class="counter-net-likes-counter" style="transform: translate(0, {100 * offset}%)">
						<strong class="top-[-100%] select-none" aria-hidden="true">{Math.floor($displayed_net_likes + 1)}</strong>
						<strong>{Math.floor($displayed_net_likes)}</strong>
					</div>
				</div>
	
			<button aria-label="dislike button" on:click={handleDisike} id="dislike-btn">
					{#if post.is_disliked}
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" id="already-disliked"
							><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
								d="M313.4 479.1c26-5.2 42.9-30.5 37.7-56.5l-2.3-11.4c-5.3-26.7-15.1-52.1-28.8-75.2H464c26.5 0 48-21.5 48-48c0-18.5-10.5-34.6-25.9-42.6C497 236.6 504 223.1 504 208c0-23.4-16.8-42.9-38.9-47.1c4.4-7.3 6.9-15.8 6.9-24.9c0-21.3-13.9-39.4-33.1-45.6c.7-3.3 1.1-6.8 1.1-10.4c0-26.5-21.5-48-48-48H294.5c-19 0-37.5 5.6-53.3 16.1L202.7 73.8C176 91.6 160 121.6 160 153.7V192v48 24.9c0 29.2 13.3 56.7 36 75l7.4 5.9c26.5 21.2 44.6 51 51.2 84.2l2.3 11.4c5.2 26 30.5 42.9 56.5 37.7zM32 384H96c17.7 0 32-14.3 32-32V128c0-17.7-14.3-32-32-32H32C14.3 96 0 110.3 0 128V352c0 17.7 14.3 32 32 32z"
							/></svg
						>
					{:else}
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" id="dislike"
							><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
								d="M323.8 477.2c-38.2 10.9-78.1-11.2-89-49.4l-5.7-20c-3.7-13-10.4-25-19.5-35l-51.3-56.4c-8.9-9.8-8.2-25 1.6-33.9s25-8.2 33.9 1.6l51.3 56.4c14.1 15.5 24.4 34 30.1 54.1l5.7 20c3.6 12.7 16.9 20.1 29.7 16.5s20.1-16.9 16.5-29.7l-5.7-20c-5.7-19.9-14.7-38.7-26.6-55.5c-5.2-7.3-5.8-16.9-1.7-24.9s12.3-13 21.3-13L448 288c8.8 0 16-7.2 16-16c0-6.8-4.3-12.7-10.4-15c-7.4-2.8-13-9-14.9-16.7s.1-15.8 5.3-21.7c2.5-2.8 4-6.5 4-10.6c0-7.8-5.6-14.3-13-15.7c-8.2-1.6-15.1-7.3-18-15.2s-1.6-16.7 3.6-23.3c2.1-2.7 3.4-6.1 3.4-9.9c0-6.7-4.2-12.6-10.2-14.9c-11.5-4.5-17.7-16.9-14.4-28.8c.4-1.3 .6-2.8 .6-4.3c0-8.8-7.2-16-16-16H286.5c-12.6 0-25 3.7-35.5 10.7l-61.7 41.1c-11 7.4-25.9 4.4-33.3-6.7s-4.4-25.9 6.7-33.3l61.7-41.1c18.4-12.3 40-18.8 62.1-18.8H384c34.7 0 62.9 27.6 64 62c14.6 11.7 24 29.7 24 50c0 4.5-.5 8.8-1.3 13c15.4 11.7 25.3 30.2 25.3 51c0 6.5-1 12.8-2.8 18.7C504.8 238.3 512 254.3 512 272c0 35.3-28.6 64-64 64l-92.3 0c4.7 10.4 8.7 21.2 11.8 32.2l5.7 20c10.9 38.2-11.2 78.1-49.4 89zM32 384c-17.7 0-32-14.3-32-32V128c0-17.7 14.3-32 32-32H96c17.7 0 32 14.3 32 32V352c0 17.7-14.3 32-32 32H32z"
							/></svg
						>
					{/if}
			</button>
		</div>

		<!-- <a href="posts/{post.id}"> -->
		<div>
			<span class="text-xs sm:text-sm text-gray-300">Posted by {post.author.username}</span>
			<h2 class="text-2xl sm:text-3xl font-semibold">{post.title}</h2>
			<p class="text-sm sm:text-base">{post.content}</p>
		</div>
		<!-- </a> -->
	</div>

	<div class="post-actions">
		<svg viewBox="0 0 24 24" aria-hidden="true"
			><g
				><path
					d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.37 2.77 6.08 6.138 6.01l.351-.01h1.761v2.3l5.087-2.81c1.951-1.08 3.163-3.13 3.163-5.36 0-3.39-2.744-6.13-6.129-6.13H9.756z"
				/></g
			></svg
		>
	</div>
</div>

<style lang="scss">
	.post {
		@apply bg-discordDark-760 shadow-xl py-3 pr-3;

		.body {
			@apply flex gap-1;
		}
	}

	.post-actions {
		@apply border-t border-t-zinc-900 p-1 flex justify-around items-center;

		svg {
			@apply h-6 w-6 fill-gray-600;
		}
	}

	.post-like-dislike-bar {
		@apply flex flex-col justify-start items-center text-gray-400;
		svg {
			@apply h-6 w-6 fill-gray-400;

			&#like:hover {@apply fill-green-500;}
			&#already-liked {@apply fill-green-500;}
			&#dislike:hover {@apply fill-blue-500;}
			&#already-disliked {@apply fill-blue-500;}
		}

		#like-btn, #dislike-btn {
			@apply p-2 mx-2;
			&:hover {
				@apply bg-gray-700
			}
		}
	}

	.net-likes-counter-viewport {
		@apply text-center overflow-hidden relative h-6 w-6;

		strong {
			@apply absolute h-full w-full flex items-center justify-center;
		}

		.counter-net-likes-counter {
			@apply absolute h-full w-full;
		}
	}
</style>
