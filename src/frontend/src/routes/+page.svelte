<script lang="ts">
	import { userData } from '$lib/stores';
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<div class="pt-5">
{#if !$userData}
	<div class="flex justify-center">
		<button class="btn loading">Loading</button>
	</div>
{:else}
	<h1 class="text-center text-xl font-semibold">Hello {$userData?.username}</h1>
	<ul class="text-center text-lg">
		<li><a href="/topics" class="link link-hover text-blue-500">View topics</a></li>
	</ul>
{/if}
</div>