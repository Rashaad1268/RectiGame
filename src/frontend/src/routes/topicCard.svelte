<script lang="ts">
    import type { TopicInterface } from "$lib/types";

    export let topic: TopicInterface;
</script>

<a href="/topics/{topic.slug}" class="topic-card">
    <div class="topic-image">
        <img loading="lazy" src={topic.image} alt={topic.name} />
    </div>
    <div class="px-1 pt-1 pb-[2px]">
        <div class="font-bold text-base max-w-full">{topic.name}</div>
        <p class="leading-[1rem] text-xs text-neutral-400">
            {topic.member_count} Member{topic.member_count !== 1 ? "s" : ""}
        </p>
    </div>
    <div class="post-tags">
        {#each topic.tags as tag (tag.slug)}
            <a href="/topics/tag/{tag.slug}">{tag.name}</a>
        {/each}
    </div>
</a>

<style lang="scss">
    .topic-image {
        @apply bg-green-500 rounded-sm;

        img {
            @apply w-full transition-transform rounded-sm;

            .topic-card:hover > & {
                @apply translate-x-[6px] -translate-y-2;
            }
        }
    }

    .post-tags {
        @apply hidden md:flex overflow-hidden gap-1 px-1 mt-[2px];

        a {
            @apply inline-block bg-zinc-700 rounded-full font-semibold
				   px-[6px] py-[1px] text-[10px];
        }
    }
</style>
