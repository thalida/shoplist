import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(vue3GoogleLogin, {
  clientId: import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID,
});
app.use(router)

app.mount('#app')
