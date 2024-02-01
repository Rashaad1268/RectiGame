<script lang="ts">
    import { page } from "$app/stores";

    import Button from "$lib/components/button.svelte";
    import { onMount } from "svelte";
    import BackgroundGrid from "../auth/backgroundGrid.svelte";

    let fromEndpoint: string | null = $page.url.searchParams.get("from");

    let nearScrollEnd = false;

    onMount(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("element-visible");
                    }
                });
            },
            { threshold: 0.4 }
        );

        const hiddenElements = document.querySelectorAll(".content");

        hiddenElements.forEach((e) => observer.observe(e));
    });
</script>

<svelte:head>
    <title>Welcome to RectiGame</title>
</svelte:head>

<!-- Keep this empty element with the faded-in class
so that the compiler doesn't purge the faded-in class -->
<span class="element-visible" />

<section class="w-full relative mb-2">
    <div id="tiles-overlay">
        <BackgroundGrid />
    </div>

    <div class="absolute mt-44 text-center">
        <h1 class="font-cod nested-green text-4xl lg:text-6xl">
            <span>Recti</span>Game
        </h1>

        <h3 class="lg:text-lg font-gamer">The game is on</h3>

        <h6 class="nested-green text-lg font-medium mt-6">
            A place for like minded gamers to collaborate and forge their path to <span
                class="font-doodle">victory</span
            >
        </h6>
    </div>
</section>

<section class="text-center">
    <div class="content max-w-4xl">
        <div class="text-3xl nested-green">
            <p>Today's world of sports and e-sports is highly competitive.</p>
            <p>
                If you don't step up your game, you will <span class="font-doodle">fall behind</span
                >
            </p>
        </div>

        <div class="text-2xl mt-4 mb-8 nested-green">
            <p>
                Ditch the randoms and find your team. Forge epic bonds, conquer pixels, and <span
                    class="font-doodle">level up</span
                >
                your game
            </p>
        </div>

        <a href="auth/signup{fromEndpoint ? `?next=${fromEndpoint}` : ''}" class="inline-block"
            ><Button class="btn-xl font-monocraft" aria-label="Sign up button"
                >Join the adventure</Button
            ></a
        >
    </div>

    <div class="content flex items-center justify-around w-full mt-52">
        <img
            width="600px"
            src="/images/welcome-page/screenshot_1.png"
            alt="A conversation between 2 people on RectiGame"
        />

        <div class="max-w-lg">
            <h1 class="text-4xl font-doodle text-green-500">Collaboration done easy</h1>
            <p>
                With RectiGame you can find the perfect squad for you. Whether it is basketball,
                Fortnite or chess that you're playing, RectiGame got you covered
            </p>
        </div>
    </div>
</section>

<button
    class="rounded-full bg-discordDark-700 p-4 fill-gray-100
           absolute bottom-4 right-8 animate-bounce"
    on:click={() => {
        document.querySelector("main")?.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth"
        });
    }}
    ><svg
        xmlns="http://www.w3.org/2000/svg"
        width="20px"
        height="20px"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="feather feather-arrow-down"
        ><line x1="12" y1="5" x2="12" y2="19" /><polyline points="19 12 12 19 5 12" /></svg
    ></button
>

<style lang="postcss">
    section {
        @apply flex flex-col items-center;
    }

    section:last-of-type {
        @apply mb-20;
    }

    :global(#tiles) {
        background: linear-gradient(to bottom, transparent, var(--background-color) 92%);
    }

    :global(#tiles-wrapper) {
        filter: blur(0.5px);
        opacity: 0.9;
    }

    #tiles-overlay {
        @apply max-h-full overflow-hidden max-w-full;
    }

    .content {
        @apply opacity-0;
        text-wrap: balance;
        transform: translate(0px, 40px);

        transition: opacity ease-in-out 0.5s, transform ease-in-out 0.4s;
    }

    .element-visible {
        opacity: 1;
        transform: translate(0px, 0px);
    }
</style>
