<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import type { TopicInterface, TopicRoomInterface, UserInterface } from "$lib/types";
    import { fetchApi, formatApiErrors } from "$lib/api";
    import { Form } from "$lib/components/forms";

    $: inviteCode = $page.params.invite_code;

    let room: TopicRoomInterface | null | undefined = undefined;
    let topic: TopicInterface | undefined;
    let inviter: UserInterface | undefined;
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

        if (room) {
            topic = await fetchAndHandleErr(`topics/${room?.topic}/`);
            inviter = await fetchAndHandleErr(`auth/users/${room.creator}/`);
        }
    });
</script>

<Form bind:errorMessages class="flex flex-col items-center justify-center h-full">
    {#if room && topic && inviter}
        <div class="flex">
            <img src={topic.image} alt="topic icon" class="size-64 object-contain" />

            <div>
                <h2 class="text-xl font-medium">
                    You are invited to join the room <strong>#{room.name}</strong>
                    <div>
                        <img src="" alt="">
                        created by {inviter.username}
                    </div>
                </h2>
                <h3>Under the topic {topic.name}</h3>
            </div>
        </div>
    {/if}
</Form>
