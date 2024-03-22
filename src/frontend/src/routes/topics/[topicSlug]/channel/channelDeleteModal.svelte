<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { toast } from "svelte-sonner";
    import { fetchApi } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { ModalActions } from "$lib/components/modals";
    import Modal from "$lib/components/modals/modal.svelte";
    import { joinedTopics, messageStore } from "$lib/stores";
    import type { TopicChatChannelInterface, TopicInterface } from "$lib/types";

    export let topic: TopicInterface | undefined;
    export let channelToDelete: TopicChatChannelInterface | null;

    async function deleteChannel() {
        if (!channelToDelete || !topic) return;

        const response = await fetchApi(`channels/${channelToDelete.id}/`, { method: "DELETE" });

        if (response.ok) {
            joinedTopics.update((topics) => {
                topics[topic!.slug].channels = topics[topic!.slug]!.channels.filter(
                    (channel) => channel.id !== channelToDelete!.id
                );

                return topics;
            });

            messageStore.update((msgs) => {
                delete msgs[channelToDelete!.id];
                return msgs;
            });
            console.log($messageStore[channelToDelete!.id]);

            if (parseInt($page.params.channel_id) === channelToDelete.id) {
                // Redirect the user if he is currently viewing that channel
                goto(`/topics/${topic.slug}/channel/`);
            }

            channelToDelete = null;
        } else {
            toast.error("Failed to delete channel", {
                duration: 10000,
                description: `${response.statusText} ${response.status}`
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
