<template>
    <div class="login">
        <h4>OpenSocial</h4>
        <h1>Войдите</h1>
        <form v-on:submit="auth" class="login_form">
            <input type="email" placeholder="Email" required>
            <input type="password" placeholder="Password" required minlength="8">
            <button type="submit($event)">Send</button>
        </form>
    </div>
</template>

<script>
import OSAccounts from "../opensocial/api.js"

export default {
    data() {
        return {
            loginData: {
                login: "",
                password: ""
            }
        }
    },
    methods: {
        auth(e) {
            e.preventDefault()
            OSAccounts.request('users/login', {
                email: this.loginData.login,
                password: this.loginData.password
            })
                .then(response => response.json())
                .then(result => {
                    console.log(result)
                })
        },
    }
}
</script>

<style lang="scss">
.login {
    margin: 8px auto;
    width: 250px;
    
    h4 {
        font-size: 12pt;
        opacity: 0.5;
        margin-bottom: 5px;
    }

    h1 {
        margin-top: 0;
    }

    .login_form {
        display: flex;
        flex-direction: column;
        input {
            padding: 9px 10px;
            font-size: 11pt;
            border: 1px solid #b1b1b1;
            outline: none;
            border-radius: 9px;
            margin: 8px 0;

            &:focus {
                border: 2px solid #2479da;
                padding: 8px 9px;
            }

            &:first-child {
                margin-top: -5px;
            }
        }

        button {
            border-radius: 9px;
            padding: 9px 10px;
            margin-top: 8px;
            color: white;
            border: none;
            background-color: #2479da;
        }
    }
}
</style>