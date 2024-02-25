<script lang="ts">
    import type { UserInterface } from "$lib/types";

    export let user: UserInterface;
</script>

<div class="w-full bg-discordDark-900 flex items-center flex-col py-6">
    <img src={user.profile.profile_picture} alt="Profile" class="size-12 object-cover rounded-full" />
    <span class="mt-8">{user.username}</span>
</div>
