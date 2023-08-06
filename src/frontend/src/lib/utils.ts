import { fetchApi } from './api';
import { joinedTopics, userData } from './stores';

export function truncate(text: string, maxLen: number) {
	return text.length > maxLen ? text.slice(0, maxLen) + '...' : text;
}

export async function fetchUserData() {
	const response = await fetchApi('auth/users/me/');

	const responseData = await response.json();
	userData.set(responseData['user']);
	joinedTopics.set(responseData['joined_topics']);
}
