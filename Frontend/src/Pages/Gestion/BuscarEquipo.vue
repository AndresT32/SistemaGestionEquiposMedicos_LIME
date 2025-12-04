<template>
  <div class="page-container">
    <h1 class="title">Buscar Equipo</h1>

    <div class="search-section">
      <div class="autocomplete-wrapper">
        <input
          v-model="terminoBusqueda"
          @input="buscarSugerencias"
          type="text"
          placeholder="Buscar por nombre o código..."
          class="search-input"
          autocomplete="off"
        />
        
        <ul v-if="sugerencias.length > 0" class="suggestions-list">
          <li 
            v-for="item in sugerencias" 
            :key="item.codigo_inventario"
            @click="seleccionarEquipo(item)"
            class="suggestion-item"
          >
            <span class="suggestion-name">{{ item.nombre }}</span>
            <span class="suggestion-code">{{ item.codigo_inventario }}</span>
          </li>
        </ul>
      </div>

      <button class="search-btn" @click="irAlEquipo()">
        Buscar
      </button>
    </div>

    <div class="filters-grid">
      
      <div class="filter-card">
        <label class="filter-title">Sede</label>
        <select v-model="selectedSede" class="filter-select">
          <option disabled value="">Seleccione una sede</option>
          <option v-for="s in sedes" :key="s.codigo_sede" :value="s.nombre">
            {{ s.nombre }}
          </option>
  
        </select>
      </div>

      <div class="filter-card">
        <label class="filter-title">Marca</label>
        <select v-model="selectedMarca" class="filter-select">
          <option disabled value="">Seleccione una marca</option>
          <option v-for="m in marcas" :key="m" :value="m">{{ m }}</option>

        </select>
      </div>

      <div class="filter-card">
        <label class="filter-title">Modelo</label>
        <select v-model="selectedModelo" class="filter-select">
          <option disabled value="">Seleccione un modelo</option>
          <option v-for="m in modelos" :key="m" :value="m">{{ m }}</option>

        </select>
      </div>

      <div class="filter-card">
        <label class="filter-title">Serie</label>
        <select v-model="selectedSerie" class="filter-select">
          <option disabled value="">Seleccione una serie</option>
          <option v-for="s in series" :key="s" :value="s">{{ s }}</option>
 
        </select>
      </div>

      <div class="filter-card">
        <label class="filter-title">Cód. IPS</label>
        <select v-model="selectedCodigoIps" class="filter-select">
          <option disabled value="">Seleccione un código IPS</option>
          <option v-for="c in ips_codigos" :key="c" :value="c">{{ c }}</option>

        </select>
      </div>

      <div class="filter-card">
        <label class="filter-title">Servicio</label>
        <select v-model="selectedServicio" class="filter-select">
          <option disabled value="">Seleccione un servicio</option>
          <option v-for="s in servicios" :key="s" :value="s">{{ s }}</option>
 
        </select>
      </div>

    </div>

    <div class="contenedor-filtros">
      <button class="btn-filtrar" @click="aplicarFiltros()">
        Filtrar Resultados
      </button>
    </div>

    <hr class="separador" />

    <div v-if="equipoSeleccionado" class="zona-detalle animate-slide-up" ref="zonaDetalle">
      <div class="detalle-header">
        <h3>Vista Rápida</h3>
        <button class="btn-cerrar-detalle" @click="cerrarDetalle">
          ✖ Cerrar Detalle
        </button>
      </div>
      
      <EquipoDetalle :codigo="equipoSeleccionado" />
    </div>

    <div v-else-if="resultados.length > 0" class="resultados-container">
      <h2 class="subtitulo">Resultados encontrados: {{ resultsCount }}</h2>
      
      <div class="table-wrapper">
        <table class="tabla-resultados">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Cód. Inventario</th>
              <th>Marca</th>
              <th>Modelo</th>
              <th>Serie</th>
              <th>Cod. IPS</th>
              <th>REG. INVIMA</th>
              <th>Clasif. Riesgo</th>
              <th class="col-acciones">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="equipo in resultados" :key="equipo.codigo_inventario">
                          <td>
              <strong>{{ equipo.nombre }}</strong>
            </td>

            <td>{{ equipo.codigo_inventario || 'Sin código' }}</td>

            <td>{{ equipo.marca || 'N/A' }}</td>

            <td>{{ equipo.modelo || 'N/A' }}</td>

            <td>{{ equipo.serie || 'N/A' }}</td>

            <td>{{ equipo.codigo_ips || 'N/A' }}</td>

            <td>{{ equipo.registro_invima || 'No disponible' }}</td>

            <td>
              <span class="badge-riesgo">{{ equipo.clasificacion_riesgo || 'N/A' }}</span>
            </td>
