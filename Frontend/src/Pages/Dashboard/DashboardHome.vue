<template>
  <div class="page-container">

    <!-- TÍTULO + FILTROS A LA DERECHA -->
    <div class="header-row">
      <h1 class="page-title">Dashboard de Equipos</h1>

      <div class="filters-inline">

        <div class="filter-item">
          <label>Sede:</label>
          <select v-model="filtros.sede" @change="cargarDatos" class="pretty-select">
            <option value="">Todas</option>
            <option v-for="s in sedes" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>

        <div class="filter-item">
          <label>Servicio:</label>
          <select v-model="filtros.servicio" @change="cargarDatos" class="pretty-select">
            <option value="">Todos</option>
            <option v-for="a in servicios" :key="a" :value="a">{{ a }}</option>
          </select>
        </div>

      </div>
    </div>

    <!-- KPI CARDS -->
    <div class="kpi-grid">

      <!-- === EQUIPOS TOTALES === -->
      <div class="kpi-card">
        <div>
          <div class="kpi-title">Equipos Totales</div>
          <div class="kpi-value">{{ kpis.total_equipos }}</div>
        </div>
      </div>

      <!-- === ACTIVOS / INACTIVOS === -->
      <div class="kpi-card">
        <div>
          <div class="kpi-title">Activos</div>
          <div class="kpi-value" style="color:#16a34a">{{ kpis.activos }}</div>
        </div>
        <div>
          <div class="kpi-title">Inactivos</div>
          <div class="kpi-value" style="color:#dc2626">{{ kpis.inactivos }}</div>
        </div>
      </div>

      <!-- === CLASIFICACIÓN DE RIESGO === -->
      <div class="kpi-card">
        <div class="kpi-title-risk">Clasificación de Riesgo (INVIMA/NI)</div>
        <ul style="margin-top:10px;">
          <li v-for="r in riesgo" :key="r.clasificacion_riesgo">
            <strong>Clase {{ r.clasificacion_riesgo }}:</strong> {{ r.total }}
          </li>
        </ul>
      </div>

    </div>

    <div style="height:28px;"></div>

    <!-- GRÁFICOS + TARJETA LISTA EQUIPOS -->
    <div class="charts-grid">

      <!-- === GRÁFICO SEDE === -->
      <div class="white-card">
        <h3 class="chart-title">Equipos por Sede</h3>
        <canvas id="chartSedes"></canvas>
      </div>

      <!-- === GRÁFICO ACTIVOS === -->
      <div class="white-card">
        <h3 class="chart-title">Activos vs Inactivos</h3>
        <canvas id="chartActivos"></canvas>
      </div>

      <!-- === TARJETA EQUIPOS PENDIENTES === -->
      <div class="white-card" style="max-height:400px; overflow-y:auto;">
        <h3 class="chart-title">Equipos con Mantenimiento/Calibración Pendiente</h3>

        <div class="kpi-value" style="color:#b91c1c; font-size:28px;">
          {{ equiposPendientes.length }}
        </div>

        <ul class="list-items">
          <li v-for="eq in equiposPendientes" :key="eq.id" class="list-item">
            <strong>{{ eq.nombre }}</strong> <br />
            Código: {{ eq.codigo }}
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>


<script>
import { onMounted, reactive, ref } from "vue";
import Chart from "chart.js/auto";

