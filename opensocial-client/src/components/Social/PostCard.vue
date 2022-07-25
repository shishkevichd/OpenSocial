<template>
    <div class="card opensocial_post_card mb-3">
        <div class="card-header">
            <div class="post_author">
                <img class="post_author_avatar" :src="post.creator.creator_type == 'user' ? post.creator.data.avatar_url : `https://avatars.dicebear.com/api/identicon/group.svg`" alt="Avatar">
                <div class="post_meta">
                    <span class="user">{{ post.creator.creator_type == 'group' ? post.creator.data.group_name : `${post.creator.data.first_name} ${post.creator.data.last_name}` }}</span>
                    <span class="date">{{ post.create_datetime }}</span>
                </div>
            </div>
            <ul class="post_card_icons">
                <li class="card_icon"><i class="bi bi-three-dots"></i></li>
            </ul>
        </div>
        <div class="card-body">
            <p class="card-text">{{ post.content }}</p>
            <div class="post_card_footer">
                <ul class="footer_buttons">
                    <li class="footer_button">
                        <i class="bi bi-heart-fill"></i> <span>4K</span>
                    </li>
                    <li class="footer_button">
                        <i class="bi bi-chat-left-fill"></i> <span>4K</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        post: {
            required: true,
            type: Object
        }
    }
}
</script>

<style lang="scss">
.opensocial_post_card {
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: transparent;

        .post_author {
            display: flex;
            align-items: center;

            .post_author_avatar {
                width: 40px;
                border-radius: 2px;
                height: 40px;
                margin-right: 13px;
            }

            .post_meta {
                display: flex;
                flex-direction: column;
                margin-bottom: 2px;

                .user {
                    font-size: 12pt;
                    font-weight: 600;
                    margin-bottom: -2px;
                }

                .date {
                    font-size: 10pt;
                    color: var(--bs-gray-600);
                }
            }
        }

        ul {
            margin-bottom: 0;
            list-style: none;
            display: flex;

            li {
                font-size: 14pt;
                margin-right: 20px;

                &:last-child {
                    margin-right: 0;
                }
            }
        }
    }

    .card-body {
        .post_card_footer {
            float: right;
            margin-bottom: 0;
            .footer_buttons {
                margin-bottom: 0;
                list-style: none;
                display: flex;

                .footer_button {
                    margin-right: 20px;

                    color: var(--bs-gray-600);

                    &:last-child {
                        margin-right: 0;
                    }

                    &:hover {
                        cursor: pointer;
                        color: var(--bs-gray-800);
                    }

                    i.bi {
                        margin-right: 4px;
                    }

                    span {
                        font-weight: 600;
                        text-transform: uppercase;
                    }
                }
            }
        }
    }
}
</style>