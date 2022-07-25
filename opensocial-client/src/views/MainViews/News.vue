<template>
    <div class="mb-3">
        <div class="input-group mb-3">
            <input type="text" class="form-control" placeholder="Что нового?">
            <button class="btn btn-outline-primary">Пост</button>
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
            posts: []
        }
    },
    mounted() {
        OpenSocial.request('users/getPostCompilation', {
            access_token: this.sessionUser['access_token']
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                this.posts = data['data']
            })
    },
    components: {
        PostCardVue
    }
}
</script>