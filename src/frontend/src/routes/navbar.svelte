<script lang="ts">
	import { userData } from '$lib/stores';
	import ProfileMenu from './profileMenu.svelte';
	// import { isDarkMode } from '$lib/stores';

	$: isLoggedIn = $userData !== null;
	$: homepageUrl = isLoggedIn ? '/' : '/welcome';

	let navLinks: Array<{
		name: string;
		href?: string;
		sublinks?: Array<{ name: string; href: string }> | undefined;
	}> = [];

	$: {
		if (!isLoggedIn) {
			navLinks = [
				{ name: 'Signup', href: 'signup/' },
				{ name: 'Login', href: 'login/' },
				...navLinks
			];
		} else {
			navLinks = navLinks.filter((item) => !['login', 'signup'].includes(item.name.toLowerCase()));
		}
	}
</script>

<nav>
	<a class="nav-title nested-green" href={homepageUrl}><span class="text-4xl">G</span>amerz.lk</a>

	<ProfileMenu />
</nav>

<style lang="scss">
	nav {
		@apply z-[9999] flex items-center bg-discordDark-830
			 shadow-neutral-800 shadow-sm sticky top-0 px-8
			   h-[var(--navbar-height)] max-h-[var(--navbar-height)];
	}

	.nav-title {
		@apply font-gamer text-2xl;
	}
</style>
