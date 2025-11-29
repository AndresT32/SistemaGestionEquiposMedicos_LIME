  <!-- src/components/MainNavbar.vue -->
  <template>
    <nav class="navbar">

      <!-- Lado izquierdo -->
      <div class="nav-left">
        <div class="brand" @click="openMenu">LIME Gestión ▼</div>

        <div class="nav-links">
          <a :class="linkClass('dashboard')" @click.prevent="goTo('/dashboard')">Dashboard</a>
        </div>
      </div>

      <!-- Lado derecho -->
      <div class="nav-right">
        <div class="user-icon">
          <a class="nav-link" @click="logout">Cerrar sesión 👤</a>
        </div>
      </div>

    </nav>

    <!-- ========= MODAL EMERGENTE ========= -->
    <div v-if="modalOpen" class="modal-overlay" @click="closeMenu">
      <div class="modal-box" @click.stop>
        
        <h2 class="modal-title">Gestión de Equipos</h2>

        <button class="modal-btn" @click="goTo('/gestion/buscar')">
          🔍 Buscar Equipo
        </button>

        <button class="modal-btn" @click="goTo('/gestion/nuevo')">
          ➕ Agregar Equipo
        </button>

        <button class="modal-btn" @click="goTo('/gestion/baja')">
          ⛔ Dar de Baja
        </button>

        <button class="modal-close" @click="closeMenu">
          Cerrar
        </button>

      </div>
    </div>
  </template>


  <script setup>
  import { ref } from "vue"
  import { useRouter, useRoute } from "vue-router"

  /* Router */
  const router = useRouter()
  const route = useRoute()

  /* Modal */
  const modalOpen = ref(false)
  const openMenu = () => { modalOpen.value = true }
  const closeMenu = () => { modalOpen.value = false }

  /* Navegación */
  const goTo = (path) => {
    closeMenu()
    router.push(path)
  }

  /* Estilos activos */
  const linkClass = (routeName) => ({
    "nav-link": true,
    "active": route.name === routeName
  })

  /* Logout */
  const logout = () => {
    sessionStorage.removeItem("usuario")
    closeMenu()
    window.dispatchEvent(new Event("userLoggedOut"))
    router.push({ name: "login" })
  }
  </script>


  <style scoped>
  .navbar {
    --h: 64px;
    height: var(--h);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #008F4C;
    color: white;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 0 20px;
    box-shadow: 0 2px 6px rgba(2,6,23,0.12);
    z-index: 50;
  }

  .nav-left { display:flex; align-items:center; gap:20px; }
  .brand { font-weight:700; font-size:18px; cursor:pointer; }
  .nav-links { display:flex; gap:12px; align-items:center; }
  .nav-link { color: rgba(255,255,255,0.9); text-decoration:none; padding:8px 10px; border-radius:6px; cursor:pointer; font-weight:500; }
  .nav-link:hover { background: rgba(255,255,255,0.06); }
  .nav-link.active { background: white; color: #008F4C; font-weight:700; }
  .nav-right { display:flex; align-items:center; gap:12px; }
  .user-icon { padding:8px; border-radius:50%; cursor:pointer; }

  /* ========= MODAL ========= */
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
  }

  .modal-box {
    background: white;
    padding: 28px;
    border-radius: 16px;
    width: 340px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    text-align: center;
    animation: fadeIn .25s ease-out;
  }

  .modal-title {
    margin-bottom: 16px;
    font-size: 20px;
    font-weight: 700;
  }

  .modal-btn {
    width: 100%;
    padding: 12px;
    margin-bottom: 12px;
    background: #008F4C;
    border: none;
    color: white;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: .2s;
  }
  .modal-btn:hover {
    background: #008F4C;
  }

  .modal-close {
    width: 100%;
    padding: 10px;
    background: #ddd;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 6px;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: scale(.96); }
    to { opacity: 1; transform: scale(1); }
  }
  </style>