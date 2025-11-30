// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import DashboardHome from "../Pages/Dashboard/DashboardHome.vue";
import BuscarEquipo from "../Pages/Gestion/BuscarEquipo.vue";
import Login from "../Pages/Login/Login.vue";
import Registro from "../Pages/Login/Registro.vue";
import AgregarEquipo from "../Pages/Gestion/AgregarEquipo.vue"
import EditarEquipo from "../Pages/Gestion/EditarEquipo.vue"
import DarDebaja from "../Pages/Gestion/DarDebaja.vue"

const routes = [
  // 👉 Pantalla inicial: login
  { path: "/", redirect: "/login" },

  {
  path: "/gestion/baja",
  name: "DarDeBaja",
  component: DarDebaja,
  meta: { requiresAuth: true }
},

  { path: "/login", name: "login", component: Login, meta: {hideNavbar: true} },
  { path: "/registro", name: "registro", component: Registro, meta: {hideNavbar: true} },

  // 👉 Rutas protegidas


  { 
    path: "/dashboard",
    name: "dashboard",
    component: DashboardHome,
    meta: { requiresAuth: true }
  },

 { 
    path: "/gestion/nuevo", 
    name: "AgregarEquipo", 
    component: AgregarEquipo }
,
{
path: '/gestion/equipo/editar/:codigo_inventario', // La URL espera el código
        name: 'EditarEquipo', // Este 'name' debe coincidir con el usado en $router.push()
        component: EditarEquipo, // El componente que creaste
        props: true // Permite que el parámetro de la ruta se pase como prop al componente
    }
,

  { 
    path: "/gestion/buscar",
    component: BuscarEquipo,
    meta: { requiresAuth: true }
  },

  {
  path: "/gestion/equipo/:codigo/info",
  name: "EquipoInfo",
  component: () => import("../Pages/Gestion/EquipoInfo.vue"),
  props: true,
  meta: { requiresAuth: true }
  },

  {
    path: "/gestion/equipo/:codigo",
    name: "EquipoDetalle",
    component: () => import("../Pages/Gestion/EquipoDetalle.vue"),
    props: true,
    meta: { requiresAuth: true }
  },

  // 👉 Rutas inexistentes → redirigir al login
  { path: "/:catchAll(.*)", redirect: "/login" },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// =========================================================
//  Protección Global de Rutas
// =========================================================
router.beforeEach((to, from, next) => {
  const raw = sessionStorage.getItem("usuario");
  let usuarioObj = null;

  try {
    usuarioObj = raw ? JSON.parse(raw) : null;
  } catch {
    usuarioObj = null;
  }

  const isLoggedIn = !!(usuarioObj && usuarioObj.usuario);

  // 👉 Si ya está logueado, no dejar entrar a login y registro
  if ((to.path === "/login" || to.path === "/registro") && isLoggedIn) {
    return next("/gestion"); // redirige al módulo principal
  }

  // 👉 Si requiere login y NO está logueado → enviar al login
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next("/login");
  }

  return next();
});

export default router;
