import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

import './style.css'
import router from './router/index.js'
import App from './App.vue'

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App)
app.use(router)
app.use(pinia);
app.use(Toast, {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    newestOnTop: true,
    showCloseButtonOnHover: false,
    closeButton: "button",
    icon: true,
    rtl: false
});
app.mount('#app')

