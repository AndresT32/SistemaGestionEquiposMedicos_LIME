<template>
  <div class="page-wrap">

    <header class="page-header">
      <h1 class="title">Dar de baja un equipo</h1>
      <p class="subtitle">Buscar un equipo por nombre o código y realizar la baja institucional.</p>
    </header>

    <div class="content-container">
      
      <section class="card">
        <div class="card-head">
          <div>
            <h2>Búsqueda de Activos</h2>
            <p class="card-sub">Localice el equipo que desea retirar</p>
          </div>
        </div>
        
        <div class="card-body">
          <div class="field">
            <label>Buscar equipo (Nombre o Código)</label>
            <div class="search-row">
              <input 
                v-model="searchQuery"
                @input="buscarEquipo"
                class="input search-input"
                placeholder="Ingrese código de inventario o nombre..."
              />
              <button v-if="searchQuery" class="btn-clean" @click="limpiarBusqueda" title="Limpiar búsqueda">
                Limpiar
              </button>
            </div>
            
            <div v-if="equipos.length > 0" class="results-list">
              <div 
                class="result-item"
                v-for="e in equipos" 
                :key="e.codigo_inventario"
                @click="seleccionarEquipo(e)"
              >
                <div class="result-code">{{ e.codigo_inventario }}</div>
                <div class="result-name">{{ e.nombre }}</div>
              </div>
            </div>
            <div v-else-if="searchQuery && equipos.length === 0" class="no-results">
              No se encontraron coincidencias.
            </div>
          </div>
        </div>
      </section>

      <transition name="fade">
        <section v-if="equipo" class="card ficha-card">
          <div class="card-head">
            <div>
              <h2>Información del equipo</h2>
              <p class="card-sub">Verifique los datos antes de proceder</p>
            </div>
          </div>

          <div class="card-body">
            <div class="info-grid">
              <div class="info-group">
                <label>Código Inventario</label>
                <div class="info-value highlight">{{ equipo.codigo_inventario }}</div>
              </div>
              <div class="info-group">
                <label>Nombre</label>
                <div class="info-value">{{ equipo.nombre }}</div>
              </div>
              <div class="info-group">
                <label>Marca</label>
                <div class="info-value">{{ equipo.marca || 'N/A' }}</div>
              </div>
              
              <div class="info-group">
                <label>Modelo</label>
                <div class="info-value">{{ equipo.modelo || 'N/A' }}</div>
              </div>
              <div class="info-group">
                <label>Serie</label>
                <div class="info-value">{{ equipo.serie || 'N/A' }}</div>
              </div>
              <div class="info-group">
                <label>Registro INVIMA</label>
                <div class="info-value">{{ equipo.registro_invima || 'N/A' }}</div>
              </div>

              <div class="info-group">
                <label>Sede</label>
                <div class="info-value">{{ equipo.sede__nombre || 'N/A' }}</div>
              </div>
              <div class="info-group">
                <label>Servicio</label>
                <div class="info-value">{{ equipo.servicio__nombre || 'N/A' }}</div>
              </div>
              <div class="info-group">
                <label>Ubicación</label>
                <div class="info-value">{{ equipo.ubicacion || 'N/A' }}</div>
              </div>
            </div>

            <hr class="divider" />

            <div class="action-area">
              <h3>Justificación de la baja</h3>
              <p class="instruction">Por favor describa detalladamente el motivo técnico o administrativo para dar de baja este activo.</p>

              <textarea 
                v-model="motivo"
                class="textarea"
                placeholder="Escriba aquí la justificación..."
              ></textarea>

              <div class="btn-container">
                <button class="btn-danger" @click="darDeBaja">
                  Confirmar Baja del Equipo
                </button>
              </div>

              <div v-if="mensaje" class="message-box" :class="{'success': mensaje.includes('correctamente'), 'error': !mensaje.includes('correctamente')}">
                {{ mensaje }}
              </div>
            </div>
          </div>
        </section>
      </transition>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DarDeBaja",
  data() {
    return {
      searchQuery: "",
      equipos: [],
      equipo: null,
      motivo: "",
      mensaje: ""
    };
  },

  methods: {
    async buscarEquipo() {
      if (!this.searchQuery) {
        this.equipos = [];
        return;
      }

      try {
        const res = await axios.get(
          `http://localhost:8081/api/equipos?q=${encodeURIComponent(this.searchQuery)}`
        );

        this.equipos = res.data.equipos || [];
      } catch (e) {
        this.equipos = [];
      }
    },

    seleccionarEquipo(e) {
      this.equipo = e;
      this.equipos = []; // Limpiar lista al seleccionar
    },

    limpiarBusqueda() {
      this.searchQuery = "";
      this.equipos = [];
      this.equipo = null;
      this.motivo = "";
      this.mensaje = "";
    },

    async darDeBaja() {
      if (!this.motivo.trim()) {
        this.mensaje = "Debe ingresar un motivo de baja.";
        return;
      }

      // Se asume que existe el objeto usuario en sessionStorage según lógica original
      const usuarioSession = sessionStorage.getItem("usuario");
      const usuario = usuarioSession ? JSON.parse(usuarioSession).usuario : "Desconocido";

      try {
        const res = await axios.put(
          `http://localhost:8081/api/dar_baja/equipo/${this.equipo.codigo_inventario}/dar_baja/`,
          {
            motivo_baja: this.motivo,
            usuario
          }
        );

        this.mensaje = "Equipo dado de baja correctamente.";
        // Opcional: Actualizar estado local visualmente si se requiere
        if(this.equipo) this.equipo.activo = false;

      } catch (error) {
        this.mensaje = "Error al procesar la baja.";
      }
    }
  }
};
</script>

