<script lang="ts">
    import { page } from "$app/stores";
    /*
	Only use the navbar for some endpoints such as /, /welcome, /auth/login, /auth/signup
	*/
    import ProfileMenu from "./profileMenu.svelte";

    export let isLoggedIn: boolean;
    $: homepageUrl = isLoggedIn ? "/" : "/welcome";

    $: fromEndpoint = $page.url.searchParams.get("from");
</script>

<nav>
    <a class="nav-title nested-green" href={homepageUrl}><span class="text-4xl">G</span>amerz.lk</a>

    <div class="ml-auto">
        {#if isLoggedIn}
            <ProfileMenu />
        {:else}
            <div class="flex gap-3 md:gap-8 font-monocraft">
                <a
                    href="/auth/login{fromEndpoint ? `?next=${fromEndpoint}` : ''}"
                    class="hover-underline">Login</a
                >
                <a
                    href="/auth/signup{fromEndpoint ? `?next=${fromEndpoint}` : ''}"
                    class="hover-underline">Signup</a
                >
            </div>
        {/if}
    </div>
</nav>

<style lang="scss">
    nav {
        @apply flex items-center bg-discordDark-830 z-[10000]
			 shadow-neutral-800 shadow-sm sticky top-0 px-8
			   h-[var(--navbar-height)] max-h-[var(--navbar-height)];
    }

    .nav-title {
        @apply font-gamer text-2xl;
    }
</style>
