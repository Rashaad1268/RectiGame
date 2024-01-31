<script lang="ts">
    import { fetchApi } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { ModalActions } from "$lib/components/modals";
    import Modal from "$lib/components/modals/modal.svelte";
    import { addToast, channelStore } from "$lib/stores";
    import type { TopicChatChannelInterface, TopicInterface } from "$lib/types";

    export let topic: TopicInterface | undefined;
    export let channelToDelete: TopicChatChannelInterface | null;

    async function deleteChannel() {
        console.log(channelToDelete)
        console.log(topic)
        if (!channelToDelete || !topic) return;

        const response = await fetchApi(`channels/${channelToDelete.id}/`, { method: "DELETE" });

        if (response.ok) {
            channelStore.update((channels) => {
                channels[topic!.slug] = channels[topic!.slug]!.filter(
                    (c) => c.id !== channelToDelete!.id
                );

                return channels;
            });
            channelToDelete = null;
        } else {
            addToast({
                type: "error",
                delay: 10000,
                message: `Failed to delete channel. ${response.statusText} ${response.status}`
            });
        }
    }
</script>

<Modal isOpen={!!channelToDelete}>
    <h1 class="text-2xl">Delete channel</h1>
    <h3>
        Are you sure you want to delete #{channelToDelete?.name}.
        <p>This action cannot be undone</p>
    </h3>

    <ModalActions class="pt-3">
        <Button class="btn-dark" on:click={() => (channelToDelete = null)}>Cancel</Button>
        <Button class="btn-destructive" on:click={deleteChannel}>Delete channel</Button>
    </ModalActions>
</Modal>
