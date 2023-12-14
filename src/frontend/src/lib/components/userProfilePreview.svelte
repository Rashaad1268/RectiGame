<script lang="ts">
    import type { UserInterface } from "$lib/types";

    export let user: UserInterface;
</script>

<div>
    {user.username}
    {user.profile.about_me}
</div>
