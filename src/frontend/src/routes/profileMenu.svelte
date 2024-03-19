<script lang="ts">
    import ProfilePicture from "$lib/components/profilePicture.svelte";
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
    <ProfilePicture class="size-11" user={$userData} />
</button>

<style lang="scss">
    .profile-btn {
        @apply transition-transform;

        &:active {
            @apply scale-90;
        }
    }
</style>
