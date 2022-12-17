const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			screens: {
				...defaultTheme.screens
			}
		}
	},
	plugins: [require('daisyui')],
	daisyui: {
		logs: false,
		themes: {
			forest: {
				...require('daisyui/src/colors/themes')['[data-theme=forest]'],
				error: 'blue'
			}
		}
	}
};
