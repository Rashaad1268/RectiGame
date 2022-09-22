<script lang="ts">
	import { joinedTopics } from '$lib/stores';
</script>

<!-- <div class="fixed top-16 left-0 h-screen w-16 flex flex-col">
    {#each $joinedTopics as topic}
        <a href="/topics/{topic.slug}">
            <div class="flex items-center justify-center w-16 h-w-16 rounded-full">
                <img src="{topic.image}" alt="{topic.name}" class="w-16 h-w-16 rounded-3xl hover:rounded-xl delay-100" />
            </div>
        </a>
    {/each}
</div> -->

<div
	class="top-16 left-0 h-screen w-14 sm:w-16 flex flex-col items-center gap-1 grow-0"
>
	{#each $joinedTopics as topic}
		<a href="/topics/{topic.slug}" class="w-14 sm:w-16">
			<img
				src={topic.image}
				alt={topic.name}
				class="rounded-full hover:rounded-3xl delay-100 "
			/>
		</a>
	{/each}
</div>
