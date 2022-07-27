<template>
    <div class="input-group mb-3">
        <input type="text" class="form-control" v-model="new_post_text" placeholder="Что нового?">
        <button class="btn btn-outline-primary" :disabled="new_post_text.length <= 0" @click="newPost">Пост</button>
    </div>
</template>

<script>
import OpenSocial from '../opensocial/api'

export default {
    data() {
        return {
            new_post_text: "",
            sessionUser: JSON.parse(localStorage.getItem('session_json'))
        }
    },
    methods: {
        newPost() {
            OpenSocial.request('users/createPost', {
                access_token: this.sessionUser['access_token'],
                content: this.new_post_text
            })
                .then((response) => response.json())
                .then((data) => {
                    this.new_post_text = "";
                    this.$emit('onPosted')
                })
        }
    }
}
</script>