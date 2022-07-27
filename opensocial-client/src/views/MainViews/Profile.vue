<template>
    <div class="mb-5 text-center" v-if="isLoading">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div class="mb-4" v-if="!isLoading">
        <div class="profile_header">
            <div class="left">
                <img :src="profile.avatar_url" :alt="profile.user_id">
                <div class="profile_meta">
                    <span class="meta_name">{{ profile.full_name }}</span>
                    <span class="meta_status">Test</span>
                </div>
            </div>
            <div class="right">
                <button class="btn btn-primary">Настройки</button>
            </div>
        </div>
    </div>
    <div class="mb-3" v-if="!isLoading">
        <nav>
            <div class="nav nav-tabs" id="nav-tab" role="tablist">
                <button class="nav-link active" id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-posts"
                    type="button" role="tab">Посты</button>
                <button class="nav-link" id="nav-profile-tab" data-bs-toggle="tab" data-bs-target="#nav-groups"
                    type="button" role="tab">Группы</button>
                <button class="nav-link" id="nav-contact-tab" data-bs-toggle="tab" data-bs-target="#nav-friends"
                    type="button" role="tab">Друзья</button>
            </div>
        </nav>
        <div class="tab-content" id="nav-tabContent">
            <div class="tab-pane fade show active" id="nav-posts" role="tabpanel" tabindex="0">
                <div class="my-5 text-center" v-if="posts.isLoading">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="my-3" v-else>
                    <PostInput @onPosted="getNews()"/>
                    <PostCard v-for="post in posts.array" :post="post" @onDeleted="getNews()"/>
                </div>
            </div>
            <div class="tab-pane fade" id="nav-groups" role="tabpanel" tabindex="0">
                <div class="my-5 text-center" v-if="groups.isLoading">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="my-3" v-else>
                    <ul class="list-group">
                        <GroupItem v-for="group in groups.array" :group="group" />
                    </ul>
                </div>
            </div>
            <div class="tab-pane fade" id="nav-friends" role="tabpanel" tabindex="0">...</div>
        </div>
    </div>
</template>

<script>
import OpenSocial from '../../opensocial/api'
import PostCard from '../../components/Social/PostCard.vue'
import GroupItem from '../../components/Social/GroupItem.vue';
import PostInput from '../../components/PostInput.vue';

export default {
    data() {
        return {
            isLoading: true,
            sessionUser: JSON.parse(localStorage.getItem("session_json")),
            profile: {},
            posts: {
                isLoading: true,
                array: []
            },
            groups: {
                isLoading: true,
                array: []
            },
            friends: {
                isLoading: true,
                array: []
            }
        };
    },
    methods: {
        getNews() {
            OpenSocial.request("users/getPosts", {
                "access_token": this.sessionUser.access_token,
                "user_id": ""
            })
                .then((response) => response.json())
                .then((data) => {
                    this.posts.array = data.data.sort((a, b) => { return new Date(b.create_datetime) - new Date(a.create_datetime); });
                    this.posts.isLoading = false;
                });
        },
        getGroups() {
            OpenSocial.request("groups/getSubscribedGroup", {
                "access_token": this.sessionUser.access_token
            })
                .then((response) => response.json())
                .then((data) => {
                    this.groups.array = data.data;
                    this.groups.isLoading = false;
                });
        }
    },
    mounted() {
        OpenSocial.request("users/getUser", {
            "access_token": this.sessionUser.access_token,
            "user_id": ""
        })
            .then((response) => response.json())
            .then((data) => {
                this.profile = data.data;
                this.isLoading = false;
                this.getNews();
                this.getGroups();
            });
    },
    components: { PostCard, GroupItem, PostInput }
}
</script>

<style lang="scss">
.profile_header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .left {
        display: flex;
        align-items: center;

        img {
            width: 72px;
            border-radius: 4px;
            margin-right: 25px;
        }

        .profile_meta {
            display: flex;
            flex-direction: column;

            .meta_name {
                font-size: 20pt;
                font-weight: 600;
                margin: 0;
                padding: 0;
            }

            .meta_status {
                font-size: 12pt;
                color: var(--bs-gray-700);
            }
        }
    }
}
</style>