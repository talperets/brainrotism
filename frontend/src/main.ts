import { createApp } from 'vue'
import App from './App.vue'
import {router} from './assets/router';

createApp(App)
.use(router)
.mount('#app')
