<script lang="ts">
	import { getContext } from 'svelte';
	import type { HTMLButtonAttributes } from 'svelte/elements';
	import type { Writable } from 'svelte/store';
	import { __menu_Key, type MenuState  } from './index';

	const menuData = getContext<Writable<MenuState>>(__menu_Key);

	interface $$Props extends HTMLButtonAttributes {
    };

	function handleOnClick() {
		menuData.update((v) => {
			return { ...v, isOpen: !v.isOpen };
		});
	}
</script>

<button aria-label="close menu button" {...$$restProps} on:click={handleOnClick}>
	<slot />
</button>