<style scoped>
/* ---------- Variables y Base ---------- */
:root {
  --lime-800: #005C33;
  --lime-600: #0a7a4a;
  --bg: #f8fbfa;
  --card: #ffffff;
  --muted: #6b7280;
  --border: #e6eef0;
  --danger: #c53030;
}

.page-wrap {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
  color: #07221a;
  background: var(--bg);
}

.page-header {
  margin-bottom: 25px;
  text-align: left;
}

.title {
  font-size: 24px;
  color: #005C33; /* Hardcoded green variable for safety */
  margin: 0;
  font-weight: 800;
}

.subtitle {
  margin: 5px 0 0;
  color: #6b7280;
  font-size: 14px;
}

/* ---------- Cards ---------- */
.card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e6eef0;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
  overflow: hidden;
  margin-bottom: 20px;
  transition: box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 8px 25px rgba(0,0,0,0.06);
}

.card-head {
  padding: 15px 20px;
  background: linear-gradient(180deg,#fbfdfc,#ffffff);
  border-bottom: 1px solid #e6eef0;
}

.card-head h2 {
  margin: 0;
  color: #005C33;
  font-size: 16px;
  font-weight: 700;
}

.card-sub {
  margin: 2px 0 0;
  font-size: 12px;
  color: #6b7280;
}

.card-body {
  padding: 20px;
}

/* ---------- Buscador ---------- */
.field label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #374151;
  font-size: 13px;
}

.search-row {
  display: flex;
  gap: 10px;
}

.input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: #fbfefc;
  outline: none;
  font-size: 14px;
  transition: border-color 0.2s;
}

.input:focus {
  border-color: #0a7a4a;
  box-shadow: 0 0 0 3px rgba(10,122,74,0.1);
}

.btn-clean {
  background: #fff;
  border: 1px solid #d1d5db;
  color: #4b5563;
  padding: 0 15px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-clean:hover {
  background: #f3f4f6;
  color: #1f2937;
}

/* ---------- Resultados de Búsqueda ---------- */
.results-list {
  margin-top: 10px;
  border: 1px solid #e6eef0;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.result-item {
  padding: 10px 15px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background-color: #f0fdf4; /* Verde muy claro */
}

.result-code {
  font-weight: 700;
  color: #005C33;
  font-size: 13px;
}

.result-name {
  color: #374151;
  font-size: 13px;
}

.no-results {
  margin-top: 10px;
  font-size: 13px;
  color: #6b7280;
  font-style: italic;
}

/* ---------- Grid de Información ---------- */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.info-group label {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  color: #6b7280;
  margin-bottom: 4px;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 14px;
  color: #111827;
  font-weight: 500;
}

.info-value.highlight {
  color: #005C33;
  font-weight: 700;
}

/* ---------- Área de Acción ---------- */
.divider {
  border: 0;
  border-top: 1px solid #e6eef0;
  margin: 25px 0;
}

.action-area h3 {
  font-size: 16px;
  color: #374151;
  margin-bottom: 5px;
}

.instruction {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 15px;
}

.textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.textarea:focus {
  border-color: #0a7a4a;
  outline: none;
}

.btn-container {
  display: flex;
  justify-content: flex-end;
}

.btn-danger {
  background: #c53030; /* Rojo conservado por semántica de "Baja" */
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-size: 14px;
  transition: background-color 0.2s, transform 0.1s;
  box-shadow: 0 2px 4px rgba(197, 48, 48, 0.2);
}

.btn-danger:hover {
  background: #9b2c2c;
  transform: translateY(-1px);
}

.btn-danger:active {
  transform: translateY(0);
}

/* ---------- Mensajes ---------- */
.message-box {
  margin-top: 15px;
  padding: 12px 15px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
}

.message-box.success {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.message-box.error {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

/* ---------- Transiciones ---------- */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Responsividad */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}
</style>