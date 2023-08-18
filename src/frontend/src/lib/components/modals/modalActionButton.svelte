<script lang="ts">
	import Button from "$lib/components/button.svelte";
	export let isDestructive: boolean = false;
	type size_t = "btn-sm" | "btn-md" | "btn-lg";
	export let size: size_t = "btn-sm";
</script>

<Button
	on:click
	class="rounded-xl text-white {size} ml-2 {$$restProps?.class ?? ''}
		{isDestructive ? 'btn-destructive bg-red-500 border-none' : 'btn-secondary'}
		"
>
	<slot />
</Button>
