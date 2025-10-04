import { createWebHistory, createRouter } from 'vue-router'

import Search from '../views/HomeView.vue'
import Settings from '../views/SettingsView.vue'

export const router = createRouter({
    routes: [
        { path: '/search', component: Search },
        { path: '/settings',  children:  [
            {path: '', component: Settings},
            {path: ':id', component: Settings},
        ]},
        { path: '/', redirect: "/search" },
    ],
    history: createWebHistory(),
})
