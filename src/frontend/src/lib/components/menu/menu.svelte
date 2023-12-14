<script lang="ts">
    import { setContext } from "svelte";
    import { writable } from "svelte/store";
    import { __menu_Key, type MenuState } from "./index";

    const menuData = writable<MenuState>({
        isOpen: false
    });

    setContext(__menu_Key, menuData);
</script>

<slot />
