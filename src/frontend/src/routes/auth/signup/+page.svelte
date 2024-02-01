<script lang="ts">
    import { goto } from "$app/navigation";
    import { fetchApi, formatApiErrors } from "$lib/api";
    import Button from "$lib/components/button.svelte";
    import { TextField } from "$lib/components/forms";
    import { fetchUserData } from "$lib/utils";
    import BackgroundGrid from "../backgroundGrid.svelte";
    import Form from "$lib/components/forms/form.svelte";
    import { page } from "$app/stores";
    import { initWebSocket } from "$lib/ws";

    $: nextEndpoint = $page.url.searchParams.get("next");

    let username: string;
    let email: string;
    let password: string;
    let password2: string;

    let errorMessages: string[] = [];

    const handleSignup = async (e: any) => {
        e.preventDefault();

        if (password !== password2) {
            errorMessages = ["Passwords do not match", ...errorMessages];
            return;
        }

        const response = await fetchApi("auth/signup/", {
            method: "POST",
            body: JSON.stringify({
                username,
                email,
                password
            })
        });

        if (response.ok) {
            try {
                const ws = initWebSocket();

                ws.addEventListener("open", () => {
                    fetchUserData().then(() => {
                        goto(nextEndpoint ?? "/");
                    });
                });
            } catch (err) {
                errorMessages = [String(err), ...errorMessages];
            }
        } else {
            errorMessages = formatApiErrors(await response.json());
        }
    };
</script>

<svelte:head>
    <title>Signup</title>
</svelte:head>

<BackgroundGrid />

<div class="signup-form">
    <div class="max-w-md w-full">
        <div>
            <h2
                class="mt-8 text-center nested-green text-3xl font-gamer
					 text-gray-700 dark:text-gray-400"
            >
                Welcome, <span>Gamer</span>
            </h2>
            <p class="mt-2 text-center font-monocraft text-sm">
                Already have an account?
                <a href="login{nextEndpoint ? `?next=${nextEndpoint}` : ''}" class="link">Login</a>
            </p>
        </div>
        <Form class="mt-6" on:submit={handleSignup} {errorMessages}>
            <div class="rounded-md shadow-sm">
                <div>
                    <label for="username" class="sr-only">Username</label>
                    <TextField
                        id="username"
                        bind:value={username}
                        name="username"
                        autocomplete="username"
                        placeholder="Username"
                        class="outline-active"
                        required
                    />
                </div>
                <div>
                    <label for="email" class="sr-only">Email address</label>
                    <TextField
                        id="email"
                        bind:value={email}
                        name="email"
                        type="email"
                        autocomplete="email"
                        class="outline-active"
                        placeholder="Email"
                        required
                    />
                </div>
                <div>
                    <label for="password" class="sr-only">Password</label>
                    <TextField
                        id="password"
                        name="password"
                        type="password"
                        bind:value={password}
                        autocomplete="new-password"
                        class="outline-active"
                        placeholder="Password"
                        required
                    />
                </div>
                <div>
                    <label for="password2" class="sr-only">Password (again)</label>
                    <TextField
                        id="password2"
                        name="password2"
                        bind:value={password2}
                        type="password"
                        autocomplete="new-password"
                        class="outline-active"
                        placeholder="Password (again)"
                        required
                    />
                </div>
            </div>

            <Button
                aria-label="Signup button"
                type="submit"
                class="flex items-center justify-center group relative !w-full mt-4 !h-12 !p-4"
            >
                Signup
            </Button>
        </Form>
    </div>
</div>

<style lang="scss">
    .signup-form {
        @apply flex items-center justify-center z-10;

        left: 50%;
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
    }
</style>
