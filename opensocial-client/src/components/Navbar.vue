<template>
    <div class="opensocial_navbar">
        <span class="navbar_title">{{ socialName }}</span>
        <ul class="navbar_links">
            <li class="navbar_link" v-if="!isLogged">
                <a href="/">
                    <i class="bi bi-box-arrow-in-right"></i> Войти
                </a>
            </li>
            <li class="navbar_link" v-if="!isLogged">
                <a href="/">
                    <i class="bi bi-person-plus-fill"></i> Регистрация
                </a>
            </li>
            <li class="navbar_link" v-if="isLogged">
                <a href="/">
                    <i class="bi bi-person-fill"></i> Профиль
                </a>
            </li>
        </ul>
    </div>
</template>

<script>
import packages from "../../package.json"
import OpenSocial from "../opensocial/api"

export default {
    data() {
        return {
            socialName: packages.config.socialname,
            isLogged: OpenSocial.isLogged()
        }
    }
}
</script>

<style lang="scss">
.opensocial_navbar {
    display: flex;
    height: 45px;
    width: 100%;
    justify-content: space-between;
    align-items: center;

    .navbar_title {
        font-weight: 600;
    }

    .navbar_links {
        display: flex;
        list-style: none;
        margin-bottom: 0;

        .navbar_link {
            margin-right: 15px;

            i.bi {
                margin-right: 4px;
            }

            a {
                color: var(--bs-gray-600);
                text-decoration: none;

                &:hover {
                    color: var(--bs-primary);
                }
            }

            &:last-child {
                margin-right: 0;
            }
        }
    }
}
</style>