<td class="col-acciones">
            <div class="acciones-wrapper">
              <button
                  @click="verDetalle(equipo.codigo_inventario)"
                  class="btn-info-udea"
                  title="Ver detalles completos"
              >
                  Ver Todo
              </button>

                <button
                  @click="editarEquipo(equipo.codigo_inventario)"
                  class="btn-editar-udea"
                  title="Editar equipo"
                >
                  ✏️ Editar
                </button>
            </div>
          </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-else-if="busquedaRealizada" class="no-results">
        <p>⚠️ No se encontraron equipos con estos filtros.</p>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import EquipoDetalle from "./EquipoDetalle.vue"; 

export default {
  name: "BuscarEquipo",
  components: { EquipoDetalle },

  data() {
    return {
      // --- Variables de UI y Buscador ---
      terminoBusqueda: "",
      sugerencias: [],
      timeoutBusqueda: null,
      busquedaRealizada: false,
      resultados: [],

      // --- Variables para los Filtros (Seleccionados) ---
      selectedSede: "",
      selectedMarca: "",
      selectedModelo: "",
      selectedSerie: "",
      selectedCodigoIps: "", 
      selectedServicio: "",

      // --- Datos para llenar los Selects ---
      todosLosEquipos: [],
      sedes: [],
      marcas: [],
      modelos: [],
      series: [],
      ips_codigos: [],
      servicios: [],

      // --- Estado del Detalle Integrado ---
      equipoSeleccionado: null 
    };
  },

  computed: {
      resultsCount() { return this.resultados ? this.resultados.length : 0; }
  },

  // Carga inicial (Lógica traída de BuscarEquipo2)
  async created() {
    // 1. Cargar Sedes
    this.cargarSedes();

    // 2. Cargar Datos Base para poblar filtros
    const datosCargados = await this.cargarDatosBase(); 
    if (datosCargados) {
        this.cargarMarcas();
        this.cargarModelos();
        this.cargarSerie();
        this.cargarCodigosIps();
        this.cargarServicios();
    }
  },

  methods: {

    editarEquipo(codigo) {
        // Usamos $router.push para navegar a la ruta de edición
        // El nombre de la ruta debe coincidir con el que definas en tu router
        this.$router.push({ 
            name: 'EditarEquipo', // 👈 Usa el nombre de la ruta que definiste
            params: { codigo_inventario: codigo }
        });
    },
    // --- MÉTODOS DE CARGA DE DATOS (De BuscarEquipo2) ---
    async cargarSedes() {
      try {
        const res = await axios.get("http://localhost:8081/api/sedes/");
        if (res.data.sedes) this.sedes = res.data.sedes;
      } catch (error) { console.error("Error sedes:", error); }
    },

    async cargarDatosBase() {
        try {
            const res = await axios.get("http://localhost:8081/api/equipos/");
            this.todosLosEquipos = res.data.equipos || [];
            return true; 
        } catch (error) {
            console.error("Error cargando base:", error);
            return false; 
        }
    },

    getUnicosDesdeEquipos(propiedad, targetList) {
        const equipos = this.todosLosEquipos;
        if (!equipos.length) return;

        const valoresUnicos = [...new Set(
            equipos.map(equipo => equipo[propiedad]).filter(valor => valor) 
        )].sort();
        this[targetList] = valoresUnicos;
    },

    cargarMarcas() { this.getUnicosDesdeEquipos('marca', 'marcas'); },
    cargarModelos() { this.getUnicosDesdeEquipos('modelo', 'modelos'); },
    cargarSerie() { this.getUnicosDesdeEquipos('serie', 'series'); },
    cargarCodigosIps() { this.getUnicosDesdeEquipos('codigo_ips', 'ips_codigos'); },
    cargarServicios() { this.getUnicosDesdeEquipos('servicio__nombre', 'servicios'); },


    // --- MÉTODOS DE BÚSQUEDA Y FILTRADO ---
    
    buscarSugerencias() {
      clearTimeout(this.timeoutBusqueda);
      if (!this.terminoBusqueda || this.terminoBusqueda.length < 2) {
        this.sugerencias = [];
        return;
      }
      this.timeoutBusqueda = setTimeout(async () => {
        try {
          const q = encodeURIComponent(this.terminoBusqueda);
          const res = await axios.get(`http://localhost:8081/api/equipos/?q=${q}`);
          this.sugerencias = res.data.equipos || [];
        } catch (error) { console.error(error); }
      }, 300);
    },

    // CASO 1: Selección desde autocomplete (Abre Detalle directo)
    seleccionarEquipo(item) {
      this.terminoBusqueda = item.nombre;
      this.sugerencias = [];
      this.resultados = []; 
      
      this.equipoSeleccionado = item.codigo_inventario; // Activa componente
      
      this.$nextTick(() => {
        if(this.$refs.zonaDetalle) this.$refs.zonaDetalle.scrollIntoView({ behavior: 'smooth' });
      });
    },

    // CASO 2: Botón "Buscar" (Filtra tabla general)
async irAlEquipo() {
    if (!this.terminoBusqueda) {
        alert("Ingrese un término de búsqueda para buscar.");
        return;
    }
    
    // *** CAMBIOS CLAVE: LIMPIAR TODOS LOS FILTROS ESPECÍFICOS ***
    this.selectedSede = '';
    this.selectedMarca = '';
    this.selectedModelo = '';
    this.selectedSerie = '';
    this.selectedCodigoIps = '';
    this.selectedServicio = '';
    
    this.equipoSeleccionado = null; 
    this.busquedaRealizada = false;
    this.resultados = [];

    try {
        const params = new URLSearchParams();
        // Solo enviamos el término de búsqueda 'q'
        params.append('q', encodeURIComponent(this.terminoBusqueda));

        const res = await axios.get(`http://localhost:8081/api/equipos/?${params.toString()}`);

        if (res.data.equipos && res.data.equipos.length > 0) {
            this.resultados = res.data.equipos;
        } 
        this.busquedaRealizada = true;

    } catch (error) {
        console.error("Error buscando:", error);
        this.busquedaRealizada = true;
    }
},

    // CASO 3: Filtrar Resultados (API Compleja)
// En BuscarEquipo.vue -> methods: { ... }

async aplicarFiltros() {
    this.equipoSeleccionado = null;
    this.busquedaRealizada = false;
    this.resultados = [];

    // *** CAMBIO CLAVE DE UX ***
    this.terminoBusqueda = ''; 

    try {
        const params = new URLSearchParams();

        // 🚨 CORRECCIÓN: Quitamos encodeURIComponent()
        // URLSearchParams ya codifica automáticamente los valores.
        if (this.selectedSede) {
            params.append('sede_nombre', this.selectedSede);
        }
        if (this.selectedMarca) {
            params.append('marca', this.selectedMarca);
        }
        if (this.selectedModelo) {
            params.append('modelo', this.selectedModelo);
        }
        if (this.selectedSerie) {
            params.append('serie', this.selectedSerie);
        }
        if (this.selectedCodigoIps) {
            params.append('codigo_ips', this.selectedCodigoIps);
        }
        if (this.selectedServicio) {
            params.append('servicio_nombre', this.selectedServicio);
        }

        // Si no hay ningún filtro aplicado, evitamos la llamada a la API
        if (params.toString() === '') {
            this.busquedaRealizada = true;
            return; 
        }

        // params.toString() ahora codificará el valor UNA SOLA VEZ, 
        // lo que permitirá que la URL se vea correctamente en el backend:
        // /api/equipos/?marca=ADAM%20EQUIPMENT
        const res = await axios.get(`http://localhost:8081/api/equipos/?${params.toString()}`);

        if (res.data.equipos && res.data.equipos.length > 0) {
            this.resultados = res.data.equipos;
        } 
        this.busquedaRealizada = true;
    } catch (error) {
        console.error("Error filtrando:", error);
        this.busquedaRealizada = true;
    }
},

    // CASO 4: Botón "Ver Detalle" en la tabla (Abre componente)
    verDetalle(codigo) {
            // 1. Codificamos el código de inventario para asegurar una URL válida
            const codigoCodificado = encodeURIComponent(codigo);
            
            // 2. Navegamos a la ruta completa (esto abre una nueva "pestaña" o vista de router)
            this.$router.push(`/gestion/equipo/${codigoCodificado}/info`);

            // NOTA: Ya no necesitamos this.equipoSeleccionado = codigo ni el scroll,
            // porque estamos cambiando de página y no usando la vista integrada.
        },
    cerrarDetalle() {
      this.equipoSeleccionado = null; 
    }
  }
};
</script>

