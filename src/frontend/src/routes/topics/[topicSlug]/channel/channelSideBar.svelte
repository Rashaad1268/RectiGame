<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Button from "$lib/components/button.svelte";
    import { addToast, joinedTopics, userData } from "$lib/stores/";
    import type { TopicChatChannelInterface, TopicInterface } from "$lib/types";
    import { objIsEmpty } from "$lib/utils";
    import ChannelCreateModal from "./channelCreateModal.svelte";
    import ChannelDeleteModal from "./channelDeleteModal.svelte";

    $: selectedTopicSlug = $page.params.topicSlug;

    // Get the topic from the joinedTopics cache
    $: topic = $joinedTopics[selectedTopicSlug] as TopicInterface | undefined;

    // In the initial load, the user data is still being fetched so the joinedTopics cache could be empty
    // in that case just set the channels to an empty array so nothing renders
    $: channels = topic?.channels || [];

    let isChannelCreateModalOpen = false;

    let channelToDelete: TopicChatChannelInterface | null = null;

    $: {
        if (!objIsEmpty($joinedTopics) && !topic) {
            /*
                This means that the user is trying to view the chat of a topic which
                they have not joined.

                Currently, we don't allow users to view channels without joining the topic
                but in the future it might be possible to add the feature of viewing the channels
                in a read-only mode
            */
            goto(`/topics/${selectedTopicSlug}`);
            addToast({delay: 10000, message: "You have to join a topic in order to view its chat" })
        }
    }
</script>

<div class="channel-sidebar">
    {#if !!topic}
        <header class="mb-3 pl-2">
            <h1 class="text-3xl font-semibold font-monocraft text-white">{topic.name}</h1>
            <a href="/topics/{topic.slug}" class="block my-1 link">View posts</a>

            {#if $userData?.is_staff}
                <Button
                    class="btn-xs btn-dark mt-4"
                    on:click={() => (isChannelCreateModalOpen = true)}>+ Create channel</Button
                >
            {/if}
        </header>

        <div class="w-full h-[1px] bg-discordDark-630 mb-2" />

        <div class="channels-container">
            {#each channels || [] as channel (channel.id)}
                <a
                    href="/topics/{topic.slug}/channel/{channel.id}"
                    class="channel-tab"
                    class:selected={parseInt($page.params.channel_id) === channel.id}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" height="15px" viewBox="0 0 448 512"
                        ><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
                            d="M181.3 32.4c17.4 2.9 29.2 19.4 26.3 36.8L197.8 128h95.1l11.5-69.3c2.9-17.4 19.4-29.2 36.8-26.3s29.2 19.4 26.3 36.8L357.8 128H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H347.1L325.8 320H384c17.7 0 32 14.3 32 32s-14.3 32-32 32H315.1l-11.5 69.3c-2.9 17.4-19.4 29.2-36.8 26.3s-29.2-19.4-26.3-36.8l9.8-58.7H155.1l-11.5 69.3c-2.9 17.4-19.4 29.2-36.8 26.3s-29.2-19.4-26.3-36.8L90.2 384H32c-17.7 0-32-14.3-32-32s14.3-32 32-32h68.9l21.3-128H64c-17.7 0-32-14.3-32-32s14.3-32 32-32h68.9l11.5-69.3c2.9-17.4 19.4-29.2 36.8-26.3zM187.1 192L165.8 320h95.1l21.3-128H187.1z"
                        /></svg
                    >
                    <span>{channel.name}</span>

                    {#if $userData?.is_staff}
                        <button
                            class="channel-delete-btn"
                            on:click={() => (channelToDelete = channel)}
                            ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                                ><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                                    d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"
                                /></svg
                            ></button
                        >
                    {/if}
                </a>
            {/each}
        </div>
    {/if}
</div>

<ChannelCreateModal bind:isOpen={isChannelCreateModalOpen} bind:topic />
<ChannelDeleteModal bind:channelToDelete bind:topic />

<style lang="scss">
    .channel-sidebar {
        @apply flex flex-col w-[165px] md:w-[260px] p-4 gap-[2px] bg-discordDark-800;

        // Setting height to 100% won't work in this case, so calculate it
        height: calc(100vh - var(--navbar-height));
    }

    .channels-container {
        @apply flex flex-col gap-[2px] overflow-y-auto;
    }

    .channel-tab {
        @apply flex text-discordDark-360 fill-discordDark-360
			   pl-6 py-1 rounded-md items-center gap-2 overflow-hidden whitespace-nowrap;

        &:hover {
            @apply bg-discordDark-660 text-discordDark-300;
        }

        &:not(.selected):active {
            // The effect when a tab which is not selected is :active
            @apply bg-discordDark-630 text-gray-200 brightness-90;
        }

        &.selected {
            @apply bg-discordDark-630 text-gray-200;
        }

        .channel-delete-btn {
            @apply ml-auto mr-4 opacity-0 size-3 fill-red-500;
        }

        &:hover > .channel-delete-btn {
            @apply opacity-100;
        }
    }
</style>
