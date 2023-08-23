<script>
	import SideBar from './sideBar.svelte';
</script>

<div class="flex gap-4 h-[100%]">
	<SideBar />
	
	<div class="w-full h-full overflow-y-scroll">
		<slot />
	</div>
</div>

<style>
	:global(body) {
		/* /topics and related endpoints needs the body element to be unscrollable in order to function */
		overflow-y: hidden;
	}
</style>