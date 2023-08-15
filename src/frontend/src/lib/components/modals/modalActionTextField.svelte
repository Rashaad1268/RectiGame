<script lang="ts">
    import TextField from "../forms/textField.svelte";
    import type { HTMLInputAttributes } from 'svelte/elements';

	export let value: string;

	interface $$Props extends HTMLInputAttributes {
		value: string;
	}
</script>

<TextField
    {...$$restProps}
    bind:value
/>
