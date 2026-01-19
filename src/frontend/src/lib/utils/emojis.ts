import { fetchApi } from "$lib/api";
import { customEmojiStore } from "$lib/stores";
import { get } from "svelte/store";

const emojiRegex = /&lt;:(\d+):&gt;/g;

// export function parseMessageContentCustomEmojis(content: string): Array<string> {
// return content.matchAll(emojiRegex);
// }

export function parseMessageEmojis(content: string) {
    const emojis = content.matchAll(emojiRegex);
    let newContent = String(content);

    // eslint-disable-next-line no-constant-condition
    for (const emoji of emojis) {
        const emojiHtml = `<span class="size-6 object-contain m-0 inline-block" />`;

        newContent = newContent.replace(emoji[0], emojiHtml);
    }

    return newContent;
}

export async function convertMessageEmojis({ content }: { content: string }) {

    const emojis = content.matchAll(emojiRegex);
    let newContent = String(content);

    for (const emoji of emojis) {
        const emojiId = parseInt(emoji[1]);

        if (!emojiId) {
            continue;
        }

        let emojiData = get(customEmojiStore)[emojiId];
        let emojiHtml = emoji[0];

        if (!emojiData) {
            const response = await fetchApi(`topics/emojis/${emojiId}/`);

            if (response.ok) {
                emojiData = await response.json();
                customEmojiStore.update((customEmojis) => {
                    customEmojis[emojiId] = emojiData;
                    return customEmojis;
                });
            } else {
                // Emoji does not exist...continue
                continue;
            }
        }
        emojiHtml = `<img class="size-6 object-contain m-0 inline-block" src="${emojiData.image}" alt="${emojiData.name} emoji" />`;
        newContent = newContent.replace(emoji[0], emojiHtml);
    }

    return newContent;
}
