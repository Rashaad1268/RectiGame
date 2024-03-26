<script lang="ts">
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import { joinedTopicRooms } from "$lib/stores";
    import type { TopicChatChannelInterface, TopicChatRoomInterface } from "$lib/types";

    export let channel: TopicChatChannelInterface | undefined;
</script>

{#if channel}
    <div class="room-member-list bg-discordDark-800 w-[18vw]">
        <h3 class="text-xl font-monocraft pl-4 pt-4">Room Members</h3>
        <div class="flex flex-col gap-[1px]">
            {#each channel?.members || [] as member (member.id)}
                <div class="member-tile">
                    <ProfilePicture user={member} class="size-10" />
                    <div>
                        <span class="text-lg font-medium">{member.username}</span>
                    </div>
                </div>
            {/each}
        </div>
    </div>
{/if}

<style lang="postcss">
    .member-tile {
        @apply flex gap-4 border items-center px-3 py-2
               justify-start bg-discordDark-800 border-discordDark-760;
    }
</style>
