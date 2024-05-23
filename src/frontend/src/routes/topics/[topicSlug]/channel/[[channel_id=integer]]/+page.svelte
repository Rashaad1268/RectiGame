<script lang="ts">
    import { page } from "$app/stores";
    import { fetchApi } from "$lib/api";
    import { joinedTopics, messageStore, userData, joinedTopicRooms } from "$lib/stores/";
    import Message from "./message.svelte";
    import type {
        TopicChatChannelInterface,
        TopicChatMessageInterface,
        TopicChatRoomInterface
    } from "$lib/types";
    import MessageInput from "./messageInput.svelte";
    import type { PageData } from "./$types";
    import Button from "$lib/components/button.svelte";
    import { toast } from "svelte-sonner";
    import RoomMemberList from "./roomMemberList.svelte";

    export let data: PageData;

    $: topicSlug = $page.params.topicSlug;
    $: selectedChannelId = parseInt($page.params.channel_id);

    $: channel = (
        !!$userData
            ? $joinedTopics[topicSlug]?.channels?.find((c) => c.id === selectedChannelId) ||
              ($joinedTopicRooms[topicSlug] || []).find((c) => c.id === selectedChannelId) ||
              null
            : undefined
    ) as
        | undefined // loading
        | null // channel not found
        | TopicChatChannelInterface;

    $: room = channel as TopicChatRoomInterface;

    $: isRoom = channel?.type === 2;
    $: messages = ($messageStore[channel?.id ?? -1] ?? {}).results;

    $: {
        if (channel && messages === undefined) {
            fetchApi(`channels/${channel!.id}/messages/`).then((response) => {
                response.json().then((fetchedMessages) => {
                    messageStore.update((msgs) => {
                        if (channel?.id) {
                            // channel can be undefined when the channel is deleted
                            msgs[channel.id] = fetchedMessages;
                        }
                        return msgs;
                    });
                });
            });
        }
    }

    let isFetchingNewMessages = false;

    function loadMessages(event: Event) {
        if (!channel || !messages) {
            return;
        }

        const element = event.target as HTMLDivElement;

        if (element.scrollHeight + element.scrollTop < 750) {
            if (!isFetchingNewMessages && messages.length !== $messageStore[channel!.id].count) {
                isFetchingNewMessages = true;
                fetchApi(
                    `channels/${channel!.id}/messages/?before=${messages[messages.length - 1].id}`
                ).then((response) => {
                    if (response.ok) {
                        response.json().then((data) => {
                            messageStore.update((existingMessages) => {
                                existingMessages[channel!.id].results?.push(...data.results);
                                return existingMessages;
                            });
                            isFetchingNewMessages = false;
                        });
                    }
                });
            }
        }
    }

    function calculateIsInlineMsg(idx: number, message: TopicChatMessageInterface): boolean {
        const msg = ($messageStore[channel!.id]?.results ?? [])[idx + 1];

        if (msg?.author?.user.id === message?.author.user.id) {
            const prevMsgCreatedAt = Date.parse(msg.created_at);
            const currentMsgCreatedAt = Date.parse(message.created_at);

            // Calculate the time gap between the 3 messages in seconds
            const diffInSeconds = Math.floor((currentMsgCreatedAt - prevMsgCreatedAt) / 1000);

            // if the time gap between the 2 messages from the same author is more than 5 minutes,
            // then it is not an inline message
            if (diffInSeconds > 300) {
                return false;
            }

            return true;
        }

        return false;
    }

    let messageContent = "";

    async function sendMessage(event: Event) {
        event.preventDefault(); // If this is not called the input will lose focus

        const finalMessageContent = messageContent.trim();

        if (!!channel && finalMessageContent) {
            const response = await fetchApi(`channels/${channel.id}/messages/`, {
                method: "POST",
                body: JSON.stringify({ content: finalMessageContent })
            });

            if (response.ok) {
                messageContent = "";
            }
        }
    }

    async function addRoomMember() {
        channel as TopicChatRoomInterface;
        const inviteLink = window.location.origin + `/invite/${room.invite_code}`;

        await navigator.clipboard.writeText(inviteLink);

        toast.success("Successfully copied room invite link to clipboard", {
            duration: 7000,
            action: {
                label: "Copy again",
                onClick: () => navigator.clipboard.writeText(inviteLink)
            }
        });
    }
</script>

{#if !selectedChannelId}
    <h1 class="text-3xl text-center font-semibold mt-[20dvh]">Select a channel to view</h1>
{:else if channel === undefined}
    Loading
{:else if channel === null}
    404 not found
{:else}
    <div class="flex h-full">
        <div
            class="flex flex-col justify-end bg-discordDark-730 max-h-[calc(100vh-var(--navbar-height))] h-full scroll-smooth pb-1 w-full"
        >
            <div
                class="flex border-b border-discordDark-600 items-center gap-2 text-lg font-medium
				   pl-8 py-3"
            >
                <span>
                    {data.topic.name}
                </span>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="14px"
                    fill="currentColor"
                    viewBox="0 0 384 512"
                    ><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
                        d="M3.4 81.7c-7.9 15.8-1.5 35 14.3 42.9L280.5 256 17.7 387.4C1.9 395.3-4.5 414.5 3.4 430.3s27.1 22.2 42.9 14.3l320-160c10.8-5.4 17.7-16.5 17.7-28.6s-6.8-23.2-17.7-28.6l-320-160c-15.8-7.9-35-1.5-42.9 14.3z"
                    /></svg
                >
                <span>
                    {channel.name}
                </span>

                <!-- Only show the room invite if the user is the creator of the topic or if the user is staff -->
                {#if isRoom && (room.creator === $userData?.id || $userData?.is_staff)}
                    <Button class="btn-dark btn-icon ml-2" on:click={addRoomMember}>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            height="16px"
                            width="16px"
                            viewBox="0 0 640 512"
                            ><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                                d="M96 128a128 128 0 1 1 256 0A128 128 0 1 1 96 128zM0 482.3C0 383.8 79.8 304 178.3 304h91.4C368.2 304 448 383.8 448 482.3c0 16.4-13.3 29.7-29.7 29.7H29.7C13.3 512 0 498.7 0 482.3zM504 312V248H440c-13.3 0-24-10.7-24-24s10.7-24 24-24h64V136c0-13.3 10.7-24 24-24s24 10.7 24 24v64h64c13.3 0 24 10.7 24 24s-10.7 24-24 24H552v64c0 13.3-10.7 24-24 24s-24-10.7-24-24z"
                            /></svg
                        >
                    </Button>
                {/if}
            </div>

            <div class="channel-messages" on:scroll={loadMessages}>
                {#each messages || [] as message, idx (message.id)}
                    {@const isInlineMsg = calculateIsInlineMsg(idx, message)}
                    <Message {message} isInline={isInlineMsg} />
                {/each}
            </div>

            <form on:submit={sendMessage} class="px-4">
                <MessageInput bind:value={messageContent} />
            </form>
        </div>

        {#if isRoom}
            <RoomMemberList channel={room} />
        {/if}
    </div>
{/if}

<style lang="scss">
    .channel-messages {
        @apply overflow-y-auto h-full p-2 flex flex-col-reverse;
    }
</style>
