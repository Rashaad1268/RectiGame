<script lang="ts">
	import Button from '$lib/components/button.svelte';
	import { toastStore, userData } from '$lib/stores/';
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<div class="pt-5">
	{#if !$userData}
		<div class="flex justify-center">
			<Button aria-label="loading indicator button" isLoading>Loading</Button>
		</div>
	{:else}
		<h1 class="text-center text-xl font-semibold">Hello {$userData?.username}</h1>
		<ul class="text-center text-lg">
			<li><a href="/topics" class="link link-hover">View topics</a></li>
		</ul>
	{/if}

	<!-- <Button on:click={() => {
	toastStore.set({
		message: "Hello world",
		type: "error",
		delay: 25000
	});
}}>Show Toast</Button> -->

	<div class="flex flex-col gap-4 items-center pt-10">
		<div class="flex flex-row items-center justify-center gap-4 w-full">
			<Button aria-label="test button" class="btn-lg">Button</Button>
			<Button aria-label="test button">Button</Button>
			<Button aria-label="test button" class="btn-sm">Button</Button>
		</div>

		<div class="flex flex-row items-center justify-center gap-4 w-full">
			<Button aria-label="test button" class="btn-destructive btn-lg">Button</Button>
			<Button aria-label="test button" class="btn-destructive">Button</Button>
			<Button aria-label="test button" class="btn-destructive btn-sm">Button</Button>
		</div>		

		<div class="flex flex-row items-center justify-center gap-4 w-full">
			<Button aria-label="test button" class="btn-blue btn-lg">Button</Button>
			<Button aria-label="test button" class="btn-blue">Button</Button>
			<Button aria-label="test button" class="btn-blue btn-sm">Button</Button>
		</div>
	</div>
</div>

<Button aria-label="test button" on:click={() => {
	toastStore.set({
		message: "Hello world",
		type: "error",
		delay: 25000
	});
}}>Open toast</Button>
