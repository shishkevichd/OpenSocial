import { createRouter, createWebHistory } from "vue-router"
import OpenSocial from "../opensocial/api.js"
import Home from "../views/Home.vue"
import Login from "../views/Login.vue"

const routes = [
    { 
        path: '/', 
        component: Home
    },
    {
        path: '/login',
        component: Login
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