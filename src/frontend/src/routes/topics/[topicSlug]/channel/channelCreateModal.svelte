<script lang="ts">
    import { fetchApi, formatApiErrors } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { Form } from "$lib/components/forms";
    import TextArea from "$lib/components/forms/textArea.svelte";
    import TextField from "$lib/components/forms/textField.svelte";
    import { Modal, ModalActions } from "$lib/components/modals";
    import type { TopicInterface } from "$lib/types";
    import { joinedTopics } from "$lib/stores/";

    export let isOpen: boolean;
    export let topic: TopicInterface | undefined;

    export let channelName = "";
    export let channelDescription = "";

    let errorMessages: string[] = [];

    async function createChannel() {
        if (!topic) return; // for whatever reason ¯\_(ツ)_/¯

        channelName = channelName.trim();
        channelDescription = channelDescription.trim();

        if (!channelName) {
            isOpen = false;
            return;
        }

        const resp = await fetchApi("channels/", {
            method: "POST",
            body: JSON.stringify({
                topic: topic.slug,
                name: channelName,
                description: channelDescription
            })
        });

        if (resp.ok) {
            // the channel will be added to the store by the ws event handler
            isOpen = false;
        } else {
            errorMessages = formatApiErrors(await resp.json());
        }
    }

    $: {
        if (!isOpen) {
            // Clear up the inputs
            channelName = "";
            channelDescription = "";
        }
    }
</script>

<Modal bind:isOpen>
    <Form on:submit={createChannel} bind:errorMessages>
        <h1 class="text-2xl">Create a new channel</h1>
        <h3 class="mb-4">for the topic {topic?.name}</h3>

        <label for="channel-name" class="text-lg">Channel name</label>
        <div class="flex items-center gap-2 mb-2">
            <span class="font-semibold text-2xl">#</span>
            <TextField
                id="channel-name"
                placeholder="test-channel"
                autocomplete="off"
                bind:value={channelName}
            />
        </div>

        <label for="channel-description" class="text-lg">Channel description</label>
        <TextArea
            id="channel-description"
            placeholder="description (optional)"
            bind:value={channelDescription}
        />

        <ModalActions class="pt-3">
            <Button class="btn-destructive" type="button" on:click={() => (isOpen = false)}
                >Cancel</Button
            >
            <Button type="submit" class="btn-blue">Create channel</Button>
        </ModalActions>
    </Form>
</Modal>
