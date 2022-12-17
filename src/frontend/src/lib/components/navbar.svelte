<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchApi } from '$lib/api';
	import { clearUserData, toastStore, userData } from '$lib/stores/';
	import { Popover, PopoverButton, PopoverPanel } from '@rgossiaux/svelte-headlessui';

	$: isLoggedIn = $userData !== null;
	$: homepageUrl = isLoggedIn ? '/' : '/welcome';

	async function logout() {
		const response = await fetchApi('auth/logout/', { method: 'POST' });

		if (response.ok) {
			clearUserData();
			toastStore.set({
				message: 'Logged Out',
				delay: 3000
			});
			goto('/welcome');
		} else {
			toastStore.set({
				message: 'Failed to logout',
				type: 'error'
			});
		}
	}
	interface NavLinkInterface {
		name: string;
		href?: string;
		sublinks?: Array<{ name: string; href: string }> | undefined;
	}

	let navLinks: Array<NavLinkInterface> = [];

	$: {
		if (!isLoggedIn) {
			navLinks = [
				{name: "Signup", href: "signup/"},
				{name: "Login", href: "login/"},
				...navLinks
			];
		} else {
			navLinks = navLinks.filter((item) => !['login', 'signup'].includes(item.name.toLowerCase()));
		}
	}
</script>

<nav class="navbar z-50 sticky top-0 right-0 bg-base-100 shadow-2xl">
	<div class="navbar-start">
		<div class="dropdown">
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label tabindex="0" class="btn btn-ghost lg:hidden">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					><path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 6h16M4 12h8m-8 6h16"
					/></svg
				>
			</label>
			<ul
				tabindex="0"
				class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
			>
				{#each navLinks as link (link.name)}
					{#if !link.sublinks}
						<li><a href={link.href}>{link.name}</a></li>
					{:else}
						<li tabindex="0">
							<a href={link.href} class="justify-between">
								{link.name}
								<svg
									class="fill-current"
									xmlns="http://www.w3.org/2000/svg"
									width="24"
									height="24"
									viewBox="0 0 24 24"
									><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg
								>
							</a>
							<ul class="p-2 bg-neutral">
								{#each link.sublinks || [] as sublink}
									<li><a href={sublink.href}>{sublink.name}</a></li>
								{/each}
							</ul>
						</li>
					{/if}
				{/each}
			</ul>
		</div>
		<a class="text-2xl sm:text-3xl" style="font-family: gamer-font;" href={homepageUrl}
			><span class="text-secondary text-3xl sm:text-4xl">G</span>amerz.lk</a
		>
	</div>
	<div class="navbar-center hidden lg:flex">
		<ul class="menu menu-horizontal p-0">
			{#each navLinks as link (link.name)}
				{#if !link.sublinks}
					<li><a href={link.href}>{link.name}</a></li>
				{:else}
					<li tabindex="0">
						<a href={homepageUrl} class="justify-between">
							{link.name}
							<svg
								class="fill-white"
								xmlns="http://www.w3.org/2000/svg"
								width="24"
								height="24"
								viewBox="0 0 24 24"
								><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg
							>
						</a>
						<ul class="p-2 bg-neutral">
							{#each link?.sublinks || [] as sublink}
								<li><a href={sublink.href}>{sublink.name}</a></li>
							{/each}
						</ul>
					</li>
				{/if}
			{/each}
		</ul>
	</div>
	<div class="navbar-end pr-3">
		<div class="dropdown dropdown-end">
			<Popover>
				<PopoverButton>
					<!-- svelte-ignore a11y-label-has-associated-control -->
					<label tabindex="0" class="btn btn-ghost btn-circle avatar">
						<div class="w-10">
							{#if $userData?.profile.profile_picture}
								<img
									src={$userData?.profile.profile_picture}
									class="rounded-full"
									alt="profile pic"
								/>
							{:else}
								<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
									<path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
									<path
										fill-rule="evenodd"
										d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"
									/>
								</svg>
							{/if}
						</div>
					</label>
				</PopoverButton>
				<PopoverPanel>
					<ul
						tabindex="0"
						class="mt-3 p-2 shadow menu menu-compact dropdown-content bg-base-100 rounded-box w-52"
					>
						{#if isLoggedIn}
							<li><button on:click={logout}>Logout</button></li>
						{:else}
							<li><a href="/login">Login</a></li>
							<li><a href="/signup">Signup</a></li>
						{/if}
					</ul>
				</PopoverPanel>
			</Popover>
		</div>
	</div>
</nav>
