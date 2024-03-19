<script lang="ts">
    import { fetchApi, formatApiErrors } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { Form } from "$lib/components/forms";
    import TextArea from "$lib/components/forms/textArea.svelte";
    import TextField from "$lib/components/forms/textField.svelte";
    import { Modal, ModalActions } from "$lib/components/modals";
    import type { TopicInterface, TopicRoomInterface } from "$lib/types";
    import { joinedTopicRooms } from "$lib/stores/";
    import { goto } from "$app/navigation";

    export let isOpen: boolean;

    export let roomInviteCode = "";

    let errorMessages: string[] = [];

    async function joinRoom() {
        const response = await fetchApi(`channels/rooms/${roomInviteCode}/join/`, {
            method: "POST"
        });

        if (response.ok) {
            const newlyJoinedRoom = (await response.json()) as TopicRoomInterface;

            joinedTopicRooms.update((joinedRooms) => {
                if (joinedRooms[newlyJoinedRoom.topic]) {
                    joinedRooms[newlyJoinedRoom.topic].push(newlyJoinedRoom);
                } else {
                    joinedRooms[newlyJoinedRoom.topic] = [newlyJoinedRoom];
                }
                
                return joinedRooms;
            });

            goto(`/topics/${newlyJoinedRoom.topic}/channel/${newlyJoinedRoom.id}/`)
            isOpen = false;
        }
    }

    $: {
        if (!isOpen) {
            // Clear up the inputs
            roomInviteCode = "";
        }
    }
</script>

<Modal bind:isOpen>
    <Form on:submit={joinRoom} bind:errorMessages>
        <h1 class="text-2xl mb-4">Join a room</h1>

        <label for="room-invite-code" class="text-lg">Room invite code</label>
        <TextField
            id="room-invite-code"
            placeholder="cyL7srY7"
            autocomplete="off"
            bind:value={roomInviteCode}
        />

        <ModalActions class="pt-3">
            <Button class="btn-dark" type="button" on:click={() => (isOpen = false)}>Cancel</Button>
            <Button type="submit" class="btn-green">Join room</Button>
        </ModalActions>
    </Form>
</Modal>
