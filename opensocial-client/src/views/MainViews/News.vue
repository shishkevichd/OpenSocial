<template>
    <div class="mb-3">
        <post-input @onPosted="loadNews()"/>
    </div>
    <div class="mb-3">
        <post-card-vue v-for='post in posts' :post='post' @onDeleted="loadNews()"/>
    </div>
</template>

<script>
import OpenSocial from '../../opensocial/api'
import PostCardVue from "../../components/Social/PostCard.vue";
import PostInput from '../../components/PostInput.vue';

export default {
    data() {
        return {
            sessionUser: JSON.parse(localStorage.getItem('session_json')),
            posts: []
        }
    },
    mounted() {
        this.loadNews()
    },
    methods: {
        loadNews() {
            OpenSocial.request('users/getPostCompilation', {
                access_token: this.sessionUser['access_token']
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data)
                    this.posts = data['data'].sort((a, b) => { return new Date(b.create_datetime) - new Date(a.create_datetime); })
                })
        },
    },
    components: {
        PostCardVue,
        PostInput
    }
}
</script>