<script lang="ts">
    import { fetchApi } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { joinedTopics, socket } from "$lib/stores/";
    import type { TopicInterface } from "$lib/types";
    import { trimText } from "$lib/utils";
    import type { PageData } from "./$types";
    import CreatePostModal from "./createPostModal.svelte";
    import TopicLeaveModal from "./topicLeaveModal.svelte";
    import TopicPostsList from "./topicPostsList.svelte";

    export let data: PageData;
    let isLeavingModalOpen = false;
    let isCreatePostModelOpen = false;

    $: topic = data.topic as TopicInterface;

    const dateTimeFormatter = new Intl.DateTimeFormat("en", {
        year: "numeric",
        month: "long",
        day: "numeric"
    });

    function handleTopicJoin() {
        if (topic.is_member) {
            isLeavingModalOpen = true;
            return;
        } else {
            fetchApi(`topics/${topic.slug}/join/`, {
                method: "POST"
            }).then((response) => {
                if (response.ok) {
                    topic.is_member = true;
                    joinedTopics.update((topics) => {
                        topics[topic.slug] = topic;

                        return topics;
                    });

                    $socket?.sendQueued(
                        JSON.stringify({ a: "SUBSCRIBE_TO_TOPIC", d: { topic_slug: topic.slug } })
                    );
                }
            });
        }
    }
</script>

<div class="flex flex-col">
    {#if topic.banner}
        <img src={topic.banner} class="w-full object-cover" alt="banner" />
    {/if}
    <div class="flex gap-4 md:gap-8 w-full pt-4">
        <img
            src={topic.image}
            class="w-32 h-32 rounded self-start object-contain"
            alt="topic img"
        />

        <div>
            <div>
                <div class="flex items-center">
                    <h1 class="text-2xl">
                        {topic.name}
                    </h1>

                    <Button
                        aria-label="leave topic button"
                        on:click={handleTopicJoin}
                        class="{topic.is_member ? 'btn-destructive' : ''} btn-sm ml-5"
                    >
                        {topic.is_member ? "Leave Topic" : "Join Topic"}
                    </Button>
                </div>

                <div class="flex items-center gap-3 mt-1">
                    <h6 class="text-[0.9rem] text-discordDark-300 leading-[0.5rem] ml-[3px]">
                        t/{topic.slug}
                    </h6>
                    <span class="select-none">•</span>
                    <div class="topic-tags">
                        {#each topic.tags as tag (tag.slug)}
                            <span class="topic-tag">{tag.name}</span>
                        {/each}
                    </div>
                </div>
            </div>

            <p class="mt-3">{trimText(topic.description, 100)}</p>
            <div class="mt-3 flex gap-5 items-center">
                {#if topic.is_member}
                    <Button
                        class="btn-sm btn-blue flex !rounded-3xl"
                        on:click={() => (isCreatePostModelOpen = !isCreatePostModelOpen)}
                        >Create Post</Button
                    >
                    <a href="/topics/{topic.slug}/channel" class="link link-hover"
                        >View topic chat</a
                    >
                {/if}
            </div>
        </div>
    </div>
</div>

<div class="mt-12 mb-6">
    <TopicPostsList bind:topic />
</div>

<TopicLeaveModal bind:isModalOpen={isLeavingModalOpen} bind:topic />

<CreatePostModal bind:isModalOpen={isCreatePostModelOpen} bind:topic />
