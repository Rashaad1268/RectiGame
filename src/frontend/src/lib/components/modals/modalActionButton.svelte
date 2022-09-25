<script lang="ts">
	export let isDestructive: boolean = false;
</script>

<button
	on:click
	class="btn rounded-xl text-white {$$restProps?.class ?? ''}
		{isDestructive ? 'btn-error bg-red-500 border-none' : 'btn-secondary'}
		"
>
	<slot />
</button>
