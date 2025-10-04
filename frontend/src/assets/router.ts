import { createWebHistory, createRouter } from 'vue-router'

import Search from '../views/HomeView.vue'
import Settings from '../views/SettingsView.vue'
import CharactersLibraryView from '../views/CharactersLibraryView.vue'
import CharactersStore from '../views/CharactersStore.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import MapView from '../views/MapView.vue'
import ProfileView from '../views/ProfileView.vue'

export const router = createRouter({
    routes: [

        { path: '/store', component: CharactersStore },
        { path: '/library', component: CharactersLibraryView },
        { path: '/leaderboard', component: LeaderboardView },
        { path: '/map', component: MapView },
        { path: '/profile', component: ProfileView },

        { path: '/search', component: Search },
        { path: '/settings',  children:  [
            {path: '', component: Settings},
            {path: ':id', component: Settings},
        ]},
        { path: '/', redirect: "/search" },
    ],
    history: createWebHistory(),
})
