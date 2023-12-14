<script lang="ts">
    import { onMount } from "svelte";

    let guildData: any;

    onMount(async () => {
        let res = await fetch("https://discord.com/api/guilds/1038761636145676298/widget.json");

        if (res.ok) {
            guildData = await res.json();
        }
    });
</script>

{#if guildData}
    <span class="inline-flex h-3 w-3 relative">
        <span class="outer" />
        <span class="inner" />
    </span>
    <span class="text-green-500">{guildData.presence_count}</span>
    member{guildData.presence_count !== 1 ? "s" : ""} online
{/if}

<style lang="postcss">
    .outer {
        @apply animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75;
    }
    .inner {
        @apply relative inline-flex rounded-full h-3 w-3 bg-green-500;
    }
</style>
