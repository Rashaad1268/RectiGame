<script lang="ts">
    import { userData } from "$lib/stores";
    import UserProfileModal from "./userProfileModal.svelte";

    $: isLoggedIn = !!$userData;
    let isUserProfileModalOpen = false;
</script>

<UserProfileModal bind:isOpen={isUserProfileModalOpen} />

<button
    aria-label="profile menu button"
    class="profile-btn"
    on:click={() => {
        if (isLoggedIn) isUserProfileModalOpen = !isUserProfileModalOpen;
    }}
>
    {#if $userData?.profile.profile_picture}
        <img src={$userData?.profile.profile_picture} class="profile-pic-img" alt="Profile pic" />
    {:else if $userData?.username}
        <div class="bg-discordDark-600 profile-pic-img grid center items-center">
            {$userData?.username.slice(0, 1)}
        </div>
    {:else}
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="profile-pic-img"
            viewBox="0 0 16 16"
        >
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
            <path
                fill-rule="evenodd"
                d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"
            />
        </svg>
    {/if}
</button>

<style lang="scss">
    .profile-btn {
        @apply transition-transform;

        &:active {
            @apply scale-90;
        }
    }
    .profile-pic-img {
        @apply size-11 rounded-full object-cover;
    }
</style>
