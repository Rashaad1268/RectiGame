<script lang="ts">
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import type { UserInterface } from "$lib/types";

    export let user: UserInterface;
</script>

<div class="w-full bg-discordDark-900 flex items-center flex-col py-6">
    <ProfilePicture {user} class="size-12" />
    <span class="mt-8">{user.username}</span>
</div>
