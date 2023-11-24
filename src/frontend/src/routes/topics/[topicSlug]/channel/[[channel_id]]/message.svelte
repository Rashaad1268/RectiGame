<script lang="ts">
	import type { TopicChatMessageInterface } from "$lib/types";

    export let message: TopicChatMessageInterface;
    export let isInline: boolean;
</script>

<div class="message" class:inline-msg={isInline}>
	{#if !!message.author}
		<!-- {@debug isInline} -->
		<div class="profile-picture-wrapper">
			{#if !isInline}
				{#if !message.author.profile.profile_picture}
					<div class="bg-discordDark-600 flex items-center justify-center">
						<span>{message.author.username.slice(0, 1)}</span>
					</div>
				{:else}
					<img
						src={message.author.profile.profile_picture}
						alt="{message.author.username} profile"
					/>
				{/if}
			{/if}
		</div>

		<div class="flex flex-col">
			{#if !isInline}
				<div>
					<span class="font-semibold">{message.author.username}</span>
					<!-- <span>{timeFormatter.format(new Date(message.created_at))}</span> -->
				</div>
			{/if}
			<span>{message.content}</span>
		</div>
	{/if}
</div>

<style lang="scss">
    .message {
		@apply flex mt-2;

		.profile-picture-wrapper {
			@apply min-w-[40px] mr-3;

			img,
			div {
				@apply h-10 w-10 object-cover rounded-full mt-[4px] text-center;
			}
		}

		&:hover {
			@apply bg-discordDark-760;
		}
	}
</style>