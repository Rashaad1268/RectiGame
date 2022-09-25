<script lang="ts">
	import { Dialog, DialogOverlay, Transition, TransitionChild } from '@rgossiaux/svelte-headlessui';

	export let isOpen: boolean;
	export let textAlign: 'left' | 'center' | 'right' = 'center';
</script>

<dir class="pl-0">
	<Transition show={isOpen}>
		<Dialog on:close={() => (isOpen = false)} {...$$restProps}>
			<div class="fixed z-10 inset-0 overflow-y-auto flex justify-center items-center">
				<div class="block items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
					<TransitionChild
						enter="ease-out duration-300"
						enterFrom="opacity-0"
						enterTo="opacity-75"
						leave="ease-in duration-200"
						leaveFrom="opacity-75"
						leaveTo="opacity-0"
						entered="opacity-75"
					>
						<DialogOverlay class="fixed inset-0 bg-base-100 transition-opacity" />
					</TransitionChild>

					<TransitionChild
						enter="ease-out transform duration-300"
						enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
						enterTo="opacity-100 translate-y-0 sm:scale-100"
						leave="ease-in transform duration-200"
						leaveFrom="opacity-100 translate-y-0 sm:scale-100"
						leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
					>
						<!-- This element is to trick the browser into centering the modal contents. -->
						<div class="inline-block align-middle w-0 h-[55vh] sm:h-screen md:h-[80vh]" aria-hidden="true">
							<!-- Keep this empty because this has no use other than centering the modal -->
						</div>

						<div
							class="inline-block align-bottom bg-base-200 px-[10%] py-7 border border-base-300
									rounded-3xl text-{textAlign} overflow-hidden shadow-xl transform transition-all
									sm:align-middle modal-box"
						>
							<slot />
						</div>
					</TransitionChild>
				</div>
			</div>
		</Dialog>
	</Transition>
</dir>
