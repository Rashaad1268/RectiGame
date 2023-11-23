<script lang="ts">
	import { socket } from '$lib/stores';
	import SideBar from './sideBar.svelte';
	import { initWebSocket } from '$lib/ws';
	import { browser } from '$app/environment';

	$: {
		if (browser) {
			while (!$socket) {
				initWebSocket();
			}
		}
	}
</script>

<div class="flex h-[100%]" id="sidebar-container">
	<SideBar />

	<div class="w-full">
		<slot />
	</div>
</div>
