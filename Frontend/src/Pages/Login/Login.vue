<template>
  <div class="login-wrapper d-flex align-items-center justify-content-center">
    
    <div class="login-card shadow-lg d-flex">

      <!-- ==== PANEL IZQUIERDO (IMAGEN/ILUSTRACIÓN) ==== -->
      <!-- Usa flex-column para apilar, justify-content-around para espacio -->
      <div class="image-panel d-none d-md-flex flex-column justify-content-around align-items-center p-5">

        <!-- Logo UdeA -->
        <img src="@/assets/CJEVlGHA_400x400.jpg"
            alt="Logo de la Universidad de Antioquia"
            class="img-fluid logo-placeholder rounded-3 mt-4">

        <h3 class="text-white fw-bold">Sistema de Gestión</h3>
        <p class="text-light text-center mt-2 mb-4">Laboratorio LIME – Universidad de Antioquia</p>
      </div>


      <!-- ==== PANEL DERECHO (FORMULARIO) ==== -->
      <!-- Usa flex-column para centrar verticalmente, justify-content-center -->
      <div class="form-panel p-5 d-flex flex-column justify-content-center">
        
        <!-- Título Principal -->
        <h2 class="fw-bold text-dark mb-4 text-center">Iniciar Sesión</h2>
        
        <!-- Formulario de Login -->
        <form @submit.prevent="login">
          
          <!-- Usuario -->
          <div class="input-container">
            <label for="usuario" class="form-label text-dark">Usuario</label>
            <input
              v-model="usuario"
              type="text"
              class="form-control input-light"
              id="usuario"
              placeholder="Ingresa tu usuario"
              required
            />
          </div>

          <!-- Password -->
          <div class="input-container mb-4">
            <label for="password" class="form-label text-dark">Contraseña</label>
            <input
              v-model="password"
              type="password"
              class="form-control input-light"
              id="password"
              placeholder="Ingresa tu contraseña"
              required
            />
          </div>

          <!-- Botón Login (VERDE UdeA) -->
          <button type="submit" class="btn btn-login-udea w-100 mb-3" >
            Entrar
          </button>
        </form>

        <!-- Links de ayuda y registro -->
        <div class="d-flex justify-content-between align-items-center text-muted mb-3">
            <div class="form-check">
                <input class="form-check-input check-udea" type="checkbox" id="rememberMe">
                <label class="form-check-label ms-1" for="rememberMe">
                    Recuérdame
                </label>
            </div>
            <a href="#" class="help-link-udea">¿Olvidaste tu contraseña?</a>
        </div>

        <p class="text-center text-muted mt-3">
            ¿No tienes una cuenta? 
            <a href="#" class="register-link-udea fw-bold" @click.prevent="abrirModalRegistro">
                Regístrate
            </a>
        </p>

        <!-- Mensaje de estado -->
        <div v-if="mensaje" class="alert mt-3"
             :class="exito ? 'alert-success' : 'alert-danger'"
             role="alert">
          {{ mensaje }}
        </div>
      </div>

    </div>
  </div>
  <!-- ==== MODAL REGISTRO + CAMBIO DE CONTRASEÑA ==== -->
<div v-if="mostrarModal" class="modal-overlay">
  <div class="modal-box">

    <!-- TÍTULO -->
    <h3 class="modal-title">
      <span v-if="!modoCambioPassword">Acceso al Registro</span>
      <span v-else>Cambiar Contraseña del Administrador</span>
    </h3>

    <!-- =======================
         MODO VALIDAR REGISTRO
         ======================= -->
    <div v-if="!modoCambioPassword">

      <p class="modal-text">Ingresa la contraseña de autorización:</p>

      <input 
        v-model="claveRegistro" 
        type="password" 
        placeholder="Contraseña"
        class="modal-input"
      />

      <div 
        v-if="mensajeRegistro" 
        class="modal-alert"
        :class="exitoRegistro ? 'success' : 'error'"
      >
        {{ mensajeRegistro }}
      </div>

      <div class="modal-actions">
        <button class="btn-cancel" @click="cerrarModal">Cancelar</button>
        <button class="btn-confirm" @click="validarClaveRegistro">Continuar</button>
      </div>

      <!-- 🔧 Botón cambiar contraseña -->
      <div class="text-center mt-3">
        <a href="#" class="change-pass-link" @click.prevent="activarModoCambio">
          ¿Deseas cambiar la contraseña del administrador?
        </a>
      </div>

    </div>

    <!-- =========================
         MODO CAMBIAR CONTRASEÑA
         ========================= -->
    <div v-else>

      <p class="modal-text">Actualiza la contraseña del administrador:</p>

      <input 
        v-model="passwordActual" 
        type="password" 
        placeholder="Contraseña actual"
        class="modal-input"
      />

      <input 
        v-model="passwordNueva" 
        type="password" 
        placeholder="Nueva contraseña"
        class="modal-input"
      />

      <input 
        v-model="passwordConfirm" 
        type="password" 
        placeholder="Confirmar nueva contraseña"
        class="modal-input"
      />

      <div 
        v-if="mensajeCambioPassword" 
        class="modal-alert"
        :class="exitoCambioPassword ? 'success' : 'error'"
      >
        {{ mensajeCambioPassword }}
      </div>

      <div class="modal-actions">
        <button class="btn-cancel" @click="activarModoValidacion">Volver</button>
        <button class="btn-confirm" @click="cambiarPasswordAdmin">Guardar</button>
      </div>

    </div>

  </div>
