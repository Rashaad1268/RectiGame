<script lang="ts">
	import type { HTMLButtonAttributes } from 'svelte/elements';

    // export let isLoading: boolean | undefined = false;
    export const isLoading: boolean | undefined = false;

    interface $$Props extends HTMLButtonAttributes {
        isLoading?: boolean;
    }
</script>

<button on:click on:dblclick {...$$restProps}>
    <div class="contents">
        <slot />
    </div>
</button>

<style lang="scss">
    button {
        @apply /* py-4 px-10 */ text-xl text-white /* font-semibold uppercase fill-green-700 */
        bg-[#32b863] font-gg
        /* bg-gradient-to-br from-emerald-500 via-green-500 to-emerald-600 */ rounded-[3px]
        cursor-pointer h-[32px] w-auto box-border min-w-[60px] min-h-[32px]
        flex items-center justify-center py-0.5 px-4 select-none
        transition-[filter];
        /* --btn-shadow-size: 3px;;
        --btn-shadow-color: theme('colors.green.800');
        box-shadow: 0 var(--btn-shadow-size) 0 var(--btn-shadow-color); */
        transition: background-color .17s ease,color .17s ease;

        .contents {
            @apply my-0 mx-auto whitespace-nowrap text-ellipsis overflow-hidden;
        }

        &:hover {
            @apply brightness-[0.86];
        }

        &:active {
            @apply translate-y-[var(--btn-shadow-size)] shadow-none;
        }

        // &.btn-no-shadow {
        //     @apply shadow-none;
        // }

        &.btn-md {
            @apply py-0.5 px-3.5 text-base
            h-[28px] min-h-[28px] min-w-[54px];
        }

        &.btn-sm {
            @apply py-[1px] px-3 text-xs font-medium
            h-[24px] min-h-[24px] min-w-[48px];
        }

        &.btn-error {
            @apply bg-red-500;
            background-image: none;
            --btn-shadow-color: theme("colors.red.900");
        }
    }
</style>
