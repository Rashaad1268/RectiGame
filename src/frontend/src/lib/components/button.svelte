<script lang="ts">
	import type { HTMLButtonAttributes } from 'svelte/elements';

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
button {
    @apply py-4 px-10 text-xl text-black font-semibold uppercase fill-green-700
       bg-gradient-to-br from-emerald-500 via-green-500 to-emerald-600 rounded-lg
       transition-[filter];
    --btn-shadow-size: 3px;;
    --btn-shadow-color: theme('colors.green.800');
    box-shadow: 0 var(--btn-shadow-size) 0 var(--btn-shadow-color);

    &:hover {
        @apply brightness-[0.86];
    }

    &:active {
        @apply translate-y-[var(--btn-shadow-size)] shadow-none;
    }

    &.btn-no-shadow {
        @apply shadow-none;
    }

    &.btn-md {
        @apply py-2 px-5 text-base;
    }

    &.btn-sm {
        @apply py-[6px] px-2 text-xs font-medium;
    }

    &.btn-error {
        @apply bg-red-500;
        background-image: none;
        --btn-shadow-color: theme("colors.red.900");
    }
}
</style>
