<script lang="ts">
    import { removeToast, toastStore } from "$lib/stores";
    import { quintOut } from "svelte/easing";
    import { crossfade, fade, scale, slide } from "svelte/transition";
    import { flip } from "svelte/animate";

    const [send, receive] = crossfade({
        fallback(node, params) {
            const style = getComputedStyle(node);
            const transform = style.transform === "none" ? "" : style.transform;

            return {
                duration: 600,
                easing: quintOut,
                css: (t) => `
					transform: ${transform} ;
					opacity: ${t}
				`
            };
        }
    });
</script>

<div id="toast-group" class:active={$toastStore.length > -1}>
    {#each $toastStore as toast (toast.id)}
        {@const toastType = toast.type || "info"}
        <button
            class="toast toast-start items-center flex-row {toastType}"
            on:click={() => removeToast(toast.id)}
            animate:flip
            in:send={{ key: toast.id }}
            out:receive={{ key: toast.id }}
        >
            <div class="icon">
                {#if toast.icon}
                    {toast.icon}
                {:else if toastType === "info"}<svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 512 512"
                        ><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                            d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"
                        /></svg
                    >{:else if toastType === "error"}
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
                        ><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                            d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"
                        /></svg
                    >
                {:else if toastType === "success"}
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        ><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                            d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"
                        /></svg
                    >{/if}
            </div>

            <p class="text-white sm:p-1 md:p-3">
                {toast.message}
            </p>
        </button>
    {/each}
</div>

<style lang="scss">
    #toast-group {
        border: none;
        @apply fixed bottom-6 right-6 m-6 cursor-pointer gap-1
               transform translate-x-80 invisible opacity-0
               flex flex-col-reverse ease-in-out z-[999] duration-500;

        &.active {
            @apply translate-x-0 visible opacity-100;
        }

        :global(:nth-child(3)) {
            @apply opacity-75;
        }
        :global(:nth-child(4)) {
            @apply opacity-60;
        }
        :global(:nth-child(5)) {
            @apply opacity-40;
        }
        :global(:nth-child(n + 6)) {
            @apply opacity-0 invisible;
        }
    }

    .toast {
        @apply flex cursor-pointer border rounded-lg py-3 px-2
               bg-discordDark-860 transition-all z-[999];
    }

    .toast.success {
        @apply border-green-500;
    }

    .toast.error {
        @apply border-red-500;
    }

    .toast.info {
        @apply border-blue-500;
    }

    .icon {
        @apply fill-white size-9 text-lg pl-1 py-1 grid place-items-center;
    }
</style>
