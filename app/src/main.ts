import './assets/main.css'
import 'animate.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createClient } from "villus";
import vue3GoogleLogin from 'vue3-google-login'

import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createClient({
  url:  import.meta.env.VITE_GRAPHQL_URL,
  cachePolicy: 'network-only',
  // cachePolicy: 'cache-and-network',
}));
app.use(createPinia())
app.use(vue3GoogleLogin, {
  clientId: import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID,
});
app.use(router)
app.mount('#app')
