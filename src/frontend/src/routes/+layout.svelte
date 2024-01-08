<script lang="ts">
    import { browser } from "$app/environment";
    import NavBar from "./navbar.svelte";
    import Toast from "$lib/components/toast.svelte";
    import { joinedTopics, userData } from "$lib/stores";
    import type { LayoutData } from "./$types";
    import SideBar from "./sideBar.svelte";
    import { initWebSocket } from "$lib/ws";

    import "../styles/app.scss";
    import { fetchUserData } from "$lib/utils";

    export let data: LayoutData;

    $: {
        if (!browser) {
            break $;
        }


        if (data.isLoggedIn && !$userData) {
            const ws = initWebSocket();
            // ws.on
            
            ws.addEventListener("open", () => {
                fetchUserData();
            });
            console.log("connecting ws", !$userData);
        }
    }
</script>

<NavBar isLoggedIn={data.isLoggedIn} />

<div class="flex h-[100%]">
    {#if $joinedTopics.length > 0}
        <SideBar />
    {/if}

    <main
        style="--max-h: calc(100vh - var(--navbar-height));
        height: var(--max-h); max-height: var(--max-h);"
        class="w-full overflow-y-auto"
    >
        <slot />
    </main>
</div>

<!-- <Footer /> -->

<Toast />
