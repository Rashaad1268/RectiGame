export enum TopicPermissionIndexes {
    // Explicitly define the permission indexes
    send_messages = 0,
    view_messages = 1,
    create_posts = 2,
    view_posts = 3,
    create_post_replies = 4,
    view_post_replies = 5,
    use_custom_emojis = 6,
    topic_admin = 7,
    topic_moderator = 8
    // if new permissions are created, add it to the end
}

export function getPermission(value: number, permission: number) {
    return value >> permission > 0;
}

export function has_permissions(value: number, permissions: number) {
    return (value & permissions) == permissions;
}
