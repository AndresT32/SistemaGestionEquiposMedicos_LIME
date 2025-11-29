<template>
  <div class="info-container">

    <div class="header-actions">

      <h1 class="titulo">Información Completa del Equipo</h1>
    </div>

<div class="top-bar">
  <button class="btn-volver" @click="$router.back()">⬅ Volver</button>

  <button class="btn-excel" @click="descargarExcel">
    📊 Descargar Excel
  </button>
</div>

    <div class="section">
      <h2 class="section-header" @click="toggle(1)">
        Información Básica
        <span>{{ open[1] ? "▲" : "▼" }}</span>
      </h2>

      <div v-if="open[1]" class="section-body">
        <table class="info-table">
          <tbody>
            <tr><td><b>Nombre:</b></td><td>{{ equipo.nombre }}</td></tr>
            <tr><td><b>Código Inventario:</b></td><td>{{ equipo.codigo_inventario }}</td></tr>
            <tr><td><b>Marca:</b></td><td>{{ equipo.marca }}</td></tr>
            <tr><td><b>Modelo:</b></td><td>{{ equipo.modelo }}</td></tr>
            <tr><td><b>Serie:</b></td><td>{{ equipo.serie }}</td></tr>
            <tr><td><b>Proceso:</b></td><td>{{ equipo.proceso }}</td></tr>
            <tr><td><b>Ubicación:</b></td><td>{{ equipo.ubicacion }}</td></tr>
            <tr><td><b>Responsable:</b></td><td>{{ equipo.responsable }}</td></tr>
            <tr><td><b>Registro Invima:</b></td><td>{{ equipo.registro_invima }}</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(2)">
        Historial
        <span>{{ open[2] ? "▲" : "▼" }}</span>
      </h2>

      <div v-if="open[2]" class="section-body">
        <div v-if="historial">
          <table class="info-table">
            <tbody>
              <tr><td><b>ID Historial:</b></td><td>{{ historial.id_historial }}</td></tr>
              <tr><td><b>Fecha Adquisición:</b></td><td>{{ historial.fecha_adquisicion }}</td></tr>
              <tr><td><b>Tiempo Vida:</b></td><td>{{ historial.tiempo_vida_anos }}</td></tr>
              <tr><td><b>Proveedor:</b></td><td>{{ historial.proveedor }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay historial registrado.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(3)">
        Documentos
        <span>{{ open[3] ? "▲" : "▼" }}</span>
      </h2>

      <div v-if="open[3]" class="section-body">
        <div v-if="documentos">
          <table class="info-table">
            <tbody>
              <tr><td><b>Hoja Vida:</b></td><td>{{ documentos.hoja_vida ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Manual Operación:</b></td><td>{{ documentos.manual_operacion ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Manual Mantenimiento:</b></td><td>{{ documentos.manual_mantenimiento ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Guía Uso:</b></td><td>{{ documentos.guia_uso ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Instructivo Rápido:</b></td><td>{{ documentos.instructivo_rapido ? 'Sí' : 'No' }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay documentos registrados.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(4)">
        Metrología Administrativa
        <span>{{ open[4] ? "▲" : "▼" }}</span>
      </h2>

      <div v-if="open[4]" class="section-body">
        <div v-if="metrologia_admin">
          <table class="info-table">
            <tbody>
              <tr><td><b>Mantenimiento:</b></td><td>{{ metrologia_admin.mantenimiento ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Frecuencia:</b></td><td>{{ metrologia_admin.frecuencia_mantenimiento_anual }}</td></tr>
              <tr><td><b>Calibración:</b></td><td>{{ metrologia_admin.calibracion ? 'Sí' : 'No' }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay metrología administrativa.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(5)">
        Metrología Técnica
        <span>{{ open[5] ? "▲" : "▼" }}</span>
      </h2>

      <div v-if="open[5]" class="section-body">
        <div v-if="metrologia_tecnica">
          <table class="info-table">
            <tbody>
              <tr><td><b>Magnitud:</b></td><td>{{ metrologia_tecnica.magnitud }}</td></tr>
              <tr><td><b>Rango:</b></td><td>{{ metrologia_tecnica.rango_equipo }}</td></tr>
              <tr><td><b>Resolución:</b></td><td>{{ metrologia_tecnica.resolucion }}</td></tr>
              <tr><td><b>Error Máximo:</b></td><td>{{ metrologia_tecnica.error_maximo_permitido }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay metrología técnica.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(6)">
        Condiciones del Equipo
        <span>{{ open[6] ? "▲" : "▼" }}</span>
      </h2>

      <div v-if="open[6]" class="section-body">
        <div v-if="condiciones">
          <table class="info-table">
            <tbody>
              <tr><td><b>Voltaje:</b></td><td>{{ condiciones.voltaje }}</td></tr>
              <tr><td><b>Corriente:</b></td><td>{{ condiciones.corriente }}</td></tr>
              <tr><td><b>Temperatura:</b></td><td>{{ condiciones.temperatura }}</td></tr>
              <tr><td><b>Dimensiones:</b></td><td>{{ condiciones.dimensiones }}</td></tr>
              <tr><td><b>Peso:</b></td><td>{{ condiciones.peso }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay condiciones registradas.</p>
      </div>
    </div>

  </div>
</template>

<script>
export default {
    name: "EquipoDetalle",
    // Aunque mantienes la prop 'codigo', NO la usamos para la API, sino el $route.params
    props: ["codigo"],

    data() {
        return {
            // Control de acordeones (1 abierto por defecto)
            open: {
                1: true,
                2: false,
                3: false,
                4: false,
                5: false,
                6: false
            },
            equipo: {},
            area: {},
            sede: {},
            // Inicializamos en NULL para que el v-else funcione correctamente
            historial: null,
            documentos: null,
            condiciones: null,
            metrologia_admin: null,
            metrologia_tecnica: null
        };
    },

    created() {
        this.cargarEquipo();
    },
    
    // ⚠️ NOTA: Añadimos un watcher para recargar si la ruta cambia (ej. navegando de un equipo a otro sin recargar la página)
    watch: {
        '$route.params.codigo_inventario': 'cargarEquipo'
    },

    methods: {



descargarExcel() {
    const codigo = this.equipo.codigo_inventario;
    
    // Si el código es '178684 / 061551/', se convierte en '178684%20%2F%20061551'
    const encodedCodigo = encodeURIComponent(codigo); 

    const downloadUrl = `http://localhost:8081/api/descargar/${encodedCodigo}/`;
    
    window.open(downloadUrl, '_blank');
},
        // Método para abrir/cerrar secciones
        toggle(id) {
            this.open[id] = !this.open[id];
        },

        async cargarEquipo() {
            // 1. OBTENER EL CÓDIGO DE LA RUTA
            
            const codigo = await fetch(`http://127.0.0.1:8081/api/detailed/${this.codigo}/`);

            // Validación (opcional, pero útil)
            if (!codigo) {
                console.warn("Código de inventario no disponible en la ruta.");
                // Limpiar datos para evitar mostrar información anterior
                this.equipo = {};
                return; 
            }

            try {
                // 2. 🟢 CORRECCIÓN CLAVE: Usamos la variable local 'codigo'
                // Esto asegura que la URL sea: /api/detailed/108942%20%2F%20008843/
                const response = await fetch(`http://127.0.0.1:8081/api/detailed/${this.codigo}/`);

                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }

                const data = await response.json();

                // ASIGNACIÓN DE DATOS
                this.equipo = data.equipo || {};
                this.area = data.area || {};
                this.sede = data.sede || {};

                // Helper para verificar si hay datos reales en el array
                const checkData = (arr) => (Array.isArray(arr) && arr.length > 0) ? arr[0] : null;

                this.historial = checkData(data.historial);
                this.documentos = checkData(data.documentos);
                this.condiciones = checkData(data.condiciones);
                this.metrologia_admin = checkData(data.metrologia_admin);
                this.metrologia_tecnica = checkData(data.metrologia_tecnica);

            } catch (error) {
                console.error("Error en la API:", error);
            }
        }
    }
};
</script>

<style scoped>
.info-container {
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
  font-family: 'Segoe UI', sans-serif;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.btn-volver {
  padding: 8px 14px;
  background: #e0e0e0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}
.btn-volver:hover {
  background: #d0d0d0;
}

.titulo {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.section {
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden; /* Para que las esquinas redondeadas funcionen bien */
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.section-header {
  background: #f8f9fa;
  padding: 15px;
  margin: 0;
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s;
  user-select: none;
}

.section-header:hover {
  background: #eef1f6;
}

.section-body {
  padding: 20px;
  background: #fff;
  border-top: 1px solid #eee;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
}

.info-table td {
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: top;
}

.info-table tr:last-child td {
  border-bottom: none;
}

.info-table b {
  color: #555;
  display: inline-block;
  min-width: 140px;
}

.no-data {
  color: #777;
  font-style: italic;
  text-align: center;
  margin: 10px 0;
}

.top-bar {
  width: 100%;
  display: flex;
  justify-content: space-between; /* Esto separa los botones a extremos */
  align-items: center;
  margin-bottom: 15px;
}

.btn-pdf {
  padding: 8px 14px;
  background: #e0e0e0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-pdf:hover {
  background: #d0d0d0;
}

/* Estilo para el botón de descarga XLSX */
.btn-excel {
  background-color: #008F4C; /* Verde UdeA o similar */
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 15px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-excel:hover {
  background-color: #005C33; 
}
</style>