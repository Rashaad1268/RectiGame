<script lang="ts">
	import type { TopicInterface } from '$lib/types';
	import type { PageData } from './$types';

	export let data: PageData;

	$: topic = data.topic as TopicInterface;
</script>

<div>
	<img src={topic.image} alt="topic img" />
	<h1 class="text-3xl">{topic.name}</h1>
	<p>{topic.description}</p>
</div>
