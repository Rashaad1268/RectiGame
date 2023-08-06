const defaultTheme = require('tailwindcss/defaultTheme');
const colors = require('tailwindcss/colors');

/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	darkMode: 'class',
	plugins: [require('@tailwindcss/typography')],

	theme: {
		colors: {
			...colors,
			discordDark: {
				300: 'hsl(210, 9.3%, 78.8%)',
				360: 'hsl(209, 8.1%, 61.2%)',
				400: 'hsl(223, 5.8%, 52.9%)',
				460: 'hsl(228, 5.2%, 38%)',
				600: 'hsl(223, 6.7%, 20.6%)',
				630: 'hsl(220, 6.5%, 18%)',
				645: 'hsl(220, 7%, 16.9%)',
				660: 'hsl(228, 6.7%, 14.7%)',
				760: 'hsl(216, 8.5%, 11.6%)',
				800: 'hsl(225, 7.7%, 10.2%)',
				830: '#121315',
				860: '#0c0d0e',
				900: 'hsl(240, 11.1%, 1.8%)'
			}
		},
		fontFamily: {
			...defaultTheme.fontFamily,
			gamer: ['gamer-font', 'sans-serif'],
			monocraft: ['monocraft', 'sans-serif']
		}
	}
};
