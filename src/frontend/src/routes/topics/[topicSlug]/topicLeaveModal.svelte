<script lang="ts">
    import { fetchApi } from "$lib/api";
    import { joinedTopics, socket } from "$lib/stores/";
    import { Modal, ModalActions, ModalTitle } from "$lib/components/modals";
    import type { TopicInterface } from "$lib/types";
    import Button from "$lib/components/button.svelte";

    export let isModalOpen: boolean;
    export let topic: TopicInterface;

    function handleTopicLeave() {
        isModalOpen = false;

        fetchApi(`topics/${topic.slug}/leave/`, {
            method: "POST"
        }).then((response) => {
            if (response.ok) {
                topic.is_member = false;
                topic.me = undefined;
                joinedTopics.update((topics) => {
                    delete topics[topic.slug];
                    return topics;
                });

                $socket?.sendQueued(
                    JSON.stringify({ a: "UNSUBSCRIBE_FROM_TOPIC", d: { topic_slug: topic.slug } })
                );
            }
        });
    }
</script>

<Modal bind:isOpen={isModalOpen}>
    <ModalTitle>Are you sure that you want to leave the topic?</ModalTitle>

    <p>
        If you leave this topic you can re-join it later but you'll lose access to all the content
        that is only available to members
    </p>

    <ModalActions>
        <Button class="btn-dark" on:click={() => (isModalOpen = false)}>Cancel</Button>
        <Button class="btn-destructive" on:click={handleTopicLeave}>Leave</Button>
    </ModalActions>
</Modal>
