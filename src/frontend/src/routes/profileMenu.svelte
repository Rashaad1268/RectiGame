<script lang="ts">
    import { goto } from "$app/navigation";
    import { fetchApi } from "$lib/api";
    import { clearUserData, toastStore, userData } from "$lib/stores";

    let menuToggleButton: HTMLButtonElement | undefined;
    let userMenuExpanded = false;

    function handleMouseDown(e: Event) {
        if (!menuToggleButton?.contains(e.target as HTMLElement)) {
            userMenuExpanded = false;
        }
    }

    async function logoutUser() {
        const response = await fetchApi("auth/logout/", { method: "POST" });

        if (response.ok) {
            clearUserData();
            toastStore.set({
                message: "Logged Out",
                delay: 3000
            });
            goto("/welcome");
        } else {
            toastStore.set({
                message: "Failed to logout",
                type: "error"
            });
        }
    }
</script>

<svelte:window on:mouseup={handleMouseDown} />

<button
    aria-label="profile menu button"
    class="profile-btn"
    on:click={() => (userMenuExpanded = !userMenuExpanded)}
    bind:this={menuToggleButton}
>
    {#if $userData?.profile.profile_picture}
        <img src={$userData?.profile.profile_picture} class="profile-pic-img" alt="Profile pic" />
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

<div class="menu-content" class:menu-visible={userMenuExpanded}>
    {#if $userData}
        <button aria-label="Logout button" class="menu-tile" on:click={logoutUser}>Logout</button>
    {:else}
        <a class="menu-tile" href="/auth/login">Login</a>
        <a class="menu-tile" href="/auth/signup">Signup</a>
    {/if}
</div>

<style lang="scss">
    .profile-btn {
        @apply transition-transform;

        &:active {
            @apply scale-90;
        }
    }
    .profile-pic-img {
        @apply h-11 w-11 rounded-full object-cover;
    }

    .menu-content {
        @apply absolute right-8 flex flex-col w-36
             bg-discordDark-860 rounded-sm p-[3px]
			   -translate-y-2 opacity-0 scale-95 /* This line is for properties related to the transition*/
			   transition-all invisible;
        top: calc(var(--navbar-height) - 2px);

        &.menu-visible {
            @apply visible opacity-100 scale-100 translate-y-0; /* Reset the transition properties */
        }

        .menu-tile {
            @apply rounded-sm p-3 px-6;

            &:hover {
                @apply bg-neutral-900;
            }
        }
    }
</style>
