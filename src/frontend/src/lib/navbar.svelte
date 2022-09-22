<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchApi } from '$lib/api';
	import * as stores from '$lib/stores';
	import { userData } from '$lib/stores';

	$: isLoggedIn = $userData !== null;
	$: homepageUrl = isLoggedIn ? '/' : '/welcome';

	async function logout() {
		const response = await fetchApi('auth/logout/', { method: 'POST' });

		if (response.ok) {
			stores.userData.set(null);
			stores.joinedTopics.set([]);
			stores.topics.set(null);
			goto('/welcome');
		}
	}
</script>

<div class="navbar fixed bg-base-100 border-b border-base-200 shadow-lg">
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
				<li><a href={homepageUrl}>Item 1</a></li>
				<li tabindex="0">
					<a href={homepageUrl} class="justify-between">
						Parent
						<svg
							class="fill-current"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							viewBox="0 0 24 24"
							><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg
						>
					</a>
					<ul class="p-2">
						<li><a href={homepageUrl}>Submenu 1</a></li>
						<li><a href={homepageUrl}>Submenu 2</a></li>
					</ul>
				</li>
				<li><a href={homepageUrl}>Item 3</a></li>
			</ul>
		</div>
		<a class="text-2xl sm:text-3xl" style="font-family: gamer-font;" href={homepageUrl}
			><span class="text-secondary text-3xl sm:text-4xl">G</span>amerz.lk</a
		>
	</div>
	<div class="navbar-center hidden lg:flex">
		<ul class="menu menu-horizontal p-0">
			<li><a href={homepageUrl}>Item 1</a></li>
			<li tabindex="0">
				<a href={homepageUrl}>
					Parent
					<svg
						class="fill-current"
						xmlns="http://www.w3.org/2000/svg"
						width="20"
						height="20"
						viewBox="0 0 24 24"
						><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" /></svg
					>
				</a>
				<ul class="p-2">
					<li><a href={homepageUrl}>Submenu 1</a></li>
					<li><a href={homepageUrl}>Submenu 2</a></li>
				</ul>
			</li>
			<li><a href={homepageUrl}>Item 3</a></li>
		</ul>
	</div>
	<div class="navbar-end pr-3">
		<div class="dropdown dropdown-end">
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label tabindex="0" class="btn btn-ghost btn-circle avatar">
				<div class="w-10">
					{#if $userData?.profile.profile_picture}
						<img src={$userData?.profile.profile_picture} class="rounded-full" alt="profile pic" />
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
		</div>
	</div>
</div>

<style lang="postcss">
	.nav-title {
		font-family: gamer-font;
	}
</style>
