from django.db import models

# ============================
#       TABLAS AUXILIARES
# ============================

class Sede(models.Model):
    codigo_sede = models.CharField(primary_key=True, max_length=30)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'sede'

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    codigo_servicio = models.CharField(primary_key=True, max_length=30)
    sede = models.ForeignKey(
        Sede, to_field='codigo_sede',
        on_delete=models.PROTECT,
        db_column='sede_codigo'
    )
    nombre = models.CharField(max_length=200)

    class Meta:
        db_table = 'servicio'

    def __str__(self):
        return f"{self.nombre} ({self.sede.nombre})"


class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'ubicacion'

    def __str__(self):
        return self.nombre


# ============================
#         TABLA EQUIPO
# ============================

class Equipo(models.Model):
    codigo_inventario = models.CharField(primary_key=True, max_length=50)

    nombre = models.CharField(max_length=120)
    codigo_ips = models.CharField(max_length=50, blank=True, null=True)
    codigo_ecri = models.CharField(max_length=50, blank=True, null=True)
    responsable = models.CharField(max_length=150, blank=True, null=True)

    sede = models.ForeignKey(
        Sede, to_field='codigo_sede',
        on_delete=models.PROTECT,
        db_column='sede_codigo',
        blank=True, null=True
    )

    servicio = models.ForeignKey(
        Servicio, to_field='codigo_servicio',
        on_delete=models.PROTECT,
        db_column='servicio_codigo',
        blank=True, null=True
    )

    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        db_column='ubicacion_id',
        blank=True, null=True
    )

    marca = models.CharField(max_length=80, blank=True, null=True)
    modelo = models.CharField(max_length=120, blank=True, null=True)
    serie = models.CharField(max_length=100, blank=True, null=True)

    clasificacion_misional = models.CharField(max_length=80, blank=True, null=True)
    clasificacion_ips = models.CharField(max_length=50, blank=True, null=True)
    clasificacion_riesgo = models.CharField(max_length=50, blank=True, null=True)

    registro_invima = models.CharField(max_length=200, blank=True, null=True)

    # Campos que pediste conservar
    modificacionUbi = models.CharField(max_length=50, blank=True, null=True)
    modificacionactivo = models.CharField(max_length=50, blank=True, null=True)

    # Baja
    activo = models.BooleanField(default=True)
    fecha_baja = models.CharField(max_length=20, blank=True, null=True)  # FECHA COMO STRING
    motivo_baja = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'equipos'

    def __str__(self):
        return f"{self.codigo_inventario} - {self.nombre}"


# ============================
#      HISTORIAL (Excel)
# ============================

class Historial(models.Model):
    id_historial = models.CharField(primary_key=True, max_length=50)
    equipo = models.ForeignKey(
        Equipo, to_field='codigo_inventario',
        on_delete=models.PROTECT,
        db_column='equipo_codigo'
    )

    tiempo_vida_anos = models.CharField(max_length=90, blank=True, null=True)

    # Fechas AHORA son STRING
    fecha_adquisicion = models.CharField(max_length=120, blank=True, null=True)
    propietario = models.CharField(max_length=50, blank=True, null=True)
    fecha_fabricacion = models.CharField(max_length=120, blank=True, null=True)
    nit = models.CharField(max_length=50, blank=True, null=True)
    proveedor = models.CharField(max_length=50, blank=True, null=True)
    garantia = models.BooleanField(default=False)
    fecha_caducidad_garantia = models.CharField(max_length=120, blank=True, null=True)

    forma_adquisicion = models.CharField(max_length=80, blank=True, null=True)
    tipo_documento = models.CharField(max_length=100, blank=True, null=True)
    numero_documento = models.CharField(max_length=60, blank=True, null=True)

    # Agregado del Excel
    valor_compra = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'historial'

    def __str__(self):
        return f"Historial {self.id_historial} - {self.equipo.codigo_inventario}"


# ============================
#         DOCUMENTOS
# ============================

