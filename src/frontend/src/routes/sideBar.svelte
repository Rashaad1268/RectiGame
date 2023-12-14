<script lang="ts">
    import { goto } from "$app/navigation";
    import { joinedTopics } from "$lib/stores/";
    import type { TopicInterface } from "$lib/types";

    function visitTopicChat(topic: TopicInterface) {
        goto(`/topics/${topic.slug}/channel/${!!topic.channels[0] ? topic.channels[0].id : ""}`);
    }
</script>

<div class="sidebar">
    <a href="/" class="sidebar-icon">
        <div class="bg-discordDark-760 square-on-hover">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="p-[10px] fill-green-500 h-12 w-12"
                viewBox="0 0 576 512"
                ><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
                    d="M575.8 255.5c0 18-15 32.1-32 32.1h-32l.7 160.2c0 2.7-.2 5.4-.5 8.1V472c0 22.1-17.9 40-40 40H456c-1.1 0-2.2 0-3.3-.1c-1.4 .1-2.8 .1-4.2 .1H416 392c-22.1 0-40-17.9-40-40V448 384c0-17.7-14.3-32-32-32H256c-17.7 0-32 14.3-32 32v64 24c0 22.1-17.9 40-40 40H160 128.1c-1.5 0-3-.1-4.5-.2c-1.2 .1-2.4 .2-3.6 .2H104c-22.1 0-40-17.9-40-40V360c0-.9 0-1.9 .1-2.8V287.6H32c-18 0-32-14-32-32.1c0-9 3-17 10-24L266.4 8c7-7 15-8 22-8s15 2 21 7L564.8 231.5c8 7 12 15 11 24z"
                /></svg
            >
        </div>
        <span class="sidebar-tooltip">View all topics</span>
    </a>

    <!-- Divider -->
    <div class="h-[1px] w-9 my-[6px] bg-discordDark-460 rounded-full" />

    {#each $joinedTopics as topic (topic.slug)}
        <button on:click={() => visitTopicChat(topic)} class="sidebar-icon">
            <div>
                <img
                    src={topic.image}
                    draggable="false"
                    alt={topic.name}
                    loading="lazy"
                    class="square-on-hover"
                />
            </div>
            <span class="sidebar-tooltip">
                {topic.name}
            </span>
        </button>
    {/each}
</div>

<style lang="scss">
    .sidebar {
        @apply sticky left-0 bottom-0 top-16 flex flex-col items-center gap-2 grow-0
			  bg-discordDark-860 overflow-y-scroll pt-4 px-4;

        // Remove the scrollbar
        -ms-overflow-style: none; /* IE and Edge */
        scrollbar-width: none; /* Firefox */

        &::-webkit-scrollbar {
            display: none;
        }
    }

    .sidebar-icon {
        @apply relative flex items-center justify-center shadow-sm;

        img {
            @apply object-cover transition-all duration-100
				   ease-linear w-12 h-12;
        }

        &:hover {
            .square-on-hover {
                @apply rounded-[17px]
					transition-all duration-100 ease-linear;
            }
        }
    }

    .square-on-hover {
        // Effect on the border radius when it is hovered
        @apply rounded-3xl transition-all duration-100 ease-linear;
    }

    .sidebar-tooltip {
        @apply absolute w-auto p-2 m-2 min-w-max left-16 rounded-md shadow-md
			 text-white bg-discordDark-900 text-xs font-semibold
			   transition-all duration-100 scale-0 origin-left;

        .sidebar-icon:hover > & {
            // Scale the tooltip up when the icon is hovered
            @apply scale-100;
        }
    }
</style>
