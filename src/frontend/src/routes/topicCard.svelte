<script lang="ts">
    import type { TopicInterface } from "$lib/types";

    export let topic: TopicInterface;
</script>

<a href="/topics/{topic.slug}" class="topic-card max-w-[15vw] min-w-[10vw]">
    <div class="topic-image">
        <img loading="lazy" src={topic.image} alt={topic.name} />
    </div>
    <div class="px-1 pt-1 pb-[2px]">
        <div class="font-bold text-base max-w-full">{topic.name}</div>
        <p class="leading-[1rem] text-xs text-neutral-400">
            {topic.member_count} Member{topic.member_count !== 1 ? "s" : ""}
        </p>
    </div>
    <div class="topic-tags px-[1px]">
        {#each topic.tags as tag (tag.slug)}
            <span class="topic-tag">{tag.name}</span>
        {/each}
    </div>
</a>

<style lang="scss">
    .topic-image {
        @apply bg-green-500 rounded-sm;

        img {
            @apply w-full transition-transform rounded-sm;

            .topic-card:hover > & {
                @apply translate-x-[6px] -translate-y-[6px];
            }
        }
    }
</style>
