<template>
  <div class="page-wrap">

    <header class="page-header">
      <h1 class="title">Gestión de Bajas</h1>
      <p class="subtitle">Administración de retiros y consulta de historial.</p>
    </header>

    <div class="tabs-container">
      <button 
        class="tab-btn" 
        :class="{ active: !mostrarHistorial }" 
        @click="cambiarModo(false)"
      >
        ⛔ Dar de Baja un Equipo
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: mostrarHistorial }" 
        @click="cambiarModo(true)"
      >
        📜 Ver Historial de Bajas
      </button>
    </div>

    <div class="content-container">
      
      <div v-if="!mostrarHistorial" class="fade-in">
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
                No se encontraron equipos <b>activos</b> con ese criterio.
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

      <div v-else class="fade-in">
        <section class="card">
          <div class="card-head">
            <div>
              <h2>Historial de Equipos Dados de Baja</h2>
              <p class="card-sub">Listado completo de equipos inactivos</p>
            </div>
            
            <div class="historial-controls">
                <input 
                    v-model="searchHistoryQuery" 
                    placeholder="🔍 Buscar en historial..." 
                    class="input-small"
                >
                <button class="btn-refresh" @click="cargarHistorial" title="Actualizar lista">
                🔄
                </button>
            </div>
          </div>
          
          <div class="card-body table-responsive">
            <table class="bajas-table" v-if="bajasFiltradas.length > 0">
              <thead>
                <tr>
                  <th>Acciones</th> <th>Fecha Baja</th>
                  <th>Motivo</th>
                  <th>Código</th>
                  <th>Nombre</th>
                  <th>Riesgo</th>
                  <th>Sede</th>
                  <th>Marca</th>
                  <th>Modelo</th>
                  <th>Serie</th>
                  <th>Invima</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in bajasFiltradas" :key="item.codigo_inventario">
                  
                  <td class="col-acciones">
                    <div class="btn-group">
                        <button class="btn-ver" @click="verDetalle(item.codigo_inventario)" title="Ver toda la información">
                            Ver Todo
                        </button>
                        <button class="btn-activar" @click="reactivarEquipo(item)" title="Volver a activar equipo">
                            Activar
                        </button>
                    </div>
                  </td>

                  <td class="col-fecha">{{ item.fecha_baja || 'NI' }}</td>
                  <td class="col-motivo" :title="item.motivo_baja">
                    {{ item.motivo_baja ? (item.motivo_baja.substring(0,40) + (item.motivo_baja.length>40?'...':'')) : 'Sin motivo' }}
                  </td>
                  <td class="font-bold">{{ item.codigo_inventario }}</td>
                  <td>{{ item.nombre }}</td>
                  <td>
                    <span class="badge-riesgo">{{ item.clasificacion_riesgo || 'N/A' }}</span>
                  </td>
                  <td>{{ item.sede__nombre || 'N/A' }}</td>
                  <td>{{ item.marca || 'N/A' }}</td>
                  <td>{{ item.modelo || 'N/A' }}</td>
                  <td>{{ item.serie || 'N/A' }}</td>
                  <td>{{ item.registro_invima || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
            
            <div v-else class="no-results-box">
              <p v-if="searchHistoryQuery">No hay resultados para "{{ searchHistoryQuery }}"</p>
              <p v-else>No se encontraron equipos dados de baja en el sistema.</p>
            </div>
          </div>
        </section>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DarDeBaja",
  data() {
    return {
      // Estado de Vistas
      mostrarHistorial: false,

      // Estado Vista 1: Dar de Baja
      searchQuery: "",
      equipos: [],
      equipo: null,
      motivo: "",
      mensaje: "",

      // Estado Vista 2: Historial
      listaBajas: [],
      searchHistoryQuery: "" // Variable para el buscador del historial
    };
  },

  computed: {
    // FILTRO EN TIEMPO REAL PARA EL HISTORIAL
    bajasFiltradas() {
        if (!this.searchHistoryQuery) return this.listaBajas;
        
        const q = this.searchHistoryQuery.toLowerCase();
        return this.listaBajas.filter(item => {
            return (
                (item.nombre && item.nombre.toLowerCase().includes(q)) ||
                (item.codigo_inventario && item.codigo_inventario.toLowerCase().includes(q)) ||
                (item.marca && item.marca.toLowerCase().includes(q))
            );
        });
    }
  },

  methods: {
    // --- Control de Pestañas ---
    cambiarModo(historial) {
      this.mostrarHistorial = historial;
      if (historial) {
        this.cargarHistorial();
      } else {
        this.limpiarBusqueda();
      }
    },

    // --- Lógica REACTIVAR ---
    async reactivarEquipo(item) {
        if(!confirm(`¿Estás seguro de que quieres REACTIVAR el equipo ${item.codigo_inventario}? Pasará a estar disponible nuevamente.`)) {
            return;
        }

        try {
            const encodedCode = encodeURIComponent(item.codigo_inventario);
            await axios.put(`http://localhost:8081/api/dar_baja/equipo/${encodedCode}/reactivar/`);
            
            alert("Equipo reactivado correctamente.");
            this.cargarHistorial(); // Recargar la lista para que desaparezca de bajas

        } catch (error) {
            console.error(error);
            alert("Error al reactivar el equipo.");
        }
    },

    // --- Lógica VER TODO ---
    verDetalle(codigo) {
        const encodedCode = encodeURIComponent(codigo);
        // Navega a la pantalla de EquipoInfo
        this.$router.push(`/gestion/equipo/${encodedCode}/info`);
    },

    // --- Métodos Vista 1: Dar de Baja ---
    async buscarEquipo() {
      if (!this.searchQuery) {
        this.equipos = [];
        return;
      }

      try {
        const res = await axios.get(
          `http://localhost:8081/api/equipos?q=${encodeURIComponent(this.searchQuery)}`
        );
        const todos = res.data.equipos || [];
        this.equipos = todos.filter(e => e.activo === true);

      } catch (e) {
        this.equipos = [];
      }
    },

    seleccionarEquipo(e) {
      this.equipo = e;
      this.equipos = []; 
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

      const usuarioSession = sessionStorage.getItem("usuario");
      const usuario = usuarioSession ? JSON.parse(usuarioSession).usuario : "Desconocido";

      try {
        await axios.put(
          `http://localhost:8081/api/dar_baja/equipo/${encodeURIComponent(this.equipo.codigo_inventario)}/dar_baja/`,
          {
            motivo_baja: this.motivo,
            usuario
          }
        );

        this.mensaje = "Equipo dado de baja correctamente.";
        if(this.equipo) this.equipo.activo = false;

        setTimeout(() => {
          this.limpiarBusqueda();
        }, 2000);

      } catch (error) {
        this.mensaje = "Error al procesar la baja.";
        console.error(error);
      }
    },

    // --- Métodos Vista 2: Historial ---
    async cargarHistorial() {
      try {
        const res = await axios.get(`http://localhost:8081/api/equipos/?mostrar_bajas=true`);
        const todos = res.data.equipos || [];
        // Filtro de seguridad
        this.listaBajas = todos.filter(e => e.activo === false);

      } catch (error) {
        console.error("Error cargando historial:", error);
        this.listaBajas = [];
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
  max-width: 1250px; /* Más ancho para las nuevas columnas */
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
  color: #005C33; 
  margin: 0;
  font-weight: 800;
}

.subtitle {
  margin: 5px 0 0;
  color: #6b7280;
  font-size: 14px;
}

/* ---------- PESTAÑAS ---------- */
.tabs-container {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e6eef0;
}

.tab-btn {
  padding: 10px 20px;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  font-size: 15px;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #005C33;
  background-color: #f0fdf4;
}

.tab-btn.active {
  color: #005C33;
  border-bottom-color: #005C33;
  font-weight: 800;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap; /* Para móviles */
  gap: 10px;
}

.card-head h2 {
  margin: 0;
  color: #005C33;
  font-size: 16px;
  font-weight: 700;
}

.card-sub { margin: 2px 0 0; font-size: 12px; color: #6b7280; }
.card-body { padding: 20px; }

/* ---------- CONTROLES DEL HISTORIAL (Buscador pequeño) ---------- */
.historial-controls {
    display: flex;
    align-items: center;
    gap: 10px;
}

.input-small {
    padding: 6px 12px;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
    font-size: 13px;
    width: 200px;
    outline: none;
}
.input-small:focus { border-color: #005C33; }

.btn-refresh {
  background: white;
  border: 1px solid #e6eef0;
  cursor: pointer;
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 6px;
  transition: 0.2s;
}
.btn-refresh:hover { background: #f0fdf4; }

/* ---------- TABLA DE BAJAS ---------- */
.table-responsive { overflow-x: auto; }

.bajas-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1000px;
}

.bajas-table th {
  background-color: #005C33;
  color: white;
  padding: 12px;
  text-align: left;
  white-space: nowrap;
}

.bajas-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
  color: #333;
  vertical-align: middle;
}

.bajas-table tr:hover { background-color: #f9f9f9; }

/* BOTONES DE ACCIÓN EN TABLA */
.btn-group {
    display: flex;
    gap: 6px;
}

.btn-ver {
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: bold;
    cursor: pointer;
}
.btn-ver:hover { background: #0056b3; }

.btn-activar {
    background: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: bold;
    cursor: pointer;
}
.btn-activar:hover { background: #1e7e34; }

.col-acciones { width: 160px; }
.col-fecha { font-weight: 600; color: #c53030; white-space: nowrap; }
.col-motivo { max-width: 200px; line-height: 1.3; font-size: 12px; }
.font-bold { font-weight: 700; }

.badge-riesgo {
  background: #eef1ff;
  color: #005C33;
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid #005C33;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

.no-results-box {
  text-align: center; color: #777; padding: 20px; font-style: italic;
}

/* ---------- Buscador (Original) ---------- */
.field label { display: block; font-weight: 600; margin-bottom: 8px; color: #374151; font-size: 13px; }
.search-row { display: flex; gap: 10px; }
.input {
  width: 100%; padding: 10px 12px; border-radius: 8px;
  border: 1px solid #e2e8f0; background: #fbfefc; outline: none; font-size: 14px;
  transition: border-color 0.2s;
}
.input:focus { border-color: #0a7a4a; box-shadow: 0 0 0 3px rgba(10,122,74,0.1); }
.btn-clean {
  background: #fff; border: 1px solid #d1d5db; color: #4b5563; padding: 0 15px; border-radius: 8px;
  cursor: pointer; font-weight: 600; font-size: 13px; transition: all 0.2s;
}
.btn-clean:hover { background: #f3f4f6; color: #1f2937; }

/* Resultados */
.results-list {
  margin-top: 10px; border: 1px solid #e6eef0; border-radius: 8px;
  max-height: 200px; overflow-y: auto; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.result-item {
  padding: 10px 15px; border-bottom: 1px solid #f3f4f6; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center; transition: background-color 0.2s;
}
.result-item:last-child { border-bottom: none; }
.result-item:hover { background-color: #f0fdf4; }
.result-code { font-weight: 700; color: #005C33; font-size: 13px; }
.result-name { color: #374151; font-size: 13px; }
.no-results { margin-top: 10px; font-size: 13px; color: #6b7280; font-style: italic; }

/* Info Grid */
.info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.info-group label { display: block; font-size: 11px; text-transform: uppercase; color: #6b7280; margin-bottom: 4px; letter-spacing: 0.05em; }
.info-value { font-size: 14px; color: #111827; font-weight: 500; }
.info-value.highlight { color: #005C33; font-weight: 700; }

.divider { border: 0; border-top: 1px solid #e6eef0; margin: 25px 0; }
.action-area h3 { font-size: 16px; color: #374151; margin-bottom: 5px; }
.instruction { font-size: 13px; color: #6b7280; margin-bottom: 15px; }
.textarea { width: 100%; min-height: 100px; padding: 12px; border-radius: 8px; border: 1px solid #d1d5db; font-family: inherit; font-size: 14px; resize: vertical; margin-bottom: 20px; box-sizing: border-box; }
.textarea:focus { border-color: #0a7a4a; outline: none; }

.btn-container { display: flex; justify-content: flex-end; }
.btn-danger { background: #c53030; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; border: none; font-size: 14px; transition: background-color 0.2s, transform 0.1s; box-shadow: 0 2px 4px rgba(197, 48, 48, 0.2); }
.btn-danger:hover { background: #9b2c2c; transform: translateY(-1px); }
.btn-danger:active { transform: translateY(0); }

.message-box { margin-top: 15px; padding: 12px 15px; border-radius: 8px; font-size: 14px; font-weight: 600; text-align: center; }
.success { background-color: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
.error { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter, .fade-leave-to { opacity: 0; }
.fade-in { animation: fadeIn 0.3s ease-in-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 768px) {
  .info-grid { grid-template-columns: 1fr; gap: 15px; }
}
</style>