<template>
  <div class="contenedor">
    <h1 class="titulo">Detalle del Equipo</h1>

    <div class="table-wrapper">
      <table class="tabla-equipos">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Cód. Inventario</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Serie</th>
            <th>Cód. IPS</th>
            <th>Reg. INVIMA</th>
            <th>Clasif. Riesgo</th>
            <th class="col-acciones">Acciones</th>
          </tr>
        </thead>

        <tbody>
          <tr>
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
                  @click="verDetalleCompleto(equipo.codigo_inventario)"
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
</template>

<script>
export default {
  name: "EquipoDetalle",
  props: ["codigo"],

  data() {
    return {
      equipo: {},
      // Aunque solo mostramos datos de 'equipo', mantenemos las otras variables 
      // por si en el futuro necesitas validar algo, o puedes borrarlas si quieres limpiar más.
      area: {},
      sede: {},
      historial: {},
      documentos: {},
      condiciones: {},
      metrologia_admin: {},
      metrologia_tecnica: {}
    };
  },

  created() {
    this.cargarEquipo();
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
    verDetalleCompleto(codigo) {
        // 1. Codificamos el código de inventario. Esto convierte '/' en '%2F' y ' ' en '%20'.
        const codigoCodificado = encodeURIComponent(codigo);
        
        // 2. Navegamos usando el código codificado
        // Esto crea una URL segura, por ejemplo: /gestion/equipo/108942%20%2F%20008843/info
        this.$router.push(`/gestion/equipo/${codigoCodificado}/info`);
    },
    async cargarEquipo() {
      
      try {
        const response = await fetch(`http://127.0.0.1:8081/api/detailed/${this.codigo}/`);

        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }

        const data = await response.json();

        this.equipo = data.equipo || {};
        this.area = data.area || {};
        this.sede = data.sede || {};
        this.historial = Array.isArray(data.historial) ? (data.historial[0] || {}) : (data.historial || {});
        this.documentos = Array.isArray(data.documentos) ? (data.documentos[0] || {}) : (data.documentos || {});
        this.condiciones = Array.isArray(data.condiciones) ? (data.condiciones[0] || {}) : (data.condiciones || {});
        this.metrologia_admin = Array.isArray(data.metrologia_admin) ? (data.metrologia_admin[0] || {}) : (data.metrologia_admin || {});
        this.metrologia_tecnica = Array.isArray(data.metrologia_tecnica) ? (data.metrologia_tecnica[0] || {}) : (data.metrologia_tecnica || {});

      } catch (error) {
        console.error("Error en la API:", error);
      }
      
    }
  }
};
</script>

<style scoped>
.contenedor {
  padding: 20px;
  max-width: 100%;
  overflow-x: auto; /* Permite scroll si la tabla es muy ancha */
}

.titulo {
  margin-bottom: 20px;
  font-size: 26px;
  font-weight: 700;
  color: #333;
}

/* --- TABLA ESTILO UdeA / MINIMALISTA --- */
.table-wrapper {
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  overflow: hidden;
}

.tabla-equipos {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
  text-align: left;
}

.tabla-equipos th {
  background: #005C33; /* Encabezado Verde Oscuro UdeA */
  color: white;
  padding: 15px;
  font-weight: 600;
  white-space: nowrap; /* Evita que los títulos se rompan feo */
}

.tabla-equipos td {
  padding: 14px 15px;
  border-bottom: 1px solid #eef2f6;
  color: #4b5563;
  vertical-align: middle;
}

/* Zebra striping suave para facilitar lectura */
.tabla-equipos tbody tr:hover {
  background-color: #f9fafb;
}

/* Contenedor flex para alinear los botones */
.acciones-wrapper {
  display: flex;
  gap: 8px; /* Espacio entre botones */
  justify-content: center;
  flex-wrap: wrap; /* Si falta espacio, bajan */
}

/* Ajustamos la columna para dar espacio a los dos botones */
.col-acciones {
  width: 180px; /* Un poco más ancho para que quepan ambos */
  text-align: center;
}


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

/* Responsividad simple */
@media (max-width: 1024px) {
  .contenedor {
    padding: 10px;
  }
  .tabla-equipos th, .tabla-equipos td {
    padding: 10px;
    font-size: 14px;
  }
}
</style>