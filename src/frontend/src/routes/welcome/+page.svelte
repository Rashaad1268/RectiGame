<script lang="ts">
    import { page } from "$app/stores";
    import Button from "$lib/components/button.svelte";
    import { onMount } from "svelte";

    onMount(() => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("show");
                } else {
                    entry.target.classList.remove("show");
                }
            });
        });

        const hiddenElements = document.querySelectorAll(".hidden-elem");
        hiddenElements.forEach((el) => observer.observe(el));
    });

    let fromEndpoint: string | null = $page.url.searchParams.get("from");
</script>

<svelte:head>
    <title>Welcome to Gamerz.lk</title>
</svelte:head>

<!-- <Navbar /> -->

<span class="show" />
<!-- Have an empty span with the show class so vite doesn't purge that css class -->

<div class="sections">
    <div class="section hidden-elem" style="--delay: 2;">
        <div class="ml-8">
            <div class="title-text hover-underline-text">
                <h1>From gamers</h1>
                <h1>To gamers</h1>
            </div>
            <div class="description-text">
                <p>Gamerz.lk is a website made for Sri Lankan gamers</p>
                <p>to connect with each other</p>
            </div>
        </div>
        <img src="/2_people_gaming.jpg" class="section-img" alt="2 people gaming" />
    </div>

    <div class="section hidden-elem" style="--delay: 4;">
        <div class="ml-8">
            <div class="title-text hover-underline-text">
                <h1>Not a gamer?</h1>
                <h1>No problem</h1>
            </div>
            <div class="description-text">
                <p>Gamerz.lk can also be used by sports players</p>
                <p>to connect with each other and organize matches</p>
            </div>
        </div>
        <img src="/people_playing_basketball.jpg" class="section-img" alt="2 people gaming" />
    </div>

    <div class="section-col items-center gap-2">
        <h1 class="text-green-500 text-6xl font-semibold text-center pt-32 pb-3">
            So what are you waiting for?
        </h1>
        <a href="auth/signup{fromEndpoint ? `?next=${fromEndpoint}` : ''}"
            ><Button class="btn-xl" aria-label="Join us button">Join us</Button></a
        >
    </div>

    <div class="flex flex-col items-center mt-32">
        <h1 class="text-5xl text-center font-semibold text-green-500 mb-2">
            Join Our Discord server
        </h1>
        <iframe
            src="https://discord.com/widget?id=1038761636145676298&theme=dark"
            title="Discord server widget"
            class="h-80 w-[200px] sm:w-[450px] md:w-[600px] lg:w-[700px]"
            allowtransparency={true}
            frameborder="0"
        />
    </div>
</div>

<style lang="scss">
    // .sections {
    // 	NOTE: maybe use a grid-like layout
    // }

    .section,
    .section-col {
        @apply flex flex-col pt-10 px-4 min-h-[80vh];
    }

    .section {
        @apply md:flex-row;
    }

    .title-text {
        @apply text-green-500 text-6xl font-semibold md:pt-[15%];
    }

    .hover-underline-text {
        background-image: linear-gradient(268.26deg, #097d8d, #60a654 102.45%);

        background-size: 0% 3px;
        background-repeat: no-repeat;
        background-position: left bottom;
        transition: background-size 400ms ease;

        &:hover {
            background-size: 100% 3px;
        }
    }

    .description-text {
        @apply text-lg font-medium pt-3;
    }

    .section-img {
        @apply rounded object-contain self-start px-5 pt-1 pl-8 md:w-[55%] md:pt-0 lg:ml-16;
    }

    /* Do not use the animations for now because it looks bad */
    .hidden-elem {
        opacity: 0.2;
        filter: blur(3px);
        transform: translateY(-10px);
        transition: all calc(300ms * var(--delay));
    }

    .show {
        /* z-index: -10; */
        opacity: 1;
        filter: blur(0);
        transform: translateY(0);
    }
</style>
