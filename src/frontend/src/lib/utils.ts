import { fetchApi } from "./api";
import { joinedTopicRooms, joinedTopics, userData } from "./stores";

export function truncate(text: string, maxLen: number) {
    return text.length > maxLen ? text.slice(0, maxLen) + "..." : text;
}

export async function fetchUserData() {
    const response = await fetchApi("auth/users/me/");

    if (response.ok) {
        const data = await response.json();
        userData.set(data["user"]);
        joinedTopics.set(data["joined_topics"]);
        joinedTopicRooms.set(data["joined_rooms"]);
    } else {
        console.error(
            `Failed to fetch user data (status: ${response.status} ${response.statusText})`
        );
    }
}

export function trimText(text: string, length: number) {
    if (text.length > length) {
        return text.substring(0, length) + "...";
    }

    return text;
}

export function isObjEmpty(obj: object) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
}
