<script>
	import SideBar from './sideBar.svelte';
</script>

<div class="flex gap-4 h-[100%]">
	<SideBar />
	
	<div class="w-full overflow-y-scroll">
		<slot />
	</div>
</div>

<style lang="scss">
	:global(body) {
		overflow-y: hidden;
	}
</style>
