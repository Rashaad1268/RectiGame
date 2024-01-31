import type { ToastInterface } from "$lib/types";
import { writable } from "svelte/store";

export const toastStore = writable<ToastInterface[]>([]);

export function addToast(toast: Omit<ToastInterface, "id">) {
    const newToast = {
        ...toast,
        id: Date.now().toString(36) + Math.random().toString(36).substring(2)
    };
    toastStore.update((toasts) => [newToast, ...toasts]);

    setTimeout(() => {
        removeToast(newToast.id);
    }, newToast.delay);
}

export function removeToast(id: ToastInterface["id"]) {
    toastStore.update((toasts) => toasts.filter((toast) => toast.id !== id));
}
