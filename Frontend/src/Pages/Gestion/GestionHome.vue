<!-- src/pages/Gestion/GestionHome.vue -->
<template>
  <div class="page-container">
    <h1 class="page-title">Sistema de Gestión</h1>

    <div class="cards-grid">
      <div class="big-card" @click="goToBuscar">
        <h2>🔍 Buscar Equipo</h2>
        <p class="muted">Filtrar por sede, área, ubicación o buscar por código.</p>
      </div>

      <div class="big-card" @click="goToNuevo">
        <h2>➕ Agregar Nuevo Equipo</h2>
        <p class="muted">Inicia el asistente paso a paso para registrar un equipo.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GestionHome",
  methods: {
    goToBuscar(){ this.$router.push('/gestion/buscar').catch(()=>{}); },
    goToNuevo(){ this.$router.push('/gestion/nuevo').catch(()=>{}); }
  }
}
</script>

<style scoped>
.page-container { max-width:1100px; margin: 0 auto; }
.page-title { font-size:28px; margin-bottom:18px; color:#0f1724; }
.cards-grid { display:grid; grid-template-columns: repeat(2, 1fr); gap:20px; }
.big-card {
  background: #fff;
  padding: 36px;
  border-radius:12px;
  box-shadow: 0 6px 18px rgba(13,38,70,0.06);
  cursor:pointer;
  transition: transform .12s ease, box-shadow .12s ease;
}
.big-card:hover { transform: translateY(-6px); box-shadow: 0 10px 30px rgba(13,38,70,0.09);}
.big-card h2 { margin:0 0 8px 0; font-size:20px; }
.muted { color:#6b7280; margin:0; }
</style>
