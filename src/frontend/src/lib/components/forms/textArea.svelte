<script lang="ts">
	export let value: string | undefined = undefined;
</script>

<textarea {...$$restProps} on:change bind:value />

<style lang="scss">
	textarea {
		@apply flex min-h-[80px] w-full text-sm ring-offset-discordDark-830
        placeholder:text-white focus-visible:outline-none focus-visible:ring-2
        focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50
        resize-none text-gray-200 mb-2 px-2 py-3 border border-gray-500
      bg-discordDark-830 rounded-[4px] transition-shadow ease-out;

		&:focus {
			outline: none;
			box-shadow: 0px 2px 0px theme('colors.green.400');
		}
	}
</style>
