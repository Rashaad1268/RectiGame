<script lang="ts">
	export let value: string | undefined = undefined;
</script>

<input type="text" {...$$restProps} on:change bind:value />

<style lang="scss">
	input {
		@apply w-full text-gray-200 mb-2 px-2 py-3
           border border-gray-500 bg-discordDark-830 rounded-[4px]
           transition-shadow ease-out;

		&:focus {
			outline: none;
			box-shadow: 0px 2px 0px theme('colors.green.400');
		}
	}
</style>
