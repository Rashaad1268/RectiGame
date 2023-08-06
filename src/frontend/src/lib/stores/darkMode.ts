import { writable } from 'svelte/store';

/*
    I don't have time to probably implement light theme on the CSS side
    So I won't be using the stuff in this file in the near future

    Hopefully some generous contributor dedicates their time to properly implement a light theme
*/

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function createDarkModeStore() {
	/*
        A custom store for handling dark mode
    */

	// Let's enable dark mode by default cuz why not
	const { subscribe, set: setState, update } = writable<boolean>(true);

	return {
		subscribe,
		init: () => {
			// This function will be called inside onMount in routes/+layout.ts
			const isDarkMode = localStorage.theme === 'dark' || !('theme' in localStorage);
			setState(isDarkMode);
			return isDarkMode;
		},
		set: (value: boolean) => {
			setState(value);
			updateLocalStorage(value);
		},
		toggle: () => {
			update((isDarkMode) => {
				updateLocalStorage(!isDarkMode);
				return !isDarkMode;
			});
		}
	};
}

function updateLocalStorage(darkMode: boolean) {
	if (darkMode) {
		localStorage.theme = 'dark';
	} else {
		localStorage.theme = 'light';
	}
}

// export const isDarkMode = createDarkModeStore();
