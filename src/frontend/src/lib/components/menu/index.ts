export { default as Menu } from './menu.svelte';
export { default as MenuButton } from './menuButton.svelte';
export { default as MenuContent } from './menuContent.svelte';

export interface MenuState {
	isOpen: boolean;
}

export const __menu_Key = Symbol();
