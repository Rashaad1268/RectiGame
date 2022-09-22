<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchApi, formatApiErrors } from '$lib/api';
	import { userData, joinedTopics } from '$lib/stores';
	import { faLock } from '@fortawesome/free-solid-svg-icons';
	import FaIcon from 'svelte-fa';
	import { slide } from 'svelte/transition';

	let username: string;
	let email: string;
	let password: string;
	let password2: string;

	let errorMessages: string[] = [];

	const handleSignup = async () => {
		if (password !== password2) {
			errorMessages = ["Passwords do not match", ...errorMessages]
			return;
		}

		const response = await fetchApi('auth/signup/', {
			method: 'POST',
			body: JSON.stringify({
                username,
				email,
				password
			})
		});

		if (response.ok) {
			const responseData = await response.json();
			userData.set(responseData['user']);
			joinedTopics.set(responseData['joined_topics']);
			goto('/');
		} else {
			errorMessages = formatApiErrors(await response.json());
		}
	};
</script>

<svlete:head>
	<title>Signup</title>
</svlete:head>

<div class="min-h-[75%] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		<div>
			<!-- <h1 class="text-green-500 text-9xl" style="font-family: gamer-font;">G</h1> -->
			<h2
				class="mt-8 text-center text-3xl font-semibold text-gray-700 dark:text-gray-400"
				style="font-family: gamer-font;"
			>
				Welcome, Gamer
			</h2>
			<p class="mt-2 text-center text-sm text-gray-300">
				Already have an account?
				<a href="/login" class="font-medium text-primary link-hover hover:text-secondary">Login</a>
			</p>
		</div>
		<form class="mt-5 space-y-6" on:submit|preventDefault={handleSignup}>
			<div class="rounded-md shadow-sm">
				<div>
					<label for="username" class="sr-only">Username</label>
					<input
						id="username"
						bind:value={username}
						name="username"
						type="text"
						autocomplete="username"
						class="input input-bordered input-secondary w-full mb-2"
						placeholder="Username"
						required
					/>
				</div>
				<div>
					<label for="email" class="sr-only">Email address</label>
					<input
						id="email"
						bind:value={email}
						name="email"
						type="email"
						autocomplete="email"
						class="input input-bordered input-secondary w-full mb-2"
						placeholder="Email"
						required
					/>
				</div>
				<div>
					<label for="password" class="sr-only">Password 1</label>
					<input
						id="password"
						name="password"
						bind:value={password}
						type="password"
						autocomplete="current-password"
						class="relative block input input-bordered input-secondary w-full mb-2"
						placeholder="Password 1"
						required
					/>
				</div>
				<div>
					<label for="password2" class="sr-only">Password 2</label>
					<input
						id="password2"
						name="password2"
						bind:value={password2}
						type="password"
						autocomplete="current-password"
						class="relative block input input-bordered input-secondary w-full mb-2"
						placeholder="Password 2"
						required
					/>
				</div>
			</div>

			<div class="pt-1">
				<button
					type="submit"
					class="btn btn-secondary group relative w-full"
				>
					<FaIcon icon={faLock} class="h-5 w-5 text-primary group-hover:text-secondary mr-1" />
					Signup
				</button>
			</div>
		</form>

		{#each errorMessages as errorMsg}
			<div class="alert alert-error shadow-lg" in:slide>
				<div>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="stroke-current flex-shrink-0 h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
						><path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
						/></svg
					>
					<span>{errorMsg}</span>
				</div>
			</div>
		{/each}
	</div>
</div>
