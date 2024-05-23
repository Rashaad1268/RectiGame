import enum


class TopicPermissionIndexes(enum.IntEnum):
    # don't use enum.auto(), be more explicit
    send_messages = 0
    view_messages = 1
    create_posts = 2
    view_posts = 3
    create_post_replies = 4
    view_post_replies = 5
    use_custom_emojis = 6
    topic_admin = 7
    topic_moderator = 8
    # If new permissions are added, add it in the end or else the order will mess up

    @property
    def permission(self):
        return 1 << self


def get_permission(value: int, permission: int) -> bool:
    return (value >> permission) > 0


def has_permissions(value: int, permissions: int) -> bool:
    return (value & permissions) == permissions


default_permissions = (
    TopicPermissionIndexes.send_messages.permission
    | TopicPermissionIndexes.view_messages.permission
    | TopicPermissionIndexes.create_posts.permission
    | TopicPermissionIndexes.view_posts.permission
    | TopicPermissionIndexes.create_post_replies.permission
    | TopicPermissionIndexes.view_post_replies.permission
    | TopicPermissionIndexes.use_custom_emojis.permission
)
