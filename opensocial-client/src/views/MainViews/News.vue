<template>
    <div class="mb-3">
        <div class="input-group mb-3">
            <input type="text" class="form-control" v-model="new_post_text" placeholder="Что нового?">
            <button class="btn btn-outline-primary" :disabled="new_post_text.length <= 0" @click="newPost">Пост</button>
        </div>
    </div>
    <div class="mb-3">
        <post-card-vue v-for='post in posts' :post='post'/>
    </div>
</template>

<script>
import OpenSocial from '../../opensocial/api'
import PostCardVue from "../../components/Social/PostCard.vue";

export default {
    data() {
        return {
            sessionUser: JSON.parse(localStorage.getItem('session_json')),
            posts: [],
            new_post_text: ""
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
        newPost() {
            OpenSocial.request('users/createPost', {
                access_token: this.sessionUser['access_token'],
                content: this.new_post_text
            })
                .then((response) => response.json())
                .then((data) => {
                    this.new_post_text = "";
                    this.loadNews()
                })
        }
    },
    components: {
        PostCardVue
    }
}
</script>