<template>
  <div class="page-wrap">
    <header class="page-header">
      <h1 class="title">Editar Equipo</h1>
      <p class="subtitle">Actualización de información — Universidad de Antioquia (LIME)</p>
    </header>

    <form @submit.prevent="onSubmit" class="form-grid">

      <section class="card">
        <div class="card-head">
          <div>
            <h2>Información básica</h2>
            <p class="card-sub">Datos principales del equipo</p>
          </div>
          <button type="button" class="collapse-btn" @click="toggleSection('basic')">
            {{ open.basic ? "▲" : "▼" }}
          </button>
        </div>

        <div v-show="open.basic" class="card-body">
          <div class="cols-2">
            <div class="field">
              <label>Sede <span class="req">*</span></label>
              <select v-model="form.sede_id" required class="input">
                <option value="">Seleccione una sede</option>
                <option v-for="s in sedes" :key="s.codigo_sede" :value="s.codigo_sede">{{ s.nombre }}</option>
              </select>
            </div>

            <div class="field">
              <label>Servicio</label>
              <input
                v-model="form.servicio_id"
                @input="buscarServicios"
                @blur="serviceBlur"
                list="serviciosList"
                class="input"
                placeholder="Escriba o seleccione"
              />
              <datalist id="serviciosList">
                <option v-for="s in serviciosSugeridos" :key="s.codigo_servicio" :value="s.nombre"></option>
              </datalist>
            </div>
          </div>

          <div class="cols-2">
            <div class="field">
              <label>Nombre del equipo <span class="req">*</span></label>
              <input v-model="form.nombre" required class="input" />
            </div>

            <div class="field">
              <label>Código inventario (No editable)</label>
              <input v-model="form.codigo_inventario" disabled class="input disabled-input" />
            </div>
          </div>

          <div class="cols-2">
            <div class="field">
              <label>Código IPS</label>
              <input v-model="form.codigo_ips" placeholder="Libre (ej: Pendiente)" class="input" />
            </div>

            <div class="field">
              <label>Código ECRI</label>
              <input v-model="form.codigo_ecri" class="input" />
            </div>
          </div>

          <div class="cols-2">
            <div class="field">
              <label>Responsable</label>
              <input
                v-model="responsableInput"
                @input="buscarResponsables"
                @blur="responsableBlur"
                list="responsablesList"
                class="input"
                placeholder="Escriba nombre o seleccione"
              />
              <datalist id="responsablesList">
                <option v-for="r in responsablesSugeridos" :key="r" :value="r"></option>
              </datalist>
            </div>

            <div class="field">
              <label>Ubicación física <span class="req">*</span></label>
              <input
                v-model="ubicacionInput"
                @input="buscarUbicaciones"
                @blur="ubicacionBlur"
                list="ubicacionesList"
                class="input"
                placeholder="Escriba o seleccione"
                required
              />
              <datalist id="ubicacionesList">
                <option v-for="u in ubicacionesSugeridas" :key="u.id_ubicacion" :value="u.nombre"></option>
              </datalist>
            </div>
          </div>

          <div class="cols-3 compacto">
            <div class="field">
              <label>Marca</label>
              <input
                v-model="marcaInput"
                @input="buscarMarcas"
                @blur="marcaBlur"
                list="marcasList"
                class="input"
                placeholder="Escriba o seleccione"
              />
              <datalist id="marcasList">
                <option v-for="m in marcasSugeridas" :key="m" :value="m"></option>
              </datalist>
            </div>

            <div class="field">
              <label>Modelo</label>
              <input
                v-model="modeloInput"
                @input="buscarModelos"
                @blur="modeloBlur"
                list="modelosList"
                class="input"
                placeholder="Escriba o seleccione"
              />
              <datalist id="modelosList">
                <option v-for="m in modelosSugeridos" :key="m" :value="m"></option>
              </datalist>
            </div>

            <div class="field">
              <label>Serie</label>
              <input v-model="form.serie" class="input" />
            </div>
          </div>

          <div class="cols-3 compacto">
            <div class="field">
              <label>Clasificación eje misional</label>
              <select v-model="form.clasificacion_misional" class="input">
                <option value="">Seleccione</option>
                <option v-for="opt in ejeMisionalOptions" :key="opt" :value="opt">{{ opt }}</option>
              </select>
            </div>

            <div class="field">
              <label>Clasificación IPS</label>
              <input v-model="form.clasificacion_ips" class="input" />
            </div>

            <div class="field">
              <label>Clasificación por riesgo</label>
              <select v-model="form.clasificacion_riesgo" class="input">
                <option v-for="r in riesgoOptions" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>
          </div>

          <div class="cols-2">
            <div class="field">
              <label>Registro INVIMA</label>
              <input v-model="form.registro_invima" placeholder="Escribe número o 'NI' si no aplica" class="input" />
            </div>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-head">
          <div>
            <h2>Historial / Adquisición</h2>
            <p class="card-sub">Información de compra y propietario</p>
          </div>
          <button type="button" class="collapse-btn" @click="toggleSection('historial')">
            {{ open.historial ? "▲" : "▼" }}
          </button>
        </div>

        <div v-show="open.historial" class="card-body">
          <div class="cols-3 compacto">
            <div class="field">
              <label>Tiempo vida (años)</label>
              <input v-model="form.historial.tiempo_vida_anos" class="input" />
            </div>

            <div class="field">
              <label>Fecha adquisición</label>
              <input type="date" v-model="form.historial.fecha_adquisicion" class="input" />
            </div>

            <div class="field">
              <label>Propietario</label>
              <input
                v-model="propietarioInput"
                @input="buscarPropietarios"
                @blur="propietarioBlur"
                list="propietariosList"
                class="input"
                placeholder="Escribe o selecciona"
              />
              <datalist id="propietariosList">
                <option v-for="p in propietariosSugeridos" :key="p" :value="p"></option>
              </datalist>
            </div>
          </div>

          <div class="cols-3 compacto">
            <div class="field">
              <label>Fecha fabricación</label>
              <input type="date" v-model="form.historial.fecha_fabricacion" class="input" />
            </div>

            <div class="field">
              <label>NIT</label>
              <input v-model="form.historial.nit" class="input" />
            </div>

            <div class="field">
              <label>Proveedor</label>
              <input
                v-model="proveedorInput"
                @input="buscarProveedores"
                @blur="proveedorBlur"
                list="proveedoresList"
                class="input"
                placeholder="Escriba o seleccione"
              />
              <datalist id="proveedoresList">
                <option v-for="p in proveedoresSugeridos" :key="p" :value="p"></option>
              </datalist>
            </div>
          </div>

          <div class="cols-3 compacto align-bottom">
            <div class="field garantia-field">
              <label>Garantía</label>
              <div class="checkbox-line">
                <input type="checkbox" v-model="form.historial.garantia" class="big-check" />
                <span> Aplica garantía</span>
              </div>
            </div>

            <div class="field">
              <label>Fecha fin garantía</label>
              <input type="date" v-model="form.historial.fecha_caducidad_garantia" :disabled="!form.historial.garantia" class="input" />
            </div>

            <div class="field">
              <label>Forma de adquisición</label>
              <input v-model="form.historial.forma_adquisicion" class="input" />
            </div>
          </div>

          <div class="cols-3 compacto">
            <div class="field">
              <label>Tipo de documento</label>
              <input v-model="form.historial.tipo_documento" class="input" />
            </div>
            <div class="field">
              <label>Número de documento</label>
              <input v-model="form.historial.numero_documento" class="input" />
            </div>
            <div class="field">
              <label>Valor de compra</label>
              <input v-model="form.historial.valor_compra" class="input" />
            </div>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-head">
          <div>
            <h2>Documentos / Metrología</h2>
            <p class="card-sub">Documentos disponibles y datos metrológicos</p>
          </div>
          <button type="button" class="collapse-btn" @click="toggleSection('documentos')">
            {{ open.documentos ? "▲" : "▼" }}
          </button>
        </div>

        <div v-show="open.documentos" class="card-body">
          <div class="row-inline doc-checkboxes">
            <label><input type="checkbox" v-model="form.documentos.hoja_vida" /> Hoja vida</label>
            <label><input type="checkbox" v-model="form.documentos.registro_importacion" /> Registro importación</label>
            <label><input type="checkbox" v-model="form.documentos.manual_operacion" /> Manual operación</label>
            <label><input type="checkbox" v-model="form.documentos.manual_mantenimiento" /> Manual mantenimiento</label>
          </div>

          <div class="cols-3 compacto">
            <div class="field">
              <label>Frecuencia metrológica (fabricante)</label>
              <input v-model="form.documentos.frecuencia_metrologica_fabricante" class="input" />
            </div>

            <div class="field">
              <label>Magnitud</label>
              <input
                v-model="magnitudInput"
                @input="buscarMagnitudes"
                @blur="magnitudBlur"
                list="magnitudesList"
                class="input"
                placeholder="Ej: Temperatura"
              />
              <datalist id="magnitudesList">
                <option v-for="m in magnitudesSugeridas" :key="m" :value="m"></option>
              </datalist>
            </div>

            <div class="field">
              <label>Rango del equipo</label>
              <input v-model="form.metrologia_tecnica.rango_equipo" class="input" />
            </div>
          </div>

          <div class="cols-3 compacto">
            <div class="field">
              <label>Resolución</label>
              <input v-model="form.metrologia_tecnica.resolucion" class="input" />
            </div>

            <div class="field">
              <label>Mantenimiento</label>
              <select v-model="form.metrologia_admin.mantenimiento">
                <option :value="true">Sí</option>
                <option :value="false">No</option>
              </select>
            </div>

            <div class="field">
              <label>Frecuencia anual mantenimiento</label>
              <input v-model="form.metrologia_admin.frecuencia_mantenimiento_anual" :disabled="!form.metrologia_admin.mantenimiento" class="input" />
            </div>
          </div>

          <div class="cols-3 compacto">
              <div class="field">
              <label>Calibración</label>
              <select v-model="form.metrologia_admin.calibracion">
                <option :value="true">Sí</option>
                <option :value="false">No</option>
              </select>
            </div>

            <div class="field">
              <label>Frecuencia anual calibración</label>
              <input v-model="form.metrologia_admin.frecuencia_calibracion_anual" :disabled="!form.metrologia_admin.calibracion" class="input" />
            </div>

            <div class="field">
              <label>Error máximo permitido</label>
              <input v-model="form.metrologia_tecnica.error_maximo_permitido" class="input" />
            </div>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-head">
          <div>
            <h2>Condiciones de funcionamiento</h2>
            <p class="card-sub">Ambiente y requisitos eléctricos</p>
          </div>
          <button type="button" class="collapse-btn" @click="toggleSection('condiciones')">
            {{ open.condiciones ? "▲" : "▼" }}
          </button>
        </div>

        <div v-show="open.condiciones" class="card-body">
          <div class="cols-3 compacto">
            <div class="field"><label>Voltaje</label><input v-model="form.condiciones.voltaje" class="input" /></div>
            <div class="field"><label>Corriente</label><input v-model="form.condiciones.corriente" class="input" /></div>
            <div class="field"><label>Humedad relativa</label><input v-model="form.condiciones.humedad_relativa" class="input" /></div>
          </div>

          <div class="cols-3 compacto">
            <div class="field"><label>Temperatura</label><input v-model="form.condiciones.temperatura" class="input" /></div>
            <div class="field"><label>Dimensiones</label><input v-model="form.condiciones.dimensiones" class="input" /></div>
            <div class="field"><label>Peso</label><input v-model="form.condiciones.peso" class="input" /></div>
          </div>
        </div>
      </section>

      <div class="actions">
        <button type="submit" class="btn-primary">Actualizar equipo</button>
        <button type="button" class="btn-secondary" @click="$router.back()">Cancelar</button>
      </div>
    </form>

    <div v-if="showConfirm" class="modal-overlay">
      <div class="modal-box">
        <h3 class="modal-title">Confirmar actualización</h3>
        <p>Se actualizará el equipo <strong>{{ form.codigo_inventario }}</strong> con la nueva información. ¿Deseas continuar?</p>
        <button class="modal-btn" @click="confirmSubmit">Sí, actualizar</button>
        <button class="modal-close" @click="showConfirm=false">Cancelar</button>
      </div>
    </div>

    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditarEquipo",
  data() {
    return {
      // listas / sugerencias
      sedes: [],
      serviciosSugeridos: [],
      ubicacionesSugeridas: [],
      marcasSugeridas: [],
      modelosSugeridos: [],
      responsablesSugeridos: [],
      proveedoresSugeridos: [],
      propietariosSugeridos: [],
      magnitudesSugeridas: [],

      // inputs de autocompletado libres
      servicioInput: "",
      ubicacionInput: "",
      marcaInput: "",
      modeloInput: "",
      responsableInput: "",
      proveedorInput: "",
      propietarioInput: "",
      magnitudInput: "",

      // UI
      message: "",
      showConfirm: false,
      // Abrimos más secciones por defecto en edición para ver la data
      open: { basic: true, historial: false, documentos: false, condiciones: false },

      ejeMisionalOptions: [
        "Extensión",
        "Investigación",
        "Docencia",
        "Administrativo"
      ],
      riesgoOptions: ["NI", "Clase I", "Clase IIa"],

      // formulario (Estructura base)
      form: {
        codigo_inventario: "",
        nombre: "",
        codigo_ips: "",
        codigo_ecri: "",
        responsable: "",
        sede: "",
        servicio: null,
        ubicacion: null,
        marca: "",
        modelo: "",
        serie: "",
        clasificacion_misional: "",
        clasificacion_ips: "",
        clasificacion_riesgo: "NI",
        registro_invima: "",
        modificacionUbi: "",
        modificacionactivo: "",
        activo: true,
        fecha_baja: "",
        motivo_baja: "",
        historial: {
          id_historial: "",
          tiempo_vida_anos: "",
          fecha_adquisicion: "",
          propietario: "",
          fecha_fabricacion: "",
          nit: "",
          proveedor: "",
          garantia: false,
          fecha_caducidad_garantia: "",
          forma_adquisicion: "",
          tipo_documento: "",
          numero_documento: "",
          valor_compra: ""
        },
        documentos: {
          hoja_vida: false,
          registro_importacion: false,
          manual_operacion: false,
          manual_mantenimiento: false,
          guia_uso: false,
          instructivo_rapido: false,
          protocolo_mto_prev: false,
          frecuencia_metrologica_fabricante: "",
          observaciones: ""
        },
        metrologia_admin: {
          mantenimiento: false,
          frecuencia_mantenimiento_anual: "",
          calibracion: false,
          frecuencia_calibracion_anual: ""
        },
        metrologia_tecnica: {
          magnitud: "",
          rango_equipo: "",
          resolucion: "",
          rango_trabajo: "",
          error_maximo_permitido: ""
        },
        condiciones: {
          voltaje: "",
          corriente: "",
          humedad_relativa: "",
          temperatura: "",
          dimensiones: "",
          peso: "",
          otros: ""
        }
      }
    };
  },
  
  // 1. Cargamos Sedes y DATOS DEL EQUIPO al montar
  created() {
    this.loadSedes();
    this.cargarDatosEquipo();
  },

  methods: {
    toggleSection(name) { this.open[name] = !this.open[name]; },

    async loadSedes() {
      try {
        const res = await axios.get("http://localhost:8081/api/sedes/");
        if (res.data.sedes) this.sedes = res.data.sedes;
      } catch (e) { console.error("Error sedes", e); }
    },

    formatDateForInput(dateString) {
    if (!dateString || dateString.toUpperCase() === 'NI') return '';

    // Caso 1: Viene con hora ("2008-12-02 00:00:00")
    if (dateString.includes(' ')) {
        return dateString.split(' ')[0]; // Retorna "2008-12-02"
    }

    // Caso 2: Viene solo el año ("2008")
    if (dateString.length === 4 && !isNaN(parseInt(dateString))) {
        // Retorna el primer día del año: "2008-01-01"
        return `${dateString}-01-01`; 
    }

    // Caso 3: Ya viene en formato YYYY-MM-DD
    return dateString;
},

    // 2. NUEVO MÉTODO: Cargar datos para editar
    async cargarDatosEquipo() {
        const codigo = this.$route.params.codigo_inventario; // Asegúrate que tu router use este nombre de param
        if (!codigo) return;

        try {
            const encodedCode = encodeURIComponent(codigo);
            const res = await axios.get(`http://localhost:8081/api/detailed/${encodedCode}/`);
            
            const data = res.data;
            
            // Asignamos datos principales
            // Usamos Object.assign para no perder la reactividad ni estructura base
            this.form = { ...this.form, ...data.equipo };

            // Asignamos datos anidados (La API devuelve array en algunos casos, verificamos)
            const checkData = (arr) => (Array.isArray(arr) && arr.length > 0) ? arr[0] : (arr || {});

            if(data.historial){
                let h = checkData(data.historial);

        // 🚨 APLICAR EL FORMATO AQUÍ 🚨
        h.fecha_adquisicion = this.formatDateForInput(h.fecha_adquisicion);
        h.fecha_fabricacion = this.formatDateForInput(h.fecha_fabricacion);
        h.fecha_caducidad_garantia = this.formatDateForInput(h.fecha_caducidad_garantia);
                
                this.form.historial = { ...this.form.historial, ...checkData(data.historial) };}
            if(data.documentos) this.form.documentos = { ...this.form.documentos, ...checkData(data.documentos) };
            if(data.metrologia_admin) this.form.metrologia_admin = { ...this.form.metrologia_admin, ...checkData(data.metrologia_admin) };
            if(data.metrologia_tecnica) this.form.metrologia_tecnica = { ...this.form.metrologia_tecnica, ...checkData(data.metrologia_tecnica) };
            if(data.condiciones) this.form.condiciones = { ...this.form.condiciones, ...checkData(data.condiciones) };
            if (data.equipo.sede_id) {
            this.form.sede = data.equipo.sede_id;
        }

        // Recomendación para Servicio y Ubicación, si son selectores:
        if (data.equipo.servicio_id) {
             this.form.servicio = data.equipo.servicio_id;
             // Si usa autocompletado para Servicio:
             this.servicioInput = data.equipo.servicio_id;
        }
        if (data.equipo.ubicacion_id) {
             this.form.ubicacion = data.equipo.ubicacion_id;
             // Si usa autocompletado para Ubicación:
             // Necesitaría el nombre de la ubicación aquí, que no viene directo.
             // Si solo viene el ID numérico (110), deberá hacer una búsqueda.
             // Pero si ubicacion_id es el nombre, úselo:
             this.ubicacionInput = data.equipo.ubicacion_id;
        }
            // 3. SINCRONIZAR INPUTS DE AUTOCOMPLETE
            // Rellenamos los inputs visuales con los datos cargados
            this.servicioInput = data.equipo.servicio__nombre || ""; // Asumiendo que el GET trae el nombre
            this.ubicacionInput = data.equipo.ubicacion__nombre || data.equipo.ubicacion || ""; // Ajustar según API
            this.marcaInput = this.form.marca || "";
            this.modeloInput = this.form.modelo || "";
            this.responsableInput = this.form.responsable || "";
            
            // Para historial
            if(this.form.historial) {
                this.proveedorInput = this.form.historial.proveedor || "";
                this.propietarioInput = this.form.historial.propietario || "";
            }
            if(this.form.metrologia_tecnica) {
                this.magnitudInput = this.form.metrologia_tecnica.magnitud || "";
            }

        } catch (error) {
            console.error("Error cargando equipo para editar:", error);
            this.message = "Error: No se pudo cargar la información del equipo.";
        }
    },

    // ------- BÚSQUEDAS / AUTOCOMPLETE (Igual que en Agregar) -------
    async buscarServicios() {
      if (!this.servicioInput) { this.serviciosSugeridos = []; return; }
      try {
        const res = await axios.get(`http://localhost:8081/api/servicio/?q=${encodeURIComponent(this.servicioInput)}`);
        if (res.data.servicios) this.serviciosSugeridos = res.data.servicios;
      } catch (e) { /* ignore */ }
    },
    serviceBlur() {
      if (!this.servicioInput) return;
      const match = this.serviciosSugeridos.find(s => s.nombre.toLowerCase() === this.servicioInput.toLowerCase());
      this.form.servicio = match ? match.codigo_servicio : this.servicioInput;
    },

    async buscarUbicaciones() {
      if (!this.ubicacionInput) { this.ubicacionesSugeridas = []; return; }
      try {
        const res = await axios.get(`http://localhost:8081/api/ubicacion/?q=${encodeURIComponent(this.ubicacionInput)}`);
        if (res.data.ubicaciones) this.ubicacionesSugeridas = res.data.ubicaciones;
      } catch (e) {}
    },
    ubicacionBlur() {
      if (!this.ubicacionInput) return;
      const match = this.ubicacionesSugeridas.find(u => u.nombre.toLowerCase() === this.ubicacionInput.toLowerCase());
      this.form.ubicacion = match ? match.id_ubicacion : this.ubicacionInput;
    },

    async buscarMarcas() {
      if (!this.marcaInput) { this.marcasSugeridas = []; return; }
      try {
        const res = await axios.get(
          `http://localhost:8081/api/autocomplete/equipo/?campo=marca&q=${encodeURIComponent(this.marcaInput)}`
        );
        if (res.data.resultados) this.marcasSugeridas = res.data.resultados;
      } catch (e) {}
    },
    marcaBlur() {
      this.form.marca = this.marcaInput || this.form.marca;
    },

    async buscarModelos() {
      if (!this.modeloInput) { this.modelosSugeridos = []; return; }
      try {
        const res = await axios.get(
          `http://localhost:8081/api/autocomplete/equipo/?campo=modelo&q=${encodeURIComponent(this.modeloInput)}`
        );
        if (res.data.resultados) this.modelosSugeridos = res.data.resultados;
      } catch (e) {}
    },
    modeloBlur() { this.form.modelo = this.modeloInput || this.form.modelo; },

    async buscarResponsables() {
      if (!this.responsableInput) { this.responsablesSugeridos = []; return; }
      try {
        const res = await axios.get(
          `http://localhost:8081/api/autocomplete/equipo/?campo=responsable&q=${encodeURIComponent(this.responsableInput)}`
        );
        if (res.data.resultados) this.responsablesSugeridos = res.data.resultados;
      } catch (e) {}
    },
    // Añadí el blur de responsable que faltaba en el original o es implicito
    responsableBlur() { this.form.responsable = this.responsableInput || this.form.responsable; },


    async buscarProveedores() {
      if (!this.proveedorInput) { this.proveedoresSugeridos = []; return; }
      try {
        const res = await axios.get(
          `http://localhost:8081/api/autocomplete/equipo/?campo=proveedor&q=${encodeURIComponent(this.proveedorInput)}`
        );
        if (res.data.resultados) this.proveedoresSugeridos = res.data.resultados;
      } catch (e) {}
    },
    proveedorBlur() { this.form.historial.proveedor = this.proveedorInput || this.form.historial.proveedor; },

    async buscarPropietarios() {
      if (!this.propietarioInput) { this.propietariosSugeridos = []; return; }
      try {
        const res = await axios.get(
          `http://localhost:8081/api/autocomplete/equipo/?campo=propietario&q=${encodeURIComponent(this.propietarioInput)}`
        );
        if (res.data.resultados) this.propietariosSugeridos = res.data.resultados;
      } catch (e) {}
    },
    propietarioBlur() { this.form.historial.propietario = this.propietarioInput || this.form.historial.propietario; },

    async buscarMagnitudes() {
      if (!this.magnitudInput) { this.magnitudesSugeridas = []; return; }
      try {
        const res = await axios.get(
          `http://localhost:8081/api/autocomplete/equipo/?campo=magnitud&q=${encodeURIComponent(this.magnitudInput)}`
        );
        if (res.data.resultados) this.magnitudesSugeridas = res.data.resultados;
      } catch (e) {}
    },
    magnitudBlur() { this.form.metrologia_tecnica.magnitud = this.magnitudInput || this.form.metrologia_tecnica.magnitud; },

    // ------- Preparar payload + validaciones -------
    setUbicacionFinal() {
      if (!this.ubicacionInput) return;
      const match = this.ubicacionesSugeridas.find(u => u.nombre.toLowerCase() === this.ubicacionInput.toLowerCase());
      this.form.ubicacion = match ? match.id_ubicacion : this.ubicacionInput;
    },

    preparePayload() {
      this.setUbicacionFinal();
      // validación obligatorios
// Campos que son obligatorios y deben estar en el objeto this.form
const requiredFields = ["codigo_inventario", "nombre", "sede", "ubicacion"]; 

// 1. Iteramos sobre los campos obligatorios.
const missing = requiredFields.filter(field => {
    const value = this.form[field];
    
    // **VERIFICACIÓN CLAVE:**
    // 1. (value || '') convierte null/undefined a "" (cadena vacía) para evitar errores.
    // 2. .toString() asegura que el valor es una cadena.
    // 3. .trim() elimina espacios en blanco al inicio y al final.
    // 4. Comparamos si la cadena resultante es estrictamente vacía.
    return (value || '').toString().trim() === '';
});

if (missing.length) {
    this.message = `Complete los campos obligatorios: ${missing.join(", ")}`;
    return null; // Detiene el flujo
}

// ... El resto de la lógica (ej. llamada a la API)

      const fillNI = (v) => {
        if (v === null || v === undefined) return "NI";
        if (typeof v === "string" && v.trim() === "") return "NI";
        return v;
      };

      const payload = JSON.parse(JSON.stringify(this.form));
      // aplicar NI recursivamente
      const applyNI = (obj) => {
        for (const k in obj) {
          if (typeof obj[k] === "object" && obj[k] !== null) applyNI(obj[k]);
          else if (typeof obj[k] === "string") obj[k] = fillNI(obj[k]);
        }
      };
      applyNI(payload);

      // forzar activo
      payload.activo = true;

      return payload;
    },

    onSubmit() {
      const payload = this.preparePayload();
      if (!payload) return;
      this.showConfirm = true;
    },

    async confirmSubmit() {
      this.showConfirm = false;
      const payload = this.preparePayload();
      if (!payload) return;
      
      try {
        // 4. CAMBIO A PUT PARA ACTUALIZAR
        const encodedCode = encodeURIComponent(this.form.codigo_inventario);
        const res = await axios.put(`http://localhost:8081/api/equipos/${encodedCode}/`, payload);
        
        if (res.data && res.data.Message) {
          this.message = "Equipo actualizado correctamente.";
          // Retraso ligero antes de volver
          setTimeout(() => {
              this.$router.push(`/gestion/equipo/${encodedCode}/`); 
          }, 1000);
        }
      } catch (err) {
        const msg = err.response && err.response.data && err.response.data.Message ? err.response.data.Message : "Error actualizando equipo";
        this.message = msg;
        console.error(err);
      }
    }
  }
};
</script>

