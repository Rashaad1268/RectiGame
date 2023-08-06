<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchApi, formatApiErrors } from '$lib/api';
	import Alert from '$lib/components/alert.svelte';
	import Button from '$lib/components/button.svelte';
	import { TextField } from '$lib/components/forms';
	import { fetchUserData } from '$lib/utils';
	import { slide } from 'svelte/transition';
	import BackgroundGrid from '../backgroundGrid.svelte';
	import type { LayoutData } from './$types';

	export let data: LayoutData;
	let username: string;
	let email: string;
	let password: string;
	let password2: string;

	let errorMessages: string[] = [];

	$: console.log(data.next);

	const handleSignup = async () => {
		if (password !== password2) {
			errorMessages = ['Passwords do not match', ...errorMessages];
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
			fetchUserData()
				.then(() => {
					goto(data.next ?? '/topics');
				})
				.catch((err) => {
					errorMessages = [err, ...errorMessages];
				});
		} else {
			errorMessages = formatApiErrors(await response.json());
		}
	};
</script>

<svelte:head>
	<title>Signup</title>
</svelte:head>

<BackgroundGrid />

<div class="signup-form">
	<div class="max-w-md w-full">
		<div>
			<h2
				class="mt-8 text-center nested-green text-3xl font-gamer
					 text-gray-700 dark:text-gray-400"
			>
				Welcome, <span>Gamer</span>
			</h2>
			<p class="mt-2 text-center font-monocraft text-sm">
				Already have an account?
				<a href="login{data.next ? `?next=${data.next}` : ''}" class="link">Login</a>
			</p>
		</div>
		<form class="mt-6" on:submit|preventDefault={handleSignup}>
			<div class="rounded-md shadow-sm">
				<div>
					<label for="username" class="sr-only">Username</label>
					<TextField
						id="username"
						bind:value={username}
						name="username"
						autocomplete="username"
						placeholder="Username"
						required
					/>
				</div>
				<div>
					<label for="email" class="sr-only">Email address</label>
					<TextField
						id="email"
						bind:value={email}
						name="email"
						type="email"
						autocomplete="email"
						placeholder="Email"
						required
					/>
				</div>
				<div>
					<label for="password" class="sr-only">Password 1</label>
					<TextField
						id="password"
						name="password"
						type="password"
						bind:value={password}
						autocomplete="new-password"
						placeholder="Password 1"
						required
					/>
				</div>
				<div>
					<label for="password2" class="sr-only">Password 2</label>
					<TextField
						id="password2"
						name="password2"
						bind:value={password2}
						type="password"
						autocomplete="new-password"
						placeholder="Password 2"
						required
					/>
				</div>
			</div>

			<Button
				aria-label="Signup button"
				type="submit"
				class="flex items-center justify-center group relative w-full mt-4"
			>
				<svg class="h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
					><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
						d="M144 144v48H304V144c0-44.2-35.8-80-80-80s-80 35.8-80 80zM80 192V144C80 64.5 144.5 0 224 0s144 64.5 144 144v48h16c35.3 0 64 28.7 64 64V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V256c0-35.3 28.7-64 64-64H80z"
					/></svg
				>
				Signup
			</Button>
		</form>

		<div class="pt-10">
			{#each errorMessages as errorMsg}
				<Alert class="alert-error shadow-lg mb-1" inTransition={slide}>
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
				</Alert>
			{/each}
		</div>
	</div>
</div>

<style lang="scss">
	.signup-form {
		@apply flex items-center justify-center z-10;

		left: 50%;
		position: absolute;
		top: 50%;
		transform: translate(-50%, -50%);
	}
</style>
