<script lang="ts">
	export let value: string;
</script>

<!-- svelte-ignore a11y-autofocus -->
<input id="message-input" type="text" bind:value autofocus autocomplete="off" />

<style lang="scss">
	#message-input {
		@apply w-full text-gray-200 mb-2 p-3
           border border-gray-500 bg-discordDark-830 rounded-[4px]
           transition-shadow ease-out;

		&:focus {
			outline: none;
		}
	}
</style>
