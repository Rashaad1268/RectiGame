<script>
    import ChannelSideBar from "./channelSideBar.svelte";
</script>

<div class="flex">
    <ChannelSideBar />

    <div class="w-full">
        <slot />
    </div>
</div>
