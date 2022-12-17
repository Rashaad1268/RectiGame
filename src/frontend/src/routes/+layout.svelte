<script lang="ts">
	import { onMount } from 'svelte';
	import '../app.css';

	import { fetchApi } from '$lib/api';
	import Footer from '$lib/components/footer.svelte';
	import NavBar from '$lib/components/navbar.svelte';
	import { joinedTopics, userData } from '$lib/stores/';
	import Toast from '$lib/components/toast.svelte';

	export let data: any;

	onMount(async () => {
		if (data.isLoggedIn && !$userData) {
			const response = await fetchApi('auth/users/me/');
			if (response.ok) {
				const responseData = await response.json();
				userData.set(responseData['user']);
				joinedTopics.set(responseData['joined_topics']);
			} else {
				console.error(
					`Failed to fetch user data (status: ${response.status} ${response.statusText})`
				);
			}
		}
	});
</script>

<NavBar />

<!-- So the navbar doesn't overlap the content -->
<main class="min-h-screen">
	<slot />
</main>

<Footer />

<Toast />