<style scoped>
.page-container { max-width: 1100px; margin: 0 auto; padding: 20px; }
.title { font-size: 28px; margin-bottom: 24px; color: #333; }

/* Búsqueda */
.search-section { display: flex; gap: 12px; margin-bottom: 28px; align-items: flex-start; }
.autocomplete-wrapper { position: relative; flex: 1; }
.search-input { width: 100%; padding: 14px; border-radius: 10px; border: 1px solid #e2e8f0; font-size: 16px; }
.search-input:focus { border-color: #008F4C; outline: none; }
.suggestions-list { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #e2e8f0; z-index: 50; }
.suggestion-item { padding: 12px 16px; cursor: pointer; display: flex; justify-content: space-between; border-bottom: 1px solid #f1f5f9; }
.suggestion-item:hover { background-color: #f4f7fe; }
.search-btn { padding: 14px 22px; background: #005C33; color: #fff; border: none; border-radius: 10px; cursor: pointer; height: 52px; font-weight: bold; }
.search-btn:hover { background: #008F4C; }

/* Grid de Filtros */
.filters-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.filter-card { background: #fff; padding: 18px; border-radius: 14px; box-shadow: 0 4px 14px rgba(0,0,0,0.06); }
.filter-title { font-weight: 600; margin-bottom: 8px; display: block; color: #374151; }
.filter-select { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; }

/* Botón Filtrar */
.contenedor-filtros { display: flex; justify-content: flex-end; margin-top: 15px; }
.btn-filtrar { background-color: #005C33; color: white; border: none; border-radius: 8px; padding: 12px 30px; font-weight: bold; cursor: pointer; transition: 0.2s; }
.btn-filtrar:hover { background-color: #008F4C; transform: translateY(-1px); }

/* Separador y Resultados */
.separador { margin: 30px 0; border: 0; border-top: 1px solid #e2e8f0; }
.resultados-container { margin-top: 20px; animation: fadeIn 0.5s ease; }
.subtitulo { font-size: 20px; font-weight: 600; color: #005C33; margin-bottom: 15px; }
.table-wrapper { background: white; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);overflow: hidden; overflow-x: auto; /* Permite desplazamiento horizontal si la tabla es más ancha */}
.tabla-resultados { width: 100%; border-collapse: collapse;table-layout: fixed;min-width: 800px;font-size: 15px; }
.tabla-resultados th { background: #005C33; color: white; padding: 12px; }
.tabla-resultados td { padding: 12px; border-bottom: 1px solid #eef2f6;;overflow: hidden;}
.btn-ver-udea { background-color: #008F4C; color: white; border: none; border-radius: 6px; padding: 6px 12px; cursor: pointer; font-weight: 600; }
.no-results { margin-top: 30px; text-align: center; color: #666; font-style: italic; }

/* Integración Detalle */
.zona-detalle { background-color: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); margin-top: 20px; }
.detalle-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #f1f5f9; }
.detalle-header h3 { margin: 0; color: #005C33; }
.btn-cerrar-detalle { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; transition: all 0.2s; }
.btn-cerrar-detalle:hover { background: #fee2e2; }

@media (max-width: 768px) {
  .filters-grid { grid-template-columns: 1fr; }
  .search-section { flex-direction: column; }
  .search-btn { width: 100%; }
}
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }




.btn-info-udea:hover {
  background-color: #008F4C;
}

/* --- ✨ Botón Editar (Amarillo) --- */
.btn-editar-udea {
  background-color: #FFC107; /* Amarillo intenso */
  color: #212529;            /* Texto oscuro para contraste */
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-editar-udea:hover {
  background-color: #FFB300; /* Amarillo más oscuro al pasar mouse */
  transform: translateY(-1px);
}

/* --- BADGE PARA RIESGO --- */
.badge-riesgo {
  background-color: #eef1ff;
  color: #005C33;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid #005C33;
}

/* --- BOTÓN DE ACCIÓN (Verde UdeA) --- */
.btn-info-udea {
  background-color: #005C33; /* Verde Principal */
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 4px rgba(0,92,51,0.2);
}


.btn-info-udea:active {
  transform: translateY(0);
}
</style>