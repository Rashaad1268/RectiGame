<script lang="ts">
    import { goto } from "$app/navigation";

    import { TextField } from "$lib/components/forms";

    import { fetchApi, formatApiErrors } from "$lib/api";
    import { Form } from "$lib/components/forms";
    import Button from "$lib/components/button.svelte";
    import { fetchUserData } from "$lib/utils";
    import BackgroundGrid from "../backgroundGrid.svelte";
    import { page } from "$app/stores";
    import { initWebSocket } from "$lib/ws";
    import { addToast } from "$lib/stores";

    $: nextEndpoint = $page.url.searchParams.get("next");

    let email: string;
    let password: string;
    let errorMessages: string[] = [];

    const handleLogin = async (e: any) => {
        e.preventDefault();
        const response = await fetchApi("auth/login/", {
            method: "POST",
            body: JSON.stringify({
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
    <title>Login</title>
</svelte:head>

<BackgroundGrid />

<div class="login-form">
    <div class="max-w-md w-full">
        <div>
            <h2
                class="mt-8 text-center nested-green text-3xl font-gamer
				 text-gray-700 dark:text-gray-400"
            >
                Welcome back, <span>Gamer</span>
            </h2>
            <p class="mt-2 text-center font-monocraft text-sm">
                Don't have an account?
                <a href="signup{nextEndpoint ? `?next=${nextEndpoint}` : ''}" class="link">Signup</a
                >
            </p>
        </div>
        <Form class="mt-6" on:submit={handleLogin} bind:errorMessages>
            <div class="rounded-md shadow-sm">
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
                        autocomplete="current-password"
                        class="outline-active"
                        placeholder="Password"
                        required
                    />
                </div>
            </div>

            <Button
                aria-label="login button"
                type="submit"
                class="flex items-center justify-center group relative !w-full mt-4 !h-12 !p-4 py-5"
            >
                Login
            </Button>
        </Form>
    </div>
</div>

<style lang="scss">
    .login-form {
        @apply flex items-center justify-center z-10;

        left: 50%;
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
    }
</style>
