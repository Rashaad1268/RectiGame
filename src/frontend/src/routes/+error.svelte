<script lang="ts">
    import { page } from "$app/stores";

    // Only need the online state when the page loads
    const online = typeof navigator !== "undefined" ? navigator.onLine : true;
</script>

<svelte:head>
    <title>{$page.status} {!!$page.error?.message ? $page.error?.message : ""}</title>
</svelte:head>

<div class="error-container">
    {#if online}
        {#if $page.status === 404}
            <h1 class="title">Page not found ¯\_(ツ)_/¯</h1>
            <p>
                If you were expecting to find something here raise an issue on
                <a href="https://github.com/Rashaad1268/RectiGame" class="link">GitHub</a>
            </p>
        {:else}
            <h1 class="title">Oops...something went wrong</h1>

            <blockquote>
                <p>"Sorry our bad ¯\_(ツ)_/¯"</p>
                <p>- Devs</p>
            </blockquote>

            {#if $page?.error?.message}
                <p class="error">{$page.status}: {$page.error.message}</p>
            {:else}
                <p class="error">Encountered a {$page.status} error.</p>
            {/if}
            <p class="text-lg">Please try reloading the page.</p>
            <p class="text-lg">
                If the error persists, please raise an issue on
                <a href="https://github.com/Rashaad1268/RectiGame">GitHub</a>
            </p>
        {/if}
    {:else}
        <h1 class="title">It looks like you're offline</h1>
        <p class="text-lg">Reload the page once you've found the internet.</p>
    {/if}
</div>

<style lang="postcss">
    .error-container {
        /* @apply flex flex-col h-full items-center justify-center; */
        @apply mt-10 ml-10;
    }

    .title {
        @apply text-3xl font-semibold mb-4;
    }

    blockquote {
        border-left: 4px solid theme("colors.green.400");
        padding: 0 0 0 20px;
    }

    .error {
        @apply text-xl font-medium mt-6 mb-3;
    }
</style>
