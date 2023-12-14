<script lang="ts">
    import { fetchApi } from "$lib/api";
    import { joinedTopics } from "$lib/stores/";
    import { Modal, ModalActionButton, ModalActions, ModalTitle } from "$lib/components/modals";
    import type { TopicInterface } from "$lib/types";

    export let isModalOpen: boolean;
    export let topic: TopicInterface;

    function handleTopicLeave() {
        isModalOpen = false;

        fetchApi(`topics/${topic.slug}/leave/`, {
            method: "POST"
        }).then((response) => {
            if (response.ok) {
                topic.is_member = false;
                joinedTopics.update((topics) => {
                    return topics.filter((t) => t.slug !== topic.slug);
                });
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
        <ModalActionButton size="btn-lg" isDestructive on:click={handleTopicLeave}
            >Leave</ModalActionButton
        >
        <ModalActionButton size="btn-lg" on:click={() => (isModalOpen = false)}
            >Cancel</ModalActionButton
        >
    </ModalActions>
</Modal>
