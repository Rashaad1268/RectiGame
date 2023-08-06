<script lang="ts">
	import { toastStore } from "$lib/stores/";
	import { onMount } from "svelte";

	let activate = false;
	let currentToast: any;
	let timeout: NodeJS.Timeout;
	let defaultIcons: any = {
		success: "✔",
		error: "❌",
		info: "ℹ️"
	};

	onMount(() => {
		toastStore.subscribe((msg) => {
			currentToast = msg;
			clearTimeout(timeout);
			if (msg) {
				timeout = setTimeout(() => {
					toastStore.set(null);
				}, msg?.delay || 10000);

				// delay hack for better animations
				activate = false;
				setTimeout(() => {
					activate = true;
				}, 200);
			}
		});
	});

	$: typeClass = currentToast?.type || "info";
</script>

{#if currentToast}
	<button
		name="close alert button"
		class="toast toast-start items-center flex-row {typeClass}"
		on:click={() => toastStore.set(null)}
		class:active={activate}
	>
		<div class="icon">
			{#if currentToast.icon}
				{currentToast.icon}
			{:else}
				{defaultIcons[currentToast.type ?? "info"]}
			{/if}
		</div>

		<p class="text-white sm:p-1 md:p-3">
			{currentToast.message}
		</p>
	</button>
{/if}

<style lang="postcss">
	.toast {
		@apply fixed m-6 cursor-pointer opacity-0 invisible rounded-lg -translate-x-80 transition-all ease-in-out z-[999];
	}
	.toast.active {
		@apply translate-x-0 visible opacity-100;
	}

	.toast.success {
		@apply bg-emerald-500;
	}

	.toast.error {
		@apply bg-red-500;
	}

	.toast.info {
		@apply bg-blue-500;
	}

	.icon {
		@apply text-white text-lg pl-1 py-1 grid place-items-center;
	}
</style>
