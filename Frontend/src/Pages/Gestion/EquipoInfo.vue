<template>
  <div class="info-container">
    
    <div class="header-actions">
      <h1 class="titulo">Información Completa del Equipo</h1>
    </div>

    <div v-if="equipo.activo === false" class="alerta-baja">
      <div class="alerta-icon">⛔</div>
      <div class="alerta-content">
        <h3>EQUIPO DADO DE BAJA</h3>
        <p><strong>Fecha de baja:</strong> {{ equipo.fecha_baja || 'No registrada' }}</p>
        <p><strong>Motivo:</strong> {{ equipo.motivo_baja || 'Sin motivo especificado' }}</p>
      </div>
    </div>

    <div class="top-bar">
      <button class="btn-volver" @click="$router.back()">⬅ Volver</button>
      <button class="btn-excel" @click="descargarExcel">📊 Descargar Excel</button>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(1)">
        Información Básica <span>{{ open[1] ? "▲" : "▼" }}</span>
      </h2>
      <div v-if="open[1]" class="section-body">
        <table class="info-table">
          <tbody>
            <tr><td><b>Nombre:</b></td><td>{{ equipo.nombre }}</td></tr>
            <tr><td><b>Código Inventario:</b></td><td>{{ equipo.codigo_inventario }}</td></tr>
            <tr><td><b>Sede:</b></td><td>{{ getNest(sede, 'nombre') }}</td></tr>
            <tr><td><b>Servicio:</b></td><td>{{ getNest(servicio, 'nombre') }}</td></tr>
            <tr><td><b>Ubicación:</b></td><td>{{ getNest(ubicacion, 'nombre') }}</td></tr>
            <tr><td><b>Marca:</b></td><td>{{ equipo.marca }}</td></tr>
            <tr><td><b>Modelo:</b></td><td>{{ equipo.modelo }}</td></tr>
            <tr><td><b>Serie:</b></td><td>{{ equipo.serie }}</td></tr>
            <tr><td><b>Responsable:</b></td><td>{{ equipo.responsable }}</td></tr>
            <tr><td><b>Registro Invima:</b></td><td>{{ equipo.registro_invima }}</td></tr>
            <tr><td><b>Estado:</b></td>
                <td>
                    <span :class="equipo.activo ? 'tag-activo' : 'tag-inactivo'">
                        {{ equipo.activo ? 'ACTIVO' : 'DE BAJA' }}
                    </span>
                </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(2)">
        Historial <span>{{ open[2] ? "▲" : "▼" }}</span>
      </h2>
      <div v-if="open[2]" class="section-body">
        <div v-if="historial">
          <table class="info-table">
            <tbody>
              <tr><td><b>ID Historial:</b></td><td>{{ historial.id_historial }}</td></tr>
              <tr><td><b>Fecha Adquisición:</b></td><td>{{ historial.fecha_adquisicion || 'NI' }}</td></tr>
              <tr><td><b>Fecha Fabricación:</b></td><td>{{ historial.fecha_fabricacion || 'NI' }}</td></tr>
              <tr><td><b>Fin Garantía:</b></td><td>{{ historial.fecha_caducidad_garantia || 'NI' }}</td></tr>
              <tr><td><b>Tiempo Vida (años):</b></td><td>{{ historial.tiempo_vida_anos }}</td></tr>
              <tr><td><b>Proveedor:</b></td><td>{{ historial.proveedor }}</td></tr>
              <tr><td><b>Propietario:</b></td><td>{{ historial.propietario }}</td></tr>
              <tr><td><b>Forma Adquisición:</b></td><td>{{ historial.forma_adquisicion }}</td></tr>
              <tr><td><b>Valor Compra:</b></td><td>{{ historial.valor_compra }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay historial registrado.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(3)">
        Documentos <span>{{ open[3] ? "▲" : "▼" }}</span>
      </h2>
      <div v-if="open[3]" class="section-body">
        <div v-if="documentos">
          <table class="info-table">
            <tbody>
              <tr><td><b>Hoja Vida:</b></td><td>{{ documentos.hoja_vida ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Registro Importación:</b></td><td>{{ documentos.registro_importacion ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Manual Operación:</b></td><td>{{ documentos.manual_operacion ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Manual Mantenimiento:</b></td><td>{{ documentos.manual_mantenimiento ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Guía Uso:</b></td><td>{{ documentos.guia_uso ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Instructivo Rápido:</b></td><td>{{ documentos.instructivo_rapido ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Observaciones:</b></td><td>{{ documentos.observaciones }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay documentos registrados.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(4)">
        Metrología Administrativa <span>{{ open[4] ? "▲" : "▼" }}</span>
      </h2>
      <div v-if="open[4]" class="section-body">
        <div v-if="metrologia_admin">
          <table class="info-table">
            <tbody>
              <tr><td><b>Mantenimiento:</b></td><td>{{ metrologia_admin.mantenimiento ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Frecuencia Mto:</b></td><td>{{ metrologia_admin.frecuencia_mantenimiento_anual }}</td></tr>
              <tr><td><b>Calibración:</b></td><td>{{ metrologia_admin.calibracion ? 'Sí' : 'No' }}</td></tr>
              <tr><td><b>Frecuencia Calib:</b></td><td>{{ metrologia_admin.frecuencia_calibracion_anual }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay metrología administrativa.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(5)">
        Metrología Técnica <span>{{ open[5] ? "▲" : "▼" }}</span>
      </h2>
      <div v-if="open[5]" class="section-body">
        <div v-if="metrologia_tecnica">
          <table class="info-table">
            <tbody>
              <tr><td><b>Magnitud:</b></td><td>{{ metrologia_tecnica.magnitud }}</td></tr>
              <tr><td><b>Rango Equipo:</b></td><td>{{ metrologia_tecnica.rango_equipo }}</td></tr>
              <tr><td><b>Resolución:</b></td><td>{{ metrologia_tecnica.resolucion }}</td></tr>
              <tr><td><b>Rango Trabajo:</b></td><td>{{ metrologia_tecnica.rango_trabajo }}</td></tr>
              <tr><td><b>Error Máximo:</b></td><td>{{ metrologia_tecnica.error_maximo_permitido }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay metrología técnica.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(6)">
        Condiciones del Equipo <span>{{ open[6] ? "▲" : "▼" }}</span>
      </h2>
      <div v-if="open[6]" class="section-body">
        <div v-if="condiciones">
          <table class="info-table">
            <tbody>
              <tr><td><b>Voltaje:</b></td><td>{{ condiciones.voltaje }}</td></tr>
              <tr><td><b>Corriente:</b></td><td>{{ condiciones.corriente }}</td></tr>
              <tr><td><b>Humedad Relativa:</b></td><td>{{ condiciones.humedad_relativa }}</td></tr>
              <tr><td><b>Temperatura:</b></td><td>{{ condiciones.temperatura }}</td></tr>
              <tr><td><b>Dimensiones:</b></td><td>{{ condiciones.dimensiones }}</td></tr>
              <tr><td><b>Peso:</b></td><td>{{ condiciones.peso }}</td></tr>
              <tr><td><b>Otros:</b></td><td>{{ condiciones.otros }}</td></tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay condiciones registradas.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header" @click="toggle(7)">
         Historial de Ubicaciones y Cambios
        <span>{{ open[7] ? "▲" : "▼" }}</span>
      </h2>
      
      <div v-if="open[7]" class="section-body table-responsive">
        <div v-if="registros_ubicacion && registros_ubicacion.length > 0">
          <table class="audit-table">
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Origen</th>
                    <th>Destino</th>
                    <th>Motivo</th>
                    <th>Responsable</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="reg in registros_ubicacion" :key="reg.id_registro">
                    <td class="date-cell">{{ reg.fecha_modificacion }}</td>
                    <td>{{ reg.tipo_modificacion }}</td>
                    <td class="muted-text">{{ reg.origenUbi || '-' }}</td>
                    <td class="highlight-text">{{ reg.destinoUbi || '-' }}</td>
                    <td>{{ reg.motivoCambio || '-' }}</td>
                    <td>{{ reg.responsable || reg.usuario }}</td>
                </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-data">No hay historial de movimientos registrado.</p>
      </div>
    </div>
    </div>
</template>

<script>
export default {
  name: "EquipoInfo",
  props: ["codigo"],
  data() {
    return {
      // Agregamos el índice 7 al objeto 'open'
      open: { 1: true, 2: false, 3: false, 4: false, 5: false, 6: false, 7: false },
      
      equipo: {},
      sede: {},
      servicio: {},
      ubicacion: {},
      
      historial: null,
      documentos: null,
      condiciones: null,
      metrologia_admin: null,
      metrologia_tecnica: null,
      
      // NUEVO ARRAY PARA LA AUDITORÍA
      registros_ubicacion: [] 
    };
  },
  
  created() {
    this.cargarEquipo();
  },
  
  watch: {
    '$route.params.codigo_inventario': 'cargarEquipo'
  },

  methods: {
    getNest(obj, key) {
        return (obj && obj[key]) ? obj[key] : 'NI';
    },

    toggle(id) { 
        this.open[id] = !this.open[id]; 
    },

    descargarExcel() {
        const codigo = this.equipo.codigo_inventario;
        if (!codigo) return;
        const encodedCodigo = encodeURIComponent(codigo);
        const downloadUrl = `http://localhost:8081/api/descargar/${encodedCodigo}/`;
        window.open(downloadUrl, '_blank');
    },

    async cargarEquipo() {
        const codigoParam = this.$route.params.codigo || this.codigo;

        if (!codigoParam) {
            console.warn("Código no detectado");
            return;
        }

        try {
            const encodedCode = encodeURIComponent(codigoParam);
            const response = await fetch(`http://localhost:8081/api/detailed/${encodedCode}/`);

            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }

            const data = await response.json();

            this.equipo = data.equipo || {};
            this.sede = data.sede || {};
            this.servicio = data.servicio || {};
            this.ubicacion = data.ubicacion || {};

            const getFirst = (arr) => (Array.isArray(arr) && arr.length > 0) ? arr[0] : null;

            this.historial = getFirst(data.historial);
            this.documentos = getFirst(data.documentos);
            this.condiciones = getFirst(data.condiciones);
            this.metrologia_admin = getFirst(data.metrologia_admin);
            this.metrologia_tecnica = getFirst(data.metrologia_tecnica);
            
            // ASIGNAR LA NUEVA LISTA DE AUDITORÍA
            this.registros_ubicacion = data.registros_ubicacion || [];

        } catch (error) {
            console.error("Error cargando equipo:", error);
        }
    }
  }
};
</script>

<style scoped>
.info-container {
  padding: 30px;
  max-width: 950px; /* Un poco más ancho para la nueva tabla */
  margin: 0 auto;
  font-family: 'Segoe UI', sans-serif;
}

/* ALERTA DE BAJA ESTILO */
.alerta-baja {
    background-color: #fee2e2;
    border: 2px solid #ef4444;
    color: #7f1d1d;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 25px;
    display: flex;
    align-items: flex-start;
    gap: 15px;
    box-shadow: 0 4px 10px rgba(239, 68, 68, 0.15);
}

.alerta-icon { font-size: 30px; }
.alerta-content h3 { margin-top: 0; margin-bottom: 10px; color: #b91c1c; font-weight: 800; }
.alerta-content p { margin: 5px 0; }

/* ETIQUETAS DE ESTADO */
.tag-activo { background: #d1fae5; color: #065f46; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em; border: 1px solid #a7f3d0; }
.tag-inactivo { background: #fee2e2; color: #991b1b; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em; border: 1px solid #fecaca; }

/* ESTILOS COMUNES */
.header-actions { display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }
.btn-volver { padding: 8px 14px; background: #e0e0e0; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
.btn-volver:hover { background: #d0d0d0; }
.titulo { font-size: 24px; font-weight: bold; color: #333; margin: 0; }

.section { margin-bottom: 15px; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.section-header { background: #f8f9fa; padding: 15px; margin: 0; cursor: pointer; font-size: 18px; font-weight: 600; color: #2c3e50; display: flex; justify-content: space-between; align-items: center; transition: background 0.2s; user-select: none; }
.section-header:hover { background: #eef1f6; }
.section-body { padding: 20px; background: #fff; border-top: 1px solid #eee; }

/* TABLA DE INFO VERTICAL (Nombre: Valor) */
.info-table { width: 100%; border-collapse: collapse; }
.info-table td { padding: 10px; border-bottom: 1px solid #f0f0f0; vertical-align: top; }
.info-table tr:last-child td { border-bottom: none; }
.info-table b { color: #555; display: inline-block; min-width: 150px; }

/* ESTILOS NUEVA TABLA DE AUDITORÍA (Horizontal) */
.table-responsive { overflow-x: auto; }
.audit-table { width: 100%; border-collapse: collapse; font-size: 13px; min-width: 700px; }
.audit-table th { background-color: #005C33; color: white; padding: 10px; text-align: left; }
.audit-table td { padding: 8px 10px; border-bottom: 1px solid #eee; color: #333; }
.audit-table tr:hover { background-color: #f9f9f9; }
.date-cell { font-weight: 600; color: #555; white-space: nowrap; }
.muted-text { color: #888; font-style: italic; }
.highlight-text { color: #005C33; font-weight: 600; }

.no-data { color: #777; font-style: normal; text-align: center; margin: 10px 0; }

.top-bar { width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.btn-excel { background-color: #008F4C; color: white; border: none; border-radius: 6px; padding: 10px 15px; font-size: 14px; font-weight: 600; cursor: pointer; transition: background-color 0.2s; display: flex; align-items: center; gap: 8px; }
.btn-excel:hover { background-color: #005C33; }
</style>