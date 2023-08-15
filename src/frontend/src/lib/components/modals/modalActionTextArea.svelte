<script lang="ts">
    import type { HTMLTextareaAttributes } from 'svelte/elements';

	export let value: string;

	interface $$Props extends HTMLTextareaAttributes {
		value: string;
	}
</script>


<textarea {...$$restProps} bind:value />

<style lang="scss">
    textarea {
        @apply flex min-h-[80px] w-full rounded-md border border-black bg-discordDark-830 px-3 py-2 text-sm ring-offset-discordDark-830 placeholder:text-white focus-visible:outline-none focus-visible:ring-2 /* focus-visible:ring-ring */ focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none;
    }
</style>