class Documento(models.Model):
    id_documento = models.CharField(primary_key=True, max_length=50)
    equipo = models.ForeignKey(
        Equipo, to_field='codigo_inventario',
        on_delete=models.PROTECT,
        db_column='equipo_codigo'
    )

    hoja_vida = models.BooleanField(default=False)
    registro_importacion = models.BooleanField(default=False)
    manual_operacion = models.BooleanField(default=False)
    manual_mantenimiento = models.BooleanField(default=False)
    guia_uso = models.BooleanField(default=False)
    instructivo_rapido = models.BooleanField(default=False)
    protocolo_mto_prev = models.BooleanField(default=False)

    frecuencia_metrologica_fabricante = models.CharField(max_length=80, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'documentos'


# ============================
#   METROLOGÍA ADMINISTRATIVA
# ============================

class MetrologiaAdministrativa(models.Model):
    id_metrologia_adm = models.CharField(primary_key=True, max_length=50)
    equipo = models.ForeignKey(
        Equipo, to_field='codigo_inventario',
        on_delete=models.PROTECT,
        db_column='equipo_codigo'
    )

    mantenimiento = models.BooleanField(default=False)
    frecuencia_mantenimiento_anual = models.CharField(max_length=50, blank=True, null=True)
    calibracion = models.BooleanField(default=False)
    frecuencia_calibracion_anual = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'metrologia_administrativa'


# ============================
#      METROLOGÍA TÉCNICA
# ============================

class MetrologiaTecnica(models.Model):
    id_metrologia_tecnica = models.CharField(primary_key=True, max_length=50)
    equipo = models.ForeignKey(
        Equipo, to_field='codigo_inventario',
        on_delete=models.PROTECT,
        db_column='equipo_codigo'
    )

    magnitud = models.CharField(max_length=200, blank=True, null=True)
    rango_equipo = models.CharField(max_length=255, blank=True, null=True)
    resolucion = models.CharField(max_length=200, blank=True, null=True)
    rango_trabajo = models.CharField(max_length=255, blank=True, null=True)
    error_maximo_permitido = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = 'metrologia_tecnica'


# ============================
#  CONDICIONES DE FUNCIONAMIENTO
# ============================

class CondicionesFuncionamiento(models.Model):
    id_condiciones = models.CharField(primary_key=True, max_length=50)
    equipo = models.ForeignKey(
        Equipo, to_field='codigo_inventario',
        on_delete=models.PROTECT,
        db_column='equipo_codigo'
    )

    voltaje = models.CharField(max_length=80, blank=True, null=True)
    corriente = models.CharField(max_length=80, blank=True, null=True)
    humedad_relativa = models.CharField(max_length=80, blank=True, null=True)
    temperatura = models.CharField(max_length=80, blank=True, null=True)
    dimensiones = models.CharField(max_length=120, blank=True, null=True)
    peso = models.CharField(max_length=50, blank=True, null=True)
    otros = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'condiciones_funcionamiento'


# ============================
#     REGISTRO DE ACTIVIDADES
# ============================

# ... (código anterior igual)

class RegistroActividades(models.Model):
    id_registro = models.AutoField(primary_key=True)
    equipo = models.ForeignKey(
        Equipo, to_field='codigo_inventario',
        on_delete=models.PROTECT,
        db_column='equipo_codigo'
    )
    usuario = models.CharField(max_length=140) # username del login
    tipo_modificacion = models.CharField(max_length=200)
    fecha_modificacion = models.CharField(max_length=20, blank=True, null=True) # string
    
    # --- NUEVAS COLUMNAS SOLICITADAS ---
    motivoCambio = models.CharField(max_length=355, blank=True, null=True)
    origenUbi = models.CharField(max_length=250, blank=True, null=True)
    destinoUbi = models.CharField(max_length=250, blank=True, null=True)
    responsable = models.CharField(max_length=150, blank=True, null=True)
    # -----------------------------------

    class Meta:
        db_table = 'registro_actividades'

    def __str__(self):
        return f"{self.equipo.codigo_inventario} - {self.tipo_modificacion}"