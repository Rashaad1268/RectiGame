<script lang="ts">
	import { goto } from '$app/navigation';
	import { slide } from 'svelte/transition';

	import { TextField } from '$lib/components/forms';

	import { fetchApi, formatApiErrors } from '$lib/api';
	import Alert from '$lib/components/alert.svelte';
	import { Form } from '$lib/components/forms';
	import Button from '$lib/components/button.svelte';
	import { fetchUserData } from '$lib/utils';
	import BackgroundGrid from '../backgroundGrid.svelte';
	import type { LayoutData } from './$types';

	export let data: LayoutData;

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
	<title>Login</title>
</svelte:head>

<BackgroundGrid />

<div class="login-form centered">
	<div class="max-w-md w-full">
		<div>
			<h2
				class="mt-8 text-center nested-green text-3xl font-gamer
				 text-gray-700 dark:text-gray-400"
			>
				Welcome back, <span>Gamer</span>
			</h2>
			<p class="mt-2 text-center font-monocraft text-sm">
				Don't have an account?
				<a href="signup{data.next ? `?next=${data.next}` : ''}" class="link">Signup</a>
			</p>
		</div>
		<Form class="mt-6" on:submit={handleLogin}>
			<div class="rounded-md shadow-sm">
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
					<label for="password" class="sr-only">Password</label>
					<TextField
						id="password"
						name="password"
						type="password"
						bind:value={password}
						autocomplete="current-password"
						placeholder="Password"
						required
					/>
				</div>
			</div>

			<Button
				aria-label="login button"
				type="submit"
				class="flex items-center justify-center group relative w-full mt-4"
			>
				<svg class="h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
					><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
						d="M144 144v48H304V144c0-44.2-35.8-80-80-80s-80 35.8-80 80zM80 192V144C80 64.5 144.5 0 224 0s144 64.5 144 144v48h16c35.3 0 64 28.7 64 64V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V256c0-35.3 28.7-64 64-64H80z"
					/></svg
				>
				Login
			</Button>
		</Form>

		<div class="pt-10">
			{#each errorMessages as errorMsg}
				<Alert class="alert-error shadow-lg" inTransition={slide}>
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
	.login-form {
		@apply flex items-center justify-center z-10;

		left: 50%;
		position: absolute;
		top: 50%;
		transform: translate(-50%, -50%);
	}
</style>
