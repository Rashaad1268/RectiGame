<script lang="ts">
    import type { HTMLButtonAttributes } from "svelte/elements";

    // export let isLoading: boolean | undefined = false;
    export const isLoading: boolean | undefined = false;

    interface $$Props extends HTMLButtonAttributes {
        isLoading?: boolean;
    }
</script>

<button on:click on:dblclick {...$$restProps}>
    <slot />
</button>

<style lang="scss">
    // Default button size is medium (md)
    button {
        @apply font-medium capitalize
      bg-green-500 w-auto box-border text-base rounded-md
        h-9 px-3 py-2 text-white whitespace-nowrap text-ellipsis overflow-hidden
        flex items-center justify-center select-none;

        // color: hsl(0 calc(1 * 0%) 100% / 1);
        transition: background-color 0.17s ease, color 0.17s ease;

        &:hover {
            @apply bg-green-600;
        }

        &:active {
            @apply bg-green-700;
        }

        &.btn-lg {
            @apply h-10 px-6 text-xl;
        }

        &.btn-xl {
            @apply h-12 px-8 text-2xl;
        }

        &.btn-sm {
            @apply h-8 px-2 text-sm;
        }

        &.btn-xs {
            @apply h-6 px-2 text-xs;
        }
    }

    .btn-destructive {
        @apply bg-red-500;

        &:hover {
            @apply bg-red-600;
        }
        &:active {
            @apply bg-red-700;
        }
    }

    .btn-blue {
        @apply bg-blue-500;

        &:hover {
            @apply bg-blue-600;
        }
        &:active {
            @apply bg-blue-700;
        }
    }

    .btn-dark {
        @apply bg-neutral-700;

        &:hover {
            @apply bg-neutral-800;
        }
        &:active {
            @apply bg-neutral-900;
        }
    }
</style>
