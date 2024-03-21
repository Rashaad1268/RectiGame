<script lang="ts">
    import { goto } from "$app/navigation";
    import { fetchApi } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { FullScreenModal } from "$lib/components/modals";
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import { clearData, userData } from "$lib/stores";
    import { toast } from "svelte-sonner";

    export let isOpen: boolean;

    async function logoutUser() {
        const response = await fetchApi("auth/logout/", { method: "POST" });

        if (response.ok) {
            isOpen = false;
            toast.success("Logged Out");
            clearData();
            goto("/welcome");
        } else {
            toast.error("Failed to logout", {
                description: `${response.statusText} ${response.status}`,
                duration: 10000
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
