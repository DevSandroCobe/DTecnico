import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './assets/estilos/index.css'
import 'vue3-toastify/dist/index.css'
import Vue3Toastify from 'vue3-toastify'

const app = createApp(App)

// Aplica primero los plugins y configuraciones
app.use(router)
app.use(Vue3Toastify, {
  autoClose: 3000,
  position: "top-center",
  transition: "slide",
  theme: "colored",
  hideProgressBar: false
})

// Luego monta la app
app.mount('#app')
