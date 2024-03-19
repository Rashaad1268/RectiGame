<script lang="ts">
    import { goto } from "$app/navigation";
    import { fetchApi } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { FullScreenModal } from "$lib/components/modals";
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import { addToast, clearData, userData } from "$lib/stores";

    export let isOpen: boolean;

    async function logoutUser() {
        const response = await fetchApi("auth/logout/", { method: "POST" });

        if (response.ok) {
            isOpen = false;
            clearData();
            addToast({
                message: "Logged Out",
                delay: 3000
            });
            goto("/welcome");
        } else {
            addToast({
                message: "Failed to logout",
                type: "error"
            });
        }
    }
</script>

<FullScreenModal bind:isOpen>
    <div class="flex items-center justify-center mt-16 gap-4">
        <ProfilePicture user={$userData} class="size-20" />
        <div>
            <h1 class="text-bold text-xl">{$userData?.username}</h1>
            <Button class="btn-destructive btn-sm" on:click={logoutUser}>Logout</Button>
        </div>
    </div>
</FullScreenModal>
