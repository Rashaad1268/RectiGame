<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import type { TopicInterface, TopicChatRoomInterface, UserInterface } from "$lib/types";
    import { joinedTopics, joinedTopicRooms } from "$lib/stores";
    import { fetchApi, formatApiErrors } from "$lib/api";
    import { Form } from "$lib/components/forms";
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import Button from "$lib/components/button.svelte";
    import { toast } from "svelte-sonner";
    import { goto } from "$app/navigation";

    $: inviteCode = $page.params.invite_code;

    interface NewTopicChatRoomInterface extends TopicChatRoomInterface {
        is_member: boolean;
    }

    let room: NewTopicChatRoomInterface | null | undefined = undefined;
    let topic: TopicInterface | undefined;
    let roomCreator: UserInterface | undefined;
    let errorMessages: string[] = [];

    async function fetchAndHandleErr(endpoint: string, options?: RequestInit | undefined) {
        const response = await fetchApi(endpoint, options);

        if (response.ok) {
            return await response.json();
        } else {
            errorMessages = [...formatApiErrors(await response.json()), ...errorMessages];
        }
    }

    onMount(async () => {
        room = await fetchAndHandleErr(`channels/rooms/${inviteCode}/invite-details/`);

        if (!room) {
            return;
        } else if (room.is_member) {
            toast.info("You are already a member of this room");
            goto(`/topics/${room.topic}/channel/${room.id}`);

            return;
        } else {
            topic = await fetchAndHandleErr(`topics/${room?.topic}/`);
            roomCreator = await fetchAndHandleErr(`auth/users/${room.creator}/`);
        }
    });

    async function joinTopicRoom() {
        const response = await fetchApi(`channels/rooms/${inviteCode}/join/`, {
            method: "POST"
        });

        if (response.ok) {
            const newRoom = (await response.json()) as TopicChatRoomInterface;

            joinedTopicRooms.update((joinedRooms) => {
                if (joinedRooms[newRoom.topic]) {
                    joinedRooms[newRoom.topic].push(newRoom);
                } else {
                    joinedRooms[newRoom.topic] = [newRoom];
                }

                return joinedRooms;
            });

            joinedTopics.update((joinedTopics) => {
                // add the topic to the users joined topics
                // just in case they have not joined the rooms topic
                joinedTopics[topic!.slug] = topic!;
                return joinedTopics;
            });

            goto(`/topics/${newRoom.topic}/channel/${newRoom.id}/`);
        }
    }
</script>

<Form bind:errorMessages class="flex flex-col items-center justify-center h-full">
    {#if room && topic && roomCreator}
        <h1 class="text-2xl">
            You are invited to join the private room <strong>#{room.name}</strong>
        </h1>

        <h2 class="text-2xl">Created by</h2>
        <div class="info-card items-center justify-center px-4 py-2">
            <ProfilePicture user={roomCreator} class="size-12" />
            <div>
                <span class="text-lg font-medium">{roomCreator.username}</span>
            </div>
        </div>

        <h2 class="text-xl">in the topic</h2>
        <div class="info-card items-start">
            <img src={topic.image} class="object-contain h-28 rounded-l-lg" alt="topic" />

            <div class="my-4">
                <h2 class="text-xl font-semibold">{topic.name}</h2>
                <h3 class="text-sm text-gray-400 mb-2">t/{topic.slug}</h3>
                <div class="topic-tags">
                    {#each topic.tags as tag (tag.slug)}
                        <span class="topic-tag">{tag.name}</span>
                    {/each}
                </div>
            </div>
        </div>

        <Button class="font-monocraft text-xl btn-xl mt-4" on:click={joinTopicRoom}
            >Join Room</Button
        >
    {:else}
        <h1>Loading...</h1>
    {/if}
</Form>

<style lang="postcss">
    .info-card {
        @apply my-4 rounded-lg pr-16 flex gap-4 border
             bg-discordDark-800 border-discordDark-760;
    }
</style>