</div>
</template>

<script setup>
import { ref } from 'vue'
import axios from "axios"
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado
const usuario = ref("")
const password = ref("")
const mensaje = ref("")
const exito = ref(false)

const login = async () => {
  mensaje.value = ""

  try {
    const res = await axios.post("http://127.0.0.1:8081/api/login/", {
      accion: "login",
      username: usuario.value,
      password: password.value,
    })

    if (res.data.success) {
      exito.value = true
      mensaje.value = `Bienvenido, ${res.data.usuario}`

      sessionStorage.setItem(
        "usuario",
        JSON.stringify({ usuario: res.data.usuario })
      )

      window.dispatchEvent(new Event("userLoggedIn"))

      // Navegar correctamente
      setTimeout(() => {
        router.push({ name: "dashboard" })
      }, 200)

    } else {
      exito.value = false
      mensaje.value = res.data.error || "Credenciales incorrectas."
    }

  } catch (err) {
    exito.value = false
    if (err.response) {
      if (err.response.status === 401) {
        mensaje.value = "Contraseña incorrecta."
      } else if (err.response.status === 404) {
        mensaje.value = "Usuario no encontrado."
      } else {
        mensaje.value = "Error en el servidor."
      }
    } else {
      mensaje.value = "No se pudo conectar al servidor."
    }

  } finally {
    password.value = ""
  }
}


/* ===========================
     MODAL GENERAL
=========================== */
const mostrarModal = ref(false)
const modoCambioPassword = ref(false)  // <-- lo movemos arriba para evitar el warning

const abrirModalRegistro = () => {
  mostrarModal.value = true
  modoCambioPassword.value = false
}

const cerrarModal = () => {
  mostrarModal.value = false
}


/* ===========================
     VALIDAR CLAVE DE REGISTRO
=========================== */
const claveRegistro = ref("")
const mensajeRegistro = ref("")
const exitoRegistro = ref(false)

const validarClaveRegistro = async () => {
  try {
    const res = await axios.post("http://127.0.0.1:8081/api/login/", {
      accion: "validar_registro",
      clave: claveRegistro.value  // aquí envías lo que el usuario ingresa
    });

    if (res.data.success) {
      exitoRegistro.value = true;
      mensajeRegistro.value = "Autorización correcta. Redirigiendo...";

      setTimeout(() => {
        cerrarModal();
        router.push({ name: "registro" });
      }, 800);

    } else {
      exitoRegistro.value = false;
      mensajeRegistro.value = res.data.error || "Contraseña incorrecta.";
    }

  } catch (err) {
    exitoRegistro.value = false;
    mensajeRegistro.value = "Error en la validación del servidor.";
  }
};



/* ===========================
     CAMBIO DE CONTRASEÑA ADMIN
=========================== */
const passwordActual = ref("")
const passwordNueva = ref("")
const passwordConfirm = ref("")

const mensajeCambioPassword = ref("")
const exitoCambioPassword = ref(false)

const activarModoCambio = () => {
  modoCambioPassword.value = true
  mensajeRegistro.value = ""
}

const activarModoValidacion = () => {
  modoCambioPassword.value = false
  mensajeCambioPassword.value = ""
}

