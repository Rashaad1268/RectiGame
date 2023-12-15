<script lang="ts">
    import UserProfilePreview from "$lib/components/userProfilePreview.svelte";
    import type { TopicChatMessageInterface } from "$lib/types";
    import { createPopperActions } from "svelte-popperjs";
    import { fade } from "svelte/transition";

    const [popperRef, popperContent] = createPopperActions({
        placement: "right",
        strategy: "fixed"
    });
    const extraOpts = {
        modifiers: [{ name: "offset", options: { offset: [0, 8] } }]
    };

    export let message: TopicChatMessageInterface;
    export let isInline: boolean;

    const timeFormatter = new Intl.DateTimeFormat("en");

    let showUserProfilePreview = false;
</script>

{#if showUserProfilePreview}
    <div class="bg-discordDark-860" use:popperContent={extraOpts} in:fade|global>
        My tooltip
        <div id="arrow" data-popper-arrow />
        <UserProfilePreview user={message.author} />
    </div>
{/if}

<div class="message" class:inline-msg={isInline}>
    {#if !!message.author}
        <!-- {@debug isInline} -->
        <div class="profile-picture-wrapper">
            {#if !isInline}
                <button
                    use:popperRef
                    on:click={() => (showUserProfilePreview = !showUserProfilePreview)}
                >
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
                </button>
            {/if}
        </div>

        <div class="flex flex-col">
            {#if !isInline}
                <div class="flex items-center">
                    <span class="font-semibold">{message.author.username}</span>

                    {#if message.author.is_staff}
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="w-5 h-5 fill-blue-500 ml-1"
                            viewBox="0 -960 960 960"
                            ><path
                                d="M756-120 537-339l84-84 219 219-84 84Zm-552 0-84-84 276-276-68-68-28 28-51-51v82l-28 28-121-121 28-28h82l-50-50 142-142q20-20 43-29t47-9q24 0 47 9t43 29l-92 92 50 50-28 28 68 68 90-90q-4-11-6.5-23t-2.5-24q0-59 40.5-99.5T701-841q15 0 28.5 3t27.5 9l-99 99 72 72 99-99q7 14 9.5 27.5T841-701q0 59-40.5 99.5T701-561q-12 0-24-2t-23-7L204-120Z"
                            /></svg
                        >
                    {/if}

                    <span class="text-neutral-400 text-[12px] ml-2"
                        >{timeFormatter.format(new Date(message.created_at))}</span
                    >
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
