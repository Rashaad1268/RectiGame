<script lang="ts">
	import type { LayoutData } from './$types';

	export let data: LayoutData;
</script>

<svelte:head>
	<title>Topics • {data.topic.name}</title>
</svelte:head>

<slot />
