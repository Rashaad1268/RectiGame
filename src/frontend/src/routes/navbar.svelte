<script lang="ts">
	/*
	Only use the navbar for some endpoints such as /, /welcome, /auth/login, /auth/signup

	Don't use the navbar for endpoints such as /topics because it'll look weird
	*/
	import { userData } from '$lib/stores';
	import ProfileMenu from './profileMenu.svelte';
	// import { isDarkMode } from '$lib/stores';

	$: isLoggedIn = $userData !== null;
	$: homepageUrl = isLoggedIn ? '/' : '/welcome';

	// Right now we don't have any links but we might need it in the future
	let navLinks: Array<{
		name: string;
		href?: string;
		sublinks?: Array<{ name: string; href: string }> | undefined;
	}> = [];
	/*
	Example:
		[{name: 'About', href='/about', sublinks: {name: 'Why Not?', href='/why_not'}}]
	*/

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
		@apply flex items-center bg-[var(--background-color)] z-[10000]
			 shadow-neutral-800 shadow-sm sticky top-0 px-8
			   h-[var(--navbar-height)] max-h-[var(--navbar-height)];
	}

	.nav-title {
		@apply font-gamer text-2xl;
	}
</style>
