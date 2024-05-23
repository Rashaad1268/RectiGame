import { browser } from "$app/environment";
import {toast} from "svelte-sonner"

export const getCookie = (name: string) =>
    document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)")?.pop() || null;

interface CustomRequestInit extends RequestInit {
    csrfToken?: string;
}

export const fetchApi = async (
    endpoint: string,
    options?: CustomRequestInit
): Promise<Response> => {
    const csrfToken = options?.csrfToken ? options?.csrfToken : getCookie("csrftoken");
    const defaultOptions = { ...options };

    defaultOptions.headers = {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...defaultOptions.headers
    };

    if (csrfToken) {
        defaultOptions.headers = { "X-CSRFToken": csrfToken, ...defaultOptions.headers };
    }
    defaultOptions.credentials = "include";
    
    const response = await fetch("/api/" + endpoint, defaultOptions);

    if (!response.ok && browser) {
        toast.error(`Error while fetching api (${response.status} ${response.statusText})`)
    }

    return response;

};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const formatApiErrors = (data: any): Array<string> => {
    const messages: Array<string> = [];
    for (const [key, value] of Object.entries(data)) {
        messages.push(
            `${key !== "detail" ? `${key}: ` : ""}${
                Array.isArray(value) ? value.join(", ") : value
            }`
        );
    }
    return messages;
};
