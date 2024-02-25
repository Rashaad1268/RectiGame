<script lang="ts">
    import Modal from "./modal.svelte";

    export let isOpen: boolean;
</script>

<Modal bind:isOpen>
    <div class="full-screen-modal-wrapper">
        <slot />
    </div>
    <button class="fixed right-8 top-8" on:click={() => (isOpen = false)}>X</button>
</Modal>

<style lang="postcss">
    .full-screen-modal-wrapper {
        @apply mt-9 min-h-screen min-w-[100vw] max-h-screen max-w-[100vw] overflow-x-hidden;
    }
</style>
