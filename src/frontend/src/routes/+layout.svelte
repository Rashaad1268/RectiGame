<script lang="ts">
	import { browser } from '$app/environment';
	import NavBar from './navbar.svelte';
	import Toast from '$lib/components/toast.svelte';
	import { userData } from '$lib/stores';
	import type { LayoutData } from './$types';
	import { socket } from '$lib/stores';
	import SideBar from './sideBar.svelte';
	import { initWebSocket } from '$lib/ws';

	import '../styles/app.scss';
	import { fetchUserData } from '$lib/utils';

	export let data: LayoutData;

	$: {
		if (!browser) {
			break $;
		}
		if (data.isLoggedIn && !$userData) {
			fetchUserData();
		}
	}

	$: {
		if (browser) {
			while (!$socket && data.isLoggedIn) {
				initWebSocket();
			}
		}
	}
</script>

<NavBar />

<div class="flex h-[100%]">
	{#if data.isLoggedIn}
		<SideBar />
	{/if}

	<main
		style="height: 100%; max-height: calc(100vh - var(--navbar-height));"
		class="w-full overflow-y-auto"
	>
		<slot />
	</main>
</div>

<!-- <Footer /> -->

<Toast />
