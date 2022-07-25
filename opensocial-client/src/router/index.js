import { createRouter, createWebHistory } from "vue-router"
import OpenSocial from "../opensocial/api.js"

import Home from "../views/Home.vue"
import Login from "../views/Login.vue"

import News from "../views/MainViews/News.vue"
import Dialogs from "../views/MainViews/Dialogs.vue"
import Groups from "../views/MainViews/Groups.vue"
import Videos from "../views/MainViews/Videos.vue"
import Music from "../views/MainViews/Music.vue"
import Profile from "../views/MainViews/Profile.vue"
import Logout from "../views/MainViews/Logout.vue"

const routes = [
    { 
        path: '/', 
        component: Home,
        redirect: '/news',
        children: [
            {
                path: '/news',
                component: News
            },
            {
                path: '/chat',
                component: Dialogs
            },
            {
                path: '/groups',
                component: Groups
            },
            {
                path: '/videos',
                component: Videos
            },
            {
                path: '/music',
                component: Music
            },
            {
                path: '/profile',
                component: Profile
            },
        ]
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/logout',
        component: Logout
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(async (to, from) => {
    if (!OpenSocial.isLogged() && to.path !== '/login') {
        return { path: '/login' }
    } else if (OpenSocial.isLogged() && to.path == '/login') {
        return { path: '/' }
    }
})

export default router