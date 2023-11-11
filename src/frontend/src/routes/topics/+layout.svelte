<script>
	import SideBar from './sideBar.svelte';
</script>

<div class="flex h-[100%]" id="sidebar-container">
	<SideBar />
	
	<div class="w-full">
		<slot />
	</div>
</div>

<style>
	:global(body) {
		/* /topics and related endpoints needs the body element to be unscrollable in order to function */
		overflow-y: hidden;
	}
</style>