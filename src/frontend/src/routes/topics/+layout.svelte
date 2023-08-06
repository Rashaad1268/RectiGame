<script>
	import SideBar from './sideBar.svelte';
</script>

<div class="flex gap-4">
	<SideBar />
	
	<div class="w-full">
		<slot />
	</div>
</div>
