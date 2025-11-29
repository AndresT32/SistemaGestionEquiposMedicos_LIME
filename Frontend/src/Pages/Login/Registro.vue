<template>
  <div class="register-wrapper d-flex align-items-center justify-content-center">

    <div class="register-card shadow-lg d-flex">

      <!-- ==== PANEL IZQUIERDO ==== -->
      <div class="image-panel d-none d-md-flex flex-column justify-content-around align-items-center p-5">
        <img src="@/assets/CJEVlGHA_400x400.jpg"
            alt="Logo de la Universidad de Antioquia"
            class="img-fluid logo-placeholder rounded-3 mt-4">
        
        <h3 class="text-white fw-bold">Registro de Nuevo Usuario</h3>
        
      </div>

      <!-- ==== PANEL DERECHO ==== -->
      <div class="form-panel p-5 d-flex flex-column justify-content-center">

        <h2 class="fw-bold text-dark mb-4 text-center">Registrar Cuenta</h2>

        <form @submit.prevent="registrar">

          <!-- Usuario -->
          <div class="input-container">
            <label class="form-label fw-bold text-dark">Usuario</label>
            <input
              v-model="usuario"
              type="text"
              class="form-control input-light"
              placeholder="Define tu nombre de usuario"
              required
            />
          </div>

          <!-- Contraseña -->
          <div class="input-container">
            <label class="form-label fw-bold text-dark">Contraseña</label>
            <input
              v-model="password"
              type="password"
              class="form-control input-light"
              placeholder="Crea una contraseña segura"
              required
            />
          </div>

          <!-- Rol -->
          <div class="input-container mb-4">
            <label class="form-label fw-bold text-dark">Rol</label>
            <select v-model="rol" class="form-select input-light" required>
              <option disabled value="">Seleccione un rol</option>
              <option>Administrador</option>
              <option>Enfermería</option>
              <option>Ingeniería Clínica</option>
              <option>Auxiliar Técnico</option>
              <option>Bacteriología</option>
              <option>Coordinación</option>
            </select>
            <p class="text-dark text-center"> <br> Asegúrate de seleccionar tu rol correctamente.</p>
          </div>

          <!-- BOTÓN Registrar -->
          <button class="btn btn-register-udea w-100 mb-3" type="submit">
            Registrar
          </button>
        </form>

        <!-- Volver al login -->
        <p class="text-center text-muted mt-3">
          ¿Ya tienes una cuenta?
          <a class="login-link-udea fw-bold" @click="router.push({ name: 'login' })">
            Iniciar Sesión
          </a>
        </p>

        <!-- MENSAJE -->
        <div v-if="mensaje"
             class="alert mt-3"
             :class="exito ? 'alert-success' : 'alert-danger'">
          {{ mensaje }}
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const usuario = ref("");
const password = ref("");
const rol = ref("");
const mensaje = ref("");
const exito = ref(false);

const router = useRouter();

const registrar = async () => {
  mensaje.value = "";

  if (!rol.value) {
    mensaje.value = "Debes seleccionar un rol.";
    exito.value = false;
    return;
  }

  try {
    const res = await axios.post("http://127.0.0.1:8081/api/login/", {
      accion: "registro",
      username: usuario.value,
      password: password.value,
      rol: rol.value
    });

    // Manejo de respuesta según tu API
    if (res.data.success) {
      exito.value = true;
      mensaje.value = res.data.message || "Usuario registrado correctamente.";

      // Limpiar campos
      usuario.value = "";
      password.value = "";
      rol.value = "";

      // Redirigir a login
      setTimeout(() => {
        router.push({ name: "login" });
      }, 1500);
    } else {
      exito.value = false;
      mensaje.value = res.data.error || "No se pudo registrar.";
    }

  } catch (error) {
    // Si el backend devuelve status 400 o 404 con error
    if (error.response && error.response.data && error.response.data.error) {
      mensaje.value = error.response.data.error;
    } else {
      mensaje.value = "Error de conexión con el servidor.";
    }
    exito.value = false;
  }
};
</script>


<style scoped>
/* Colores de la UdeA: Verde Oscuro #005C33 (Principal), Verde Claro #008F4C (Acento) */

/* --- Contenedor general (Fondo claro TailAdmin-style) --- */
.register-wrapper {
  height: 100vh;
  width: 100%;
  background: #f4f7fe; /* Fondo gris claro, limpio y profesional */
  margin: 0;
  padding: 0;
}

/* --- Card dividido (Tamaño y estilo) --- */
.register-card {
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
  display: flex; 
  flex-direction: column;
  justify-content: space-around;
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

/* Botón Registrar (Verde UdeA Principal) */
.btn-register-udea {
  background-color: #005C33; 
  color: white !important;
  padding: 10px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  transition: background-color 0.3s ease, transform 0.2s;
}
.btn-register-udea:hover {
  background-color: #008F4C; /* Acento verde al pasar el ratón */
  transform: translateY(-1px);
}

/* Enlace (Color UdeA de acento) */
.login-link-udea {
    color: #008F4C; 
    text-decoration: none;
    transition: color 0.3s;
}

.login-link-udea:hover {
    color: #005C33;
    text-decoration: underline;
}

/* --- Media Queries (Responsividad) --- */
@media (max-width: 768px) {
  .register-card {
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
</style>