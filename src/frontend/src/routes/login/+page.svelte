<script lang="ts">
	import { goto } from '$app/navigation';
	import { faLock } from '@fortawesome/free-solid-svg-icons';
	import FaIcon from 'svelte-fa';
	import { slide } from 'svelte/transition';

	import { fetchApi, formatApiErrors } from '$lib/api';
	import { userData, joinedTopics } from '$lib/stores';


	export let data: any;

	let email: string;
	let password: string;
	let errorMessages: string[] = [];

	const handleLogin = async () => {
		const response = await fetchApi('auth/login/', {
			method: 'POST',
			body: JSON.stringify({
				email,
				password
			})
		});

		if (response.ok) {
			const responseData = await response.json();
			userData.set(responseData['user']);
			joinedTopics.set(responseData['joined_topics']);
			goto(data.next ?? '/');
		} else {
			errorMessages = formatApiErrors(await response.json());
		}
	};
</script>

<svlete:head>
	<title>Login</title>
</svlete:head>

<div class="min-h-[75%] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		<div>
			<h2
				class="mt-8 text-center text-3xl font-semibold text-gray-700 dark:text-gray-400"
				style="font-family: gamer-font;"
			>
				Welcome back, Gamer
			</h2>
			<p class="mt-2 text-center text-sm text-gray-300">
				Don't have an account?
				<a href="/signup" class="font-medium text-primary link-hover hover:text-secondary">Signup</a
				>
			</p>
		</div>
		<form class="mt-5 space-y-6" on:submit|preventDefault={handleLogin}>
			<div class="rounded-md shadow-sm">
				<div>
					<label for="email" class="sr-only">Email address</label>
					<input
						id="email"
						bind:value={email}
						name="email"
						type="email"
						autocomplete="email"
						class="input input-bordered input-secondary w-full mb-1"
						placeholder="Email"
						required
					/>
				</div>
				<div>
					<label for="password" class="sr-only">Password</label>
					<input
						id="password"
						name="password"
						bind:value={password}
						type="password"
						autocomplete="current-password"
						class="relative block input input-bordered input-secondary w-full"
						placeholder="Password"
						required
					/>
				</div>
			</div>

			<div class="pt-1">
				<button type="submit" class="btn btn-secondary group relative w-full">
					<FaIcon icon={faLock} class="h-5 w-5 text-primary group-hover:text-secondary mr-1" />
					Login
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