export default {
  name: "DashboardHome",

  setup() {
    const kpis = reactive({
      total_equipos: "--",
      activos: "--",
      inactivos: "--",
      mantenimiento: "--",
      calibracion: "--",
    });

    const sedes = ref([]);
    const servicios = ref([]);

    const equiposPendientes = ref([]);   //////// NUEVO
    const riesgo = ref([]);              //////// NUEVO

    const filtros = reactive({
      sede: "",
      servicio: "",
    });

    let chartSedes = null;
    let chartActivos = null;

    // ===============================
    // 1. Cargar catálogos
    // ===============================
    const cargarCatalogos = async () => {
      try {
        const resp = await fetch("http://localhost:8081/api/estadisticas/catalogos/");
        const data = await resp.json();
        sedes.value = data.sedes || [];
        servicios.value = data.servicios || [];
      } catch (err) {
        console.error("Error cargando catálogos:", err);
      }
    };

    // ===============================
    // 2. Cargar estadísticas reales
    // ===============================
    const cargarDatos = async () => {
      try {
        let url = "http://localhost:8081/api/estadisticas/estadisticas/?";
        if (filtros.sede) url += `sede=${filtros.sede}&`;
        if (filtros.servicio) url += `servicio=${filtros.servicio}&`;

        const resp = await fetch(url);
        const data = await resp.json();

        const resumen = data.resumen_general || {};

        // === KPIs ===
        kpis.total_equipos = resumen.total_equipos ?? "--";
        kpis.activos = resumen.equipos_activos ?? "--";
        kpis.inactivos = resumen.equipos_inactivos ?? "--";
        kpis.mantenimiento = resumen.requieren_mantenimiento ?? "--";
        kpis.calibracion = resumen.requieren_calibracion ?? "--";

        // === NUEVO: Equipos con Mantenimiento/Calibración pendiente ===
        equiposPendientes.value = data.equipos_mant_calib || [];

        // === NUEVO: Clasificación de riesgo ===
        riesgo.value = data.clasificacion_riesgo || [];

        // === destruir gráficos anteriores ===
        if (chartSedes) chartSedes.destroy();
        if (chartActivos) chartActivos.destroy();

        // === Gráfico por sede ===
        const sedesData = data.por_sede || [];
        chartSedes = new Chart(document.getElementById("chartSedes"), {
          type: "bar",
          data: {
            labels: sedesData.map(s => s.sede_nombre),
            datasets: [{ label: "Equipos", data: sedesData.map(s => s.total) }],
          },
          options: { responsive: true, maintainAspectRatio: false },
        });

        // === Gráfico activos vs inactivos ===
        chartActivos = new Chart(document.getElementById("chartActivos"), {
          type: "pie",
          data: {
            labels: ["Activos", "Inactivos"],
            datasets: [{ data: [kpis.activos || 0, kpis.inactivos || 0] }],
          },
          options: { responsive: true, maintainAspectRatio: false },
        });

      } catch (error) {
        console.error("Error cargando datos del dashboard:", error);
      }
    };

    onMounted(() => {
      cargarCatalogos();
      cargarDatos();
    });

    return { kpis, filtros, sedes, servicios, cargarDatos, equiposPendientes, riesgo };
  },
};
</script>



<style scoped>

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

/* FILTROS EN LÍNEA */
.filters-inline {
  display: flex;
  gap: 20px;
  align-items: center;
}

/* Labels */
.filter-item label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

/* ================================
   SELECT BONITO / MODERNO
================================ */
.pretty-select {
  padding: 8px 14px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  transition: all 0.2s ease;
  min-width: 160px;
  cursor: pointer;
}

.pretty-select:hover {
  border-color: #3b82f6;
  box-shadow: 0 0 4px rgba(59, 130, 246, 0.4);
}

.pretty-select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 6px rgba(37, 99, 235, 0.5);
}

/* Título principal */
.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Mantener tus estilos existentes */
.page-container { max-width:1200px; margin: 0 auto; padding: 10px; }
.page-title { font-size:28px; margin-bottom:18px; color:#0f1724; }

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}

.kpi-card {
  background:#fff;
  padding:16px;
  border-radius:10px;
  box-shadow: 0 6px 18px rgba(13,38,70,0.04);
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.kpi-title { color:#6b7280; font-size:14px; }
.kpi-value { font-size:22px; font-weight:700; }
.kpi-title-risk {
    font-size: 14px;
    font-weight: 600;
    display: inline-block;  /* Hace que no ocupe 100% del ancho */
    margin-bottom: 6px;
    
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
}

.white-card {
  background:#fff;
  padding:24px;
  border-radius:10px;
  box-shadow: 0 6px 18px rgba(13,38,70,0.04);
  height: 350px;
  position: relative;
}

.white-card canvas {
  width: 100% !important;
  height: 100% !important;
}

.chart-title { margin-bottom: 10px; font-size: 18px; color: #0f1724; }

.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  font-size: 14px;
}

.filter-item select {
  padding: 6px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
}
</style>
