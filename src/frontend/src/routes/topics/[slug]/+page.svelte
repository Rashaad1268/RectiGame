<!-- 
	Right now there is a MAJOR issue where this endpoint sends a reques to the API every
	time it's visited. 
	FIX: Implement caching and reduce the number of API calls

	related file: ./+page.ts
-->

<script lang="ts">
	import type { TopicInterface } from "$lib/types";
	import type { PageData } from "./$types";
	import { topics} from "$lib/stores";


	export let data: PageData;

	$: topic = data.topic as TopicInterface;
</script>

<svelte:head>
	<title>{topic.name}</title>
</svelte:head>

<div >

<h1 class="text-3xl font-semibold">{topic.name} chat</h1>
<a href="{topic.slug}/posts" class="text-2xl link link-hover">View topic posts</a>

</div>