<style scoped>
/* SE MANTIENE EL MISMO ESTILO EXACTO DEL ARCHIVO ORIGINAL */

/* ---------- Paleta LIME UdeA (clínico institucional) ---------- */
:root {
  --lime-800: #005C33;
  --lime-600: #0a7a4a;
  --bg: #f8fbfa;
  --card: #ffffff;
  --muted: #6b7280;
  --border: #e6eef0;
}

/* Page */
.page-wrap {
  max-width: 1180px;
  margin: 18px auto;
  padding: 20px;
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: #07221a;
  background: var(--bg);
  border-radius: 10px;
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}
.title {
  font-size: 22px;
  color: var(--lime-800);
  margin: 0;
  font-weight: 800;
}
.subtitle {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
}

/* Card */
.card {
  background: var(--card);
  border-radius: 12px;
  border: 1px solid var(--border);
  box-shadow: 0 8px 20px rgba(2,6,23,0.04);
  overflow: hidden;
}
.card-head {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:14px 18px;
  background: linear-gradient(180deg,#f8fdfb,#ffffff);
  border-bottom: 1px solid var(--border);
}
.card-head h2 {
  margin:0;
  color: var(--lime-800);
  font-size:15px;
}
.card-sub {
  margin:2px 0 0;
  font-size:12px;
  color:var(--muted);
}
.collapse-btn {
  background:transparent;
  border:none;
  color:var(--lime-600);
  font-weight:700;
  cursor:pointer;
}

/* Card body */
.card-body { padding:16px 18px; }

/* Grid utilities */
.form-grid { display:flex; flex-direction:column; gap:16px; }

/* Columns */
.cols-2 { display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:12px; }
.cols-3 { display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-bottom:12px; }
.cols-3.compacto { gap:10px; margin-bottom:10px; }

/* Compact adjustments (tight layout) */
.compacto .field { padding-bottom:2px; }
.compacto .field label { margin-bottom:6px; font-size:13px; }

/* Inline row */
.row-inline { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:12px; }
.doc-checkboxes label { margin-right:18px; font-size:14px; color:var(--muted); }

/* Field */
.field { display:flex; flex-direction:column; }
.field.align-center { justify-content:center; }
.field.align-bottom { align-items:flex-start; justify-content:center; }
label { font-weight:700; margin-bottom:6px; color:#0b2a22; font-size:13px; }
.req { color:#c53030; margin-left:6px; font-weight:700; }

/* Inputs */
.input {
  padding:10px 12px;
  border-radius:10px;
  border:1px solid var(--border);
  background:#fbfefc;
  outline:none;
  font-size:14px;
  height:42px;
  box-sizing:border-box;
  transition: box-shadow .12s, border-color .12s;
}
.input:focus {
  box-shadow: 0 10px 22px rgba(10,122,74,0.06);
  border-color: var(--lime-600);
}

/* Estilo para input deshabilitado (Código inv) */
.disabled-input {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
    font-weight: bold;
}

/* Checkbox styled switch (activo) */
.checkbox-wrap { display:flex; align-items:center; gap:10px; }
.switch { position: relative; display: inline-block; width:42px; height:24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #e6eef0;
  transition: .2s;
  border-radius: 999px;
  border: 1px solid #e9f3ee;
}
.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  top: 2px;
  background-color: white;
  transition: .2s;
  border-radius: 50%;
  box-shadow: 0 1px 4px rgba(2,6,23,0.08);
}
.switch input:checked + .slider {
  background-color: var(--lime-800);
  border-color: var(--lime-800);
}
.switch input:checked + .slider:before {
  transform: translateX(18px);
}

/* Buttons */
.actions { display:flex; gap:12px; justify-content:flex-end; margin-top:6px; }
.btn-primary {
  background: linear-gradient(180deg, #0BA360, #067C45);
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 800;
  box-shadow: 0 8px 18px rgba(6, 124, 69, 0.25);
  transition: 0.2s ease;
}
.btn-secondary {
  background: #EAFBF1;  /* Verde muy suave, clínico */
  color: #067C45;       /* Verde institucional */
  border: 1px solid #A8E6C8;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s ease;
}
/* Select con estilo institucional LIME */
select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-color: #fbfdfe;
  border: 1px solid #e6eef0;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #0f1724;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg width='14' height='14' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M5 7L10 12L15 7' stroke='%231E6F4A' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 14px;
}

select:focus {
  border-color: var(--lime-600);
  box-shadow: 0 6px 18px rgba(0, 92, 51, 0.10);
  outline: none;
}

select:disabled {
  background-color: #f3f4f6;
  color: #8a8a8a;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.45); display:flex; align-items:center; justify-content:center; z-index:999; }
.modal-box { background:#fff; padding:20px; border-radius:10px; width:420px; box-shadow:0 18px 48px rgba(2,6,23,0.18); text-align:center; }
.modal-title { margin-bottom:8px; font-size:17px; font-weight:800; color:var(--lime-800); }
.modal-btn { width:100%; padding:12px; margin-bottom:8px; background:var(--lime-800); border:none; color:white; border-radius:8px; cursor:pointer; font-size:15px; }

/* Messages */
.message { margin-top:16px; padding:12px; background:#f0f8f3; border-left:4px solid var(--lime-800); border-radius:8px; color:var(--lime-800); }

/* Muted */
.muted { color:var(--muted); font-size:12px; }

/* Responsive */
@media (max-width: 980px) {
  .cols-2, .cols-3 { grid-template-columns: 1fr; }
  .page-wrap { padding: 12px; }
}


/*botones de confirmacion*/
/* --- 1. FONDO Y CONTENEDOR PRINCIPAL DEL MODAL --- */
.modal-overlay {
  /* Fija la posición, cubre toda la pantalla */
  position: fixed; 
  inset: 0; 
  /* Fondo semi-transparente oscuro */
  background: rgba(0, 0, 0, 0.6); 
  /* Centra el modalbox */
  display: flex; 
  align-items: center; 
  justify-content: center; 
  /* Asegura que esté por encima de todo */
  z-index: 1000; 
}

/* --- 2. CAJA DEL MODAL --- */
.modal-box {
  background: #fff; /* Fondo blanco */
  padding: 30px;
  border-radius: 12px;
  width: 90%;
  max-width: 450px; /* Tamaño máximo razonable */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  /* Animación de entrada suave */
  animation: fadeInDown 0.3s ease-out; 
}

/* --- 3. TÍTULO Y TEXTO --- */
.modal-title {
  color: #005C33; /* Verde UdeA */
  font-size: 24px;
  margin-top: 0;
  margin-bottom: 15px;
  font-weight: 700;
}
.modal-box p {
  font-size: 16px;
  color: #333;
  margin-bottom: 25px;
}

/* --- 4. CONTENEDOR DE BOTONES (flex para alinearlos) --- */
.modal-box > .modal-btn,
.modal-box > .modal-close {
  /* Esto asegura que los botones se vean en la misma línea */
  display: inline-block;
  margin-right: 15px; /* Espacio entre botones */
}

/* --- 5. BOTÓN PRINCIPAL (Sí, actualizar) --- */
.modal-btn {
  background-color: #005C33; /* Verde principal */
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.modal-btn:hover {
  background-color: #008F4C; /* Verde más claro al pasar el mouse */
  transform: translateY(-1px);
}

/* --- 6. BOTÓN SECUNDARIO (Cancelar) --- */
.modal-close {
  background-color: #f8f9fa; /* Gris claro */
  color: #6c757d; /* Texto gris */
  border: 1px solid #ced4da;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-close:hover {
  background-color: #e9ecef;
  color: #495057;
}

/* --- 7. ANIMACIÓN (Opcional) --- */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>