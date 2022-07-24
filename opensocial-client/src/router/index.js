import { createRouter, createWebHistory } from "vue-router"
import OSAccounts from "../opensocial/api.js"
import Home from "../views/Home.vue"
import Login from "../views/Login.vue"

const routes = [
    { 
        path: '/', 
        beforeEnter: (to, from) => {
            if (!OSAccounts.isLogged) {
                return {
                    path: '/login'
                }
            } else {
                return {
                    path: '/news'
                }
            }
        },
        children: [
            {
                path: '/news',
                component: Home
            }
        ]
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

export default router