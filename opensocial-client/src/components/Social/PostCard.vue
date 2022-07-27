<template>
    <div class="card opensocial_post_card mb-3">
        <div class="card-header">
            <div class="post_author">
                <img class="post_author_avatar" :src="post.creator.creator_type == 'user' ? post.creator.data.avatar_url : `https://avatars.dicebear.com/api/identicon/group.svg`" alt="Avatar">
                <div class="post_meta">
                    <span class="user">{{ post.creator.creator_type == 'group' ? post.creator.data.group_name : post.creator.data.full_name }} <span v-if="isCreatorIsYou">(вы)</span></span>
                    <span class="date">{{ post.create_datetime }}</span>
                </div>
            </div>
            <ul class="post_card_icons">
                <li class="card_icon" v-if="isCreatorIsYou && !alerts.isDeletedAlert" @click="alerts.isDeletedAlert = true"><i class="bi bi-trash-fill"></i></li>
                <li class="card_icon" v-if="isCreatorIsYou"><i class="bi bi-pencil-fill"></i></li>
            </ul>
        </div>
        <div class="card-body">
            <div class="alert alert-danger delete-alert" v-if="alerts.isDeletedAlert">
                <div class="left">
                    <i class="bi bi-info-circle-fill"></i>
                    <span>Вы хотите удалить этот пост?</span>
                </div>
                <div class="right">
                    <ul>
                        <li @click="deletePost"><i class="bi bi-check2"></i></li>
                        <li @click="alerts.isDeletedAlert = false"><i class="bi bi-x-lg"></i></li>
                    </ul>
                </div>
            </div>
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
import OpenSocial from '../../opensocial/api'
export default {
    props: {
        post: {
            required: true,
            type: Object,
        }
    },
    data() {
        return {
            sessionUser: JSON.parse(localStorage.getItem('session_json')),
            alerts: {
                isDeletedAlert: false,
                isEditedAlert: false,
            }
        }
    },
    methods: {
        deletePost() {
            if (this.post.creator.creator_type == 'user') {
                OpenSocial.request('users/deletePost', {
                    access_token: this.sessionUser.access_token,
                    post_id: this.post.post_id
                })
                    .then((response) => response.json())
                    .then((data) => {
                        this.$emit('onDeleted')
                    });
            } else {
                
            }
        }
    },
    computed: {
        isCreatorIsYou() {
            if (this.post.creator.creator_type == 'user' & this.post.creator.data.user_id == this.sessionUser.user_id) {
                return true
            } else {
                return false
            }
        }
    }
}
</script>

<style lang="scss">
.opensocial_post_card {
    border: 1px solid #dee2e6;
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: transparent;
        border-bottom: 1px solid #dee2e6;

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

                    > span {
                        color: var(--bs-gray-600);
                        font-weight: 400;
                    }
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

                &:hover {
                    cursor: pointer;
                }
            }
        }
    }

    .card-body {
        .delete-alert {
            padding: 7px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;

            .left {
                i.bi {
                    margin-right: 12px;
                }
            }

            .right {
                ul {
                    display: flex;
                    align-items: center;
                    margin-bottom: 0;
                    list-style: none;

                    li {
                        margin-right: 15px;

                        &:last-child {
                            margin-right: 0;
                        }

                        &:hover {
                            cursor: pointer;
                        }
                    }
                }
            }
        }

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