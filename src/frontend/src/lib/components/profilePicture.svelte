<script lang="ts">
    import type { UserInterface } from "$lib/types";

    export let user: UserInterface | undefined | null;
</script>

{#if user?.profile.profile_picture}
    <img
        {...$$restProps}
        src={user?.profile.profile_picture}
        class="{$$restProps.class ?? ''} profile-pic-img"
        alt={$$restProps.alt ?? "profile"}
    />
{:else if user?.username}
    <div
        {...$$restProps}
        class="{$$restProps.class ?? ''} bg-discordDark-600 profile-pic-img grid place-items-center"
    >
        {user?.username.slice(0, 1)}
    </div>
{:else}
    <svg
        {...$$restProps}
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        fill="currentColor"
        class="{$$restProps.class ?? ''} profile-pic-img"
        viewBox="0 0 16 16"
    >
        <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
        <path
            fill-rule="evenodd"
            d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"
        />
    </svg>
{/if}

<style lang="postcss">
    .profile-pic-img {
        @apply rounded-full object-cover;
    }
</style>
