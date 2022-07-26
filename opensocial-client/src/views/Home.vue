<template>
    <div class="row">
        <div class="col-sm-3 col-md-4 col-xl-3">
            <ul class="list-group opensocial_tabs">
                <router-link class="list-group-item list-group-item-action" v-for="tab in opensocialTabs" :to="tab.link" active-class="active"><i :class="`bi ${tab.icon}`"></i> {{ tab.title }}</router-link>
            </ul>
        </div>
        <div class="col-sm-9 col-md-8 col-xl-9">
            <keep-alive>
                <router-view></router-view>
            </keep-alive>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            opensocialTabs: [
                {
                    title: "Профиль",
                    icon: "bi-person-badge",
                    link: "/profile"
                },
                {
                    title: "Лента",
                    icon: "bi-newspaper",
                    link: "/news"
                },
                {
                    title: "Диалоги",
                    icon: "bi-chat-left-fill",
                    link: "/chat"
                },
                {
                    title: "Группы",
                    icon: "bi-people-fill",
                    link: "/groups"
                },
                {
                    title: "Друзья",
                    icon: "bi-person-lines-fill",
                    link: '/friends'
                },
                {
                    title: "Видео",
                    icon: "bi-camera-video-fill",
                    link: "/videos"
                },
                {
                    title: "Музыка",
                    icon: "bi-music-note-list",
                    link: "/music"
                },
                {
                    title: "Выйти",
                    icon: "bi-box-arrow-right",
                    link: "/logout"
                },
            ]
        }
    }
}
</script>

<style lang="scss">
.opensocial_tabs {
    li {
        i.bi {
            margin-right: 8px;
        }
    }
}
</style>