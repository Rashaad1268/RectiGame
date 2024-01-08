<script lang="ts">
    import { page } from "$app/stores";
    import { userData } from "$lib/stores";
    /*
	Only use the navbar for some endpoints such as /, /welcome, /auth/login, /auth/signup
	*/
    import ProfileMenu from "./profileMenu.svelte";

    export let isLoggedIn: boolean;

    /*
    Reason to determine logged in status using this method is,
    
      Checking if the sessionid cookie exists to determine whether the user is logged in is not reactive,
      so when the user logouts, the navbar will think that the user is still logged in, until the page is refreshed

      And obtaining login state by checking the whether the userData store is null has its own problems,
      when the page initially loads, the fetchUserData function takes time to execute,
      so for a split second the navbar will think that the user is logged out and the
      when the user data is fetched, the navbar will update showing the profile picture instead of the authentication links
      

    so to fix the above 2 issues, the login state determined by checking whether one of following is truthy
        - the sessionid cookie exists
        - the userData store is not null
    */
    $: isActuallyLoggedIn = isLoggedIn || !!$userData;

    $: homepageUrl = isActuallyLoggedIn ? "/" : "/welcome";
    $: fromEndpoint = $page.url.searchParams.get("from");
</script>

<nav>
    <a class="nav-title nested-green" href={homepageUrl}><span class="text-4xl">G</span>amerz.lk</a>

    <div class="ml-auto">
        {#if isActuallyLoggedIn}
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
