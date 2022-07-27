<template>
    <div class="row mt-5">
        <div class="col-sm-8 my-5">
            <h2>Страница входа</h2>
            <p class="lead">Описание</p>
        </div>
        <div class="col-sm-4" v-if="currentSection == 'login'">
            <div class="alert alert-danger" v-if="loggingData.incorrectPassword" role="alert">
                Неверная почта или пароль.
            </div>
            <form v-on:submit="authUser($event)">
                <div class="mb-3">
                    <label for="email" class="form-label">Почта</label>
                    <input type="email" class="form-control" v-model="loginData.email" id="email" required>
                    <div id="emailHelp" class="form-text">Почта не передается третьим лицам</div>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Пароль</label>
                    <input type="password" class="form-control" v-model="loginData.password" required minlength="8" id="password">
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" required v-model="loginData.wantToLogin" id="wantToLogin">
                    <label class="form-check-label" for="wantToLogin">Хочу войти</label>
                </div>
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button type="submit" v-if="!loggingData.isLoading" :disabled="!loginData.wantToLogin" class="btn btn-primary">Войти</button>
                    <button class="btn btn-primary" v-else type="button" disabled>
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        Войти
                    </button>
                    <button type="button" class="btn btn-secondary" @click="this.currentSection = 'register'">Регистрация</button>
                </div>
            </form>
        </div>
        <div class="col-sm-4" v-else-if="currentSection == 'register'">
            <div class="section_navigator">
                <h2><span @click="this.currentSection = 'login'"><i class="bi bi-arrow-left"></i></span> Регистрация</h2>
            </div>
            <form>
                <div class="my-3">
                    <label class="form-label">Ваша почта</label>
                    <input type="email" class="form-control" v-model="registerData.email" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Пароль</label>
                    <input type="password" class="form-control" v-model="registerData.password" minlength="8" maxlength="32" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Имя</label>
                    <input type="text" class="form-control" v-model="registerData.first_name" minlength="2" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Фамилия</label>
                    <input type="text" class="form-control" v-model="registerData.last_name" minlength="2" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Гендер</label>
                    <select class="form-select" v-model="registerData.gender" required>
                        <option value="1">Девочка</option>
                        <option value="2">Мальчик</option>
                    </select>
                </div>
                <div class="mb-4 form-check">
                    <input type="checkbox" class="form-check-input" required v-model="loginData.wantToReg" id="wantToLogin">
                    <label class="form-check-label" for="wantToLogin">Хочу зарегистрироваться</label>
                </div>
                <button type="submit" class="btn btn-primary" v-if="!registeringData.isLoading" :disabled="registerData.wantToReg">Регистрация</button>
                <button class="btn btn-primary" v-else type="button" disabled>
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Регистрация
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
            registerData: {
                email: "",
                password: "",
                first_name: "",
                last_name: "",
                gender: null,
                wantToReg: false
            },
            loggingData: {
                isLoading: false,
                incorrectPassword: false
            },
            registeringData: {
                isLoading: false
            },
            currentSection: "login"
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

                        window.location.reload()
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

<style lang="scss">
.section_navigator {
    h2 {
        span {
            margin-right: 7px;

            &:hover {
                cursor: pointer;
                color: var(--bs-primary);
            }
        }
    }
}
</style>