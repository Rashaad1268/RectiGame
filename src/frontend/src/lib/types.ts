export interface PaginatorInterface<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: Array<T>;
}

export interface UserInterface {
    id: number;
    username: string;
    is_staff: boolean;
    profile: {
        about_me: string | null;
        profile_picture: string | null;
        banner_image: string | null;
    };
    is_online: boolean;
    last_online: string;
}

export interface TopicTagInterface {
    name: string;
    slug: string;
}

export interface TopicInterface {
    name: string;
    slug: string;
    description: string;
    image: string;
    icon: string;
    created_at: string;
    banner: string | null;
    tags: Array<TopicTagInterface>;
    member_count: number;
    is_member: boolean;
    channels: Array<TopicChatChannelInterface>;
}

export interface PostInterface {
    id: number;
    topic: string; // The topic slug is only provided
    title: string;
    content: string;
    author: UserInterface;
    created_at: string;
    edited_at: string;
    like_count: number;
    dislike_count: number;
    is_liked: boolean;
    is_disliked: boolean;
}

export interface TopicChatChannelInterface {
    id: number;
    name: string;
    description: string;
    created_at: string;
}

export interface TopicChatMessageInterface {
    id: number;
    author: UserInterface;
    channel: TopicChatChannelInterface;
    content: string;
    created_at: string;
    edited_at: string;
    message_type: number;
}

// -------------------------------
// |    Non API related types    |
// -------------------------------
export interface ToastInterface {
    id: string;
    message: string;
    type?: "success" | "error" | "info";
    icon?: string;
    delay?: number;
}
