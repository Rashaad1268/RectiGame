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
    created_at: string;
    banner: string | null;
    tags: Array<TopicTagInterface>;
    member_count: number;
    is_member: number;
}
