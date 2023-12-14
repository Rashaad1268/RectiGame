<script lang="ts">
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import { __menu_Key, type MenuState } from "./index";

    const menuData = getContext<Writable<MenuState>>(__menu_Key);
</script>

{#if $menuData.isOpen}
    <div class="menu-content">
        <slot />
    </div>
{/if}

<style lang="scss">
    .menu-content {
        @apply absolute z-30 bottom-10;
    }
</style>
