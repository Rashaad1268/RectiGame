<script lang="ts">
	import Button from "$lib/components/button.svelte";
	export let isDestructive: boolean = false;
</script>

<Button
	on:click
	class="rounded-xl text-white {$$restProps?.class ?? ''}
		{isDestructive ? 'btn-error bg-red-500 border-none' : 'btn-secondary'}
		"
>
	<slot />
</Button>
