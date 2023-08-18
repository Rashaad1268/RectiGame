<script lang="ts">
	import type { HTMLButtonAttributes } from 'svelte/elements';

	// export let isLoading: boolean | undefined = false;
	export const isLoading: boolean | undefined = false;
	export const isDestructive: boolean | undefined = false;

	interface $$Props extends HTMLButtonAttributes {
		isLoading?: boolean;
		isDestructive?: boolean;
	}
</script>

<button on:click on:dblclick class={isDestructive ? 'btn-destructive' : ''} {...$$restProps}>
	<div class="contents">
		<slot />
	</div>
</button>

<style lang="scss">
	// Default button size is medium (md)
	button {
		@apply font-semibold font-gg capitalize
      bg-green-600 w-auto box-border
        text-lg rounded-md
        h-9 px-4 py-2
        flex items-center justify-center select-none;

		color: hsl(0 calc(1 * 0%) 100% /1);
		transition: background-color 0.17s ease, color 0.17s ease;

		.contents {
			@apply my-0 mx-auto whitespace-nowrap text-ellipsis overflow-hidden;
		}

		&:hover {
			@apply bg-green-700;
		}

		&:active {
			@apply bg-green-800;
		}

		&.btn-lg {
			@apply h-10 rounded-md px-8 text-xl;
		}

		&.btn-sm {
			@apply h-8 rounded-md px-3 text-sm;
		}
	}

	.btn-destructive {
		@apply bg-red-600;

		&:hover {
			@apply bg-red-700;
		}
		&:active {
			@apply bg-red-800;
		}
	}

	.btn-blue {
		@apply bg-blue-600;

		&:hover {
			@apply bg-blue-700;
		}
		&:active {
			@apply bg-blue-800;
		}
	}
</style>