const cambiarPasswordAdmin = async () => {

  mensajeCambioPassword.value = ""

  if (passwordNueva.value !== passwordConfirm.value) {
    exitoCambioPassword.value = false
    mensajeCambioPassword.value = "Las contraseñas no coinciden."
    return
  }

  try {
    const res = await axios.post("http://127.0.0.1:8081/api/login/", {
      accion: "cambiar_password_admin",
      password_actual: passwordActual.value,
      password_nueva: passwordNueva.value,
    })

    if (res.data.success) {
      exitoCambioPassword.value = true
      mensajeCambioPassword.value = "Contraseña actualizada correctamente."

      passwordActual.value = ""
      passwordNueva.value = ""
      passwordConfirm.value = ""

      setTimeout(() => {
        modoCambioPassword.value = false
        mensajeRegistro.value = ""
      }, 800)

    } else {
      exitoCambioPassword.value = false
      mensajeCambioPassword.value = res.data.error
    }

  } catch (err) {
    exitoCambioPassword.value = false
    mensajeCambioPassword.value = "Error realizando el cambio."
  }
}
</script>


<style scoped>
/* Colores de la UdeA: Verde Oscuro #005C33 (Principal), Verde Claro #008F4C (Acento) */

/* --- Contenedor general (Fondo claro TailAdmin-style) --- */
.login-wrapper {
  height: 100vh;
  width: 100%;
  background: #f4f7fe; /* Fondo gris claro, limpio y profesional */
  margin: 0;
  padding: 0;
}

/* --- Card dividido (Tamaño y estilo) --- */
.login-card {
  width: 900px;
  max-width: 95%; 
  height: 600px; /* Altura fija para el split-screen */
  background: white;
  border-radius: 12px; /* Bordes suaves */
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); /* Sombra elegante */
}

/* Panel izquierdo (Imagen/Ilustración) - Degradado UdeA */
.image-panel {
  width: 45%; 
  background: linear-gradient(to bottom right, #005C33, #008F4C); 
  color: white;
  text-align: center;
  /* Aseguramos que ocupe todo el alto disponible en el card */
  display: flex; /* Asegura que la columna tenga flex para justificar contenido */
  flex-direction: column;
}

/* Panel derecho (Formulario) */
.form-panel {
  width: 55%; 
  background: #ffffff;
}

/* Estilo de Inputs (Fondo claro, borde suave) */
.input-container {
  margin-bottom: 20px;
}

.form-label {
    font-weight: 500;
    color: #333;
}

.input-light {
  border: 1px solid #e2e8f0; /* Borde gris muy claro */
  border-radius: 8px; 
  padding: 0.75rem 1rem;
  height: 50px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.input-light:focus {
  border-color: #008F4C; /* Borde de acento UdeA al enfocar */
  box-shadow: 0 0 0 0.1rem #008f4c30; /* Sombra verde suave */
  outline: none;
}

/* Checkbox estilo UdeA */
.check-udea:checked {
    background-color: #008F4C;
    border-color: #008F4C;
}

/* Botón Login (Verde UdeA Principal) */
.btn-login-udea {
  background-color: #005C33; 
  color: white !important;
  padding: 10px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  transition: background-color 0.3s ease, transform 0.2s;
}
.btn-login-udea:hover {
  background-color: #008F4C; /* Acento verde al pasar el ratón */
  transform: translateY(-1px);
}

/* Enlaces (Color UdeA de acento) */
.help-link-udea, .register-link-udea {
    color: #008F4C; 
    text-decoration: none;
    transition: color 0.3s;
}

.help-link-udea:hover, .register-link-udea:hover {
    color: #005C33;
    text-decoration: underline;
}

/* --- Media Queries (Responsividad) --- */
@media (max-width: 768px) {
  .login-card {
    height: auto; 
    flex-direction: column; 
    width: 90%;
  }

  .image-panel {
    display: none !important; /* Ocultar imagen en móvil */
  }
  
  .form-panel {
    width: 100%;
  }
}

/* Fondo oscurecido */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

/* Caja del modal */
.modal-box {
  background: #fff;
  padding: 25px;
  width: 350px;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.2);
  animation: fadeIn 0.25s ease-out;
}

/* Títulos y textos */
.modal-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.modal-text {
  font-size: 14px;
  margin-bottom: 10px;
}

.modal-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #bbb;
  border-radius: 8px;
  outline: none;
}

/* Alertas */
.modal-alert {
  margin-top: 12px;
  padding: 10px;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
}

.modal-alert.success {
  background: #d4edda;
  color: #155724;
}

.modal-alert.error {
  background: #f8d7da;
  color: #721c24;
}

/* Botones */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 18px;
  gap: 10px;
}

.btn-cancel {
  padding: 8px 14px;
  background: #ccc;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-confirm {
  padding: 8px 14px;
  background: #0f6fff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* Animación suave */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>