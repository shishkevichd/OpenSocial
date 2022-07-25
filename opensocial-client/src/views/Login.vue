<template>
    <div class="row mt-5">
        <div class="col-sm-8 my-5">
            <h2>Страница входа</h2>
            <p class="lead">Описание</p>
        </div>
        <div class="col-sm-4">
            <div class="alert alert-danger" v-if="loggingData.incorrectPassword" role="alert">
                Неверная почта или пароль.
            </div>
            <form v-on:submit="authUser($event)">
                <div class="mb-3">
                    <label for="email" class="form-label">Почта</label>
                    <input type="email" class="form-control" v-model="loginData.email" id="email" required aria-describedby="emailHelp">
                    <div id="emailHelp" class="form-text">Почта не передается третьим лицам</div>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Пароль</label>
                    <input type="password" class="form-control" v-model="loginData.password" minlength="8" id="password">
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" v-model="loginData.wantToLogin" id="wantToLogin">
                    <label class="form-check-label" for="wantToLogin">Хочу войти</label>
                </div>
                <button type="submit" v-if="!loggingData.isLoading" :disabled="!loginData.wantToLogin" class="btn btn-primary">Войти</button>
                <button class="btn btn-primary" v-else type="button" disabled>
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Войти
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import OpenSocial from '../opensocial/api'

export default {
    data() {
        return {
            loginData: {
                email: "",
                password: "",
                wantToLogin: false
            },
            loggingData: {
                isLoading: false,
                incorrectPassword: false
            }
        }
    },
    methods: {
        authUser(e) {
            e.preventDefault()

            this.loggingData.isLoading = true

            OpenSocial.request('users/login', {
                email: this.loginData.email,
                password: this.loginData.password
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data['success']) {
                        localStorage.setItem('session_json', JSON.stringify(data['data']))

                        this.loggingData.isLoading = false

                        this.$router.push({ path: '/' })
                    } else {
                        if (data['why'] == 'incorrect_password_or_email') {
                            this.loginData.email = ""
                            this.loginData.password = ""
                            this.loginData.wantToLogin = false

                            this.loggingData.incorrectPassword = true
                            this.loggingData.isLoading = false
                        }
                    }
                })
        }
    }
}
</script>