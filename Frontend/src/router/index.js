import { createRouter, createWebHistory } from 'vue-router'
import ActaDespachoTraslado from '../components/ActaDespachoTraslado.vue'
import ActaDespachoVenta from '../components/ActaDespachoVenta.vue'
import Migracion from '../components/Migracion.vue'
import HomeView from '../components/HomeView.vue'


const routes = [
  { path: '/', component: HomeView }, // página de inicio
  { path: '/actas-traslados', component: ActaDespachoTraslado },
  { path: '/actas-ventas', component: ActaDespachoVenta },
  { path: '/migracion', component: Migracion }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
