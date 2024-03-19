<script lang="ts">
    import { fetchApi, formatApiErrors } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { Form } from "$lib/components/forms";
    import TextArea from "$lib/components/forms/textArea.svelte";
    import TextField from "$lib/components/forms/textField.svelte";
    import { Modal, ModalActions } from "$lib/components/modals";
    import type { TopicInterface } from "$lib/types";
    import { joinedTopicRooms } from "$lib/stores/";

    export let isOpen: boolean;
    export let topic: TopicInterface | undefined;

    export let roomName = "";
    export let roomDescription = "";

    let errorMessages: string[] = [];

    async function createChannel() {
        if (!topic) return; // for whatever reason ¯\_(ツ)_/¯

        roomName = roomName.trim();
        roomDescription = roomDescription.trim();

        if (!roomName) {
            isOpen = false;
            return;
        }

        const resp = await fetchApi("channels/rooms/", {
            method: "POST",
            body: JSON.stringify({
                topic: topic.slug,
                name: roomName,
                description: roomDescription
            })
        });

        if (resp.ok) {
            isOpen = false;

            const newRoom = await resp.json();

            joinedTopicRooms.update((joinedRooms) => {
                if (joinedRooms[newRoom.topic]) {
                    joinedRooms[newRoom.topic].push(newRoom);
                } else {
                    joinedRooms[newRoom.topic] = [newRoom];
                }

                return joinedRooms;
            });
        } else {
            errorMessages = formatApiErrors(await resp.json());
        }
    }

    $: {
        if (!isOpen) {
            // Clear up the inputs
            roomName = "";
            roomDescription = "";
        }
    }
</script>

<Modal bind:isOpen>
    <Form on:submit={createChannel} bind:errorMessages>
        <h1 class="text-2xl">Create a new private room</h1>
        <h3 class="mb-4">for the topic {topic?.name}</h3>

        <label for="room-name" class="text-lg">Room name</label>
        <div class="flex items-center gap-2 mb-2">
            <span class="font-semibold text-2xl">#</span>
            <TextField
                id="room-name"
                placeholder="test-room"
                autocomplete="off"
                bind:value={roomName}
            />
        </div>

        <label for="room-description" class="text-lg">Room description</label>
        <TextArea
            id="room-description"
            placeholder="description (optional)"
            bind:value={roomDescription}
        />

        <ModalActions class="pt-3">
            <Button class="btn-destructive" type="button" on:click={() => (isOpen = false)}
                >Cancel</Button
            >
            <Button type="submit" class="btn-blue">Create Room</Button>
        </ModalActions>
    </Form>
</Modal>
