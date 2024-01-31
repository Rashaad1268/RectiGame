<script lang="ts">
    import { removeToast } from "$lib/stores";
    import type { ToastInterface } from "$lib/types";
    import { onDestroy, onMount } from "svelte";
    import { flip } from "svelte/animate";
    import { quintOut } from "svelte/easing";
    import { crossfade, fade, slide } from "svelte/transition";

    export let toast: ToastInterface;
    let timeout: number;

    let toastType = toast.type || "info";

    const [send, receive] = crossfade({
        fallback(node, params) {
            const style = getComputedStyle(node);
            const transform = style.transform === "none" ? "" : style.transform;

            return {
                duration: 600,
                easing: quintOut,
                css: (t) => `
					transform: ${transform} scale(${t});
					opacity: ${t}
				`
            };
        }
    });

    onMount(() => {
        timeout = setTimeout(() => {
            removeToast(toast.id);
        }, toast.delay);
    });

    onDestroy(() => {
        clearTimeout(timeout);
    });
</script>

<button
    class="toast {toastType}"
    in:receive={{ key: toast.id }}
    out:send={{ key: toast.id }}
    on:click={() => removeToast(toast.id)}
>
    {toast.message}
</button>

<style lang="postcss">
    .toast {
        @apply m-6 cursor-pointer rounded-lg transition-all z-[999];
    }

    .toast.success {
        @apply bg-emerald-500;
    }

    .toast.error {
        @apply bg-red-500;
    }

    .toast.info {
        @apply bg-blue-500;
    }

    .icon {
        @apply text-white text-lg pl-1 py-1 grid place-items-center;
    }
</style>
