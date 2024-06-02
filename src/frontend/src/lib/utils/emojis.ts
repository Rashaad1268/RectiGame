import { fetchApi } from "$lib/api";
import { customEmojiStore } from "$lib/stores";
import { get } from "svelte/store";

const emojiRegex = /(<:(\d+):>)|(&lt;:(\d+):&gt;)/g;

// export function parseMessageContentCustomEmojis(content: string): Array<string> {
// return content.matchAll(emojiRegex);
// }

export function parseMessage(content: string) {
    const emojis = content.matchAll(emojiRegex);
    let newContent = String(content);

    // eslint-disable-next-line no-constant-condition
    while (true) {
        const emoji = emojis.next().value;

        if (!emoji) break;

        const emojiHtml = `<span class="size-5 block bg-red-600 object-contain" />`;

        newContent = newContent.replace(emoji[0], emojiHtml);
    }

    return newContent;
}

export async function convertMessageEmojis({ content, topic }: { content: string; topic?: string }) {
    if (!topic) {
        return parseMessage(content);
    }

    const emojis = content.matchAll(emojiRegex);
    let newContent = String(content);

    // eslint-disable-next-line no-constant-condition
    while (true) {
        const emoji = emojis.next().value;

        if (!emoji) break;

        const emojiId = parseInt(emoji[4]);

        if (!emojiId) {
            continue;
        }

        const emojiFromCache = get(customEmojiStore)[emojiId];
        let emojiHtml = emoji[0];

        if (emojiFromCache) {
            emojiHtml = `<img class="size-5 block object-contain" src="${emojiFromCache.image}" alt="${emojiFromCache.name} emoji" />`;
        } else {
            const response = await fetchApi(`topics/${topic}/emojis/${emojiId}/`);
            
            if (response.ok) {
                const emojiData = await response.json();
                customEmojiStore.update((customEmojis) => {
                    customEmojis[emojiId] = emojiData;
                    return customEmojis;
                });
                emojiHtml = `<img class="size-5 object-contain m-0 inline-block" src="${emojiData.image}" alt="${emojiData.name} emoji" />`;
            }
            
        }
        newContent = newContent.replace(emoji[0], emojiHtml);
    }

    return newContent;
}
