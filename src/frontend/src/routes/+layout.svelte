<script lang="ts">
    import { browser } from "$app/environment";
    import NavBar from "./navbar.svelte";
    import { userData } from "$lib/stores";
    import type { LayoutData } from "./$types";
    import SideBar from "./sideBar.svelte";
    import { Toaster } from "svelte-sonner";
    import { initWebSocket } from "$lib/ws";

    import "../styles/app.scss";
    import { fetchUserData } from "$lib/utils/";

    export let data: LayoutData;

    $: {
        if (!browser) {
            break $;
        }

        if (data.isLoggedIn && !$userData) {
            const ws = initWebSocket();

            ws.addEventListener("open", () => {
                fetchUserData();
            });
        }
    }
</script>

<NavBar isLoggedIn={data.isLoggedIn} />

<div class="flex h-[100%]">
    {#if data.isLoggedIn || !!$userData}
        <SideBar />
    {/if}

    <main
        style="--max-content-h: calc(100vh - var(--navbar-height));
        height: var(--max-content-h); max-height: var(--max-content-h);"
        class="w-full overflow-y-auto"
    >
        <slot />
    </main>
</div>

<Toaster theme="dark" />
