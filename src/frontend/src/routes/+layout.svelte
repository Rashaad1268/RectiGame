<script lang="ts">
	import { browser } from '$app/environment';
	import { fetchApi } from '$lib/api';
	import Footer from '$lib/components/footer.svelte';
	import NavBar from './navbar.svelte';
	import Toast from '$lib/components/toast.svelte';
	import { joinedTopics, userData } from '$lib/stores';
	import type { LayoutData } from './$types';

	import '../styles/app.scss';

	export let data: LayoutData;

	// function setTheme(isDarkMode: boolean) {
	// 	if (!isDarkMode) {
	// 		document.documentElement.classList.remove('dark');
	// 	} else {
	// 		document.documentElement.classList.add('dark');
	// 	}
	// }

	$: {
		if (!browser) {
			break $;
		}
		if (data.isLoggedIn && !$userData) {
			fetchApi('auth/users/me/', { csrfToken: data.csrfToken }).then((response) => {
				if (response.ok) {
					response.json().then((responseData) => {
						userData.set(responseData['user']);
						joinedTopics.set(responseData['joined_topics']);
					});
				} else {
					console.error(
						`Failed to fetch user data (status: ${response.status} ${response.statusText})`
					);
				}
			});
		}
	}
</script>


<main style="min-height: calc(100vh - var(--navbar-height)); height: 100%;">
	<NavBar />
	<slot />
</main>

<!-- <Footer /> -->

<Toast />
