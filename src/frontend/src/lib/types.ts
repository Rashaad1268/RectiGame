export interface PaginatorInterface<T> {
    count: number;
    previous?: string;
    next?: string;
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
    author: TopicMemberInterface;
    created_at: string;
    edited_at: string;
    like_count: number;
    dislike_count: number;
    is_liked: boolean;
    is_disliked: boolean;
}



export interface TopicChatRoomInterface {
    type: number;
    id: number;
    name: string;
    description: string;
    created_at: string;
    topic: string;

    creator: number;
    invite_code: string;
    members: TopicMemberInterface[];
}

export type TopicChatChannelInterface = Omit<TopicChatRoomInterface, "creator" | "invite_code" | "members">

export interface TopicChatMessageInterface {
    id: number;
    author: TopicMemberInterface;
    channel: number;
    content: string;
    created_at: string;
    edited_at: string;
    message_type: number;
}

export interface TopicMemberInterface {
    user: UserInterface;
    topic: string;
    nickname?: string;
    permissions: number;
    joined_at?: string;
    has_left: boolean;
}
