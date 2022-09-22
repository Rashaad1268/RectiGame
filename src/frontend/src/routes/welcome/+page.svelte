<script defer lang="ts">
	import { onMount } from 'svelte';

	onMount(() => {
		const observer = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					entry.target.classList.add('show');
				}
			});
		});

		const hiddenElements = document.querySelectorAll('.hidden-elem');
		hiddenElements.forEach((el) => observer.observe(el));
	});
</script>

<svelte:head>
	<title>Welcome to Gamerz.lk</title>
</svelte:head>

<main>
	<span class="show" />
	<!-- Keep an empty span with the show class to make vite not purge it -->

	<div class="sections">
		<div class="section hidden-elem" style="--delay: 1;">
			<div class="ml-8">
				<div class="title-text">
					<h1>From gamers</h1>
					<h1>to gamers</h1>
				</div>
				<div class="description-text">
					<p>Gamerz.lk is a website made for Sri Lankan gamers</p>
					<p>to connect with each other</p>
				</div>
			</div>
			<img src="/2_people_gaming.jpg" class="section-img" alt="2 people gaming" />
		</div>

		<br /><br /><br /><br />

		<div class="section hidden-elem" style="--delay: 2;">
			<div class="ml-8">
				<div class="title-text">
					<h1>Not a gamer?</h1>
					<h1>No problem</h1>
				</div>
				<div class="description-text">
					<p>Gamerz.lk can also be used by sports players</p>
					<p>to connect with each other and organize matches</p>
				</div>
			</div>
			<img
				src="/people_playing_basketball.jpg"
				class="section-img"
				alt="2 people gaming"
			/>
		</div>
	</div>

	<div class="flex flex-col items-center">
		<h1 class="text-green-500 text-6xl font-semibold text-center pt-32 pb-3">
			So what are you waiting for?
		</h1>
		<a href="/signup"><button class="btn btn-primary btn-lg btn-wide">Join us</button></a>
	</div>
</main>

<style lang="postcss">
	.sections {
		/* TODO: use a grid layout */
	}

	.section {
		@apply flex justify-start flex-col md:flex-row pt-10 px-4;
	}

	.title-text {
		@apply text-green-500 text-6xl font-semibold md:pt-[15%];
	}

	.description-text {
		@apply text-lg font-medium pt-3;
	}

	.section-img {
		@apply rounded w-[100%] justify-end px-5 pt-1 pl-8 md:w-[55%] md:pt-0 lg:ml-16;
	}

	/* Comment the below animation classes because it messes with other contents of the website */
	/* .hidden-elem {
		opacity: 0;
		filter: blur(3 px);
		transform: translateX(-100%);
		transition: all calc(1s * var(--delay));
	}

	.show {
		opacity: 1;
		filter: blur(0);
		transform: translateX(0);
	} */
</style>
