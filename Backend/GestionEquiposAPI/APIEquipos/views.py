from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from .models import Equipo, Sede, Historial, Documento, MetrologiaAdministrativa, MetrologiaTecnica, CondicionesFuncionamiento, Ubicacion, Servicio
from urllib.parse import unquote
from django.urls import path

@method_decorator(csrf_exempt, name='dispatch')
class EquipoViewDetailed(View):

    # ---------------------- GET ----------------------
    def get(self, request, codigo_inventario=None):

    # Si piden un equipo específico
        if codigo_inventario:
            codigo_inventario_decodificado = unquote(codigo_inventario)
            try:
                equipo_obj = Equipo.objects.get(codigo_inventario=codigo_inventario_decodificado)
            except Equipo.DoesNotExist:
                return JsonResponse({"Message": "Equipo no encontrado"}, status=404)

            # Equipo base
            equipo = {
                **equipo_obj.__dict__
            }
            equipo.pop("_state", None)

            # Relaciones simples
            sede = None
            if equipo_obj.sede:
                sede = {
                    "codigo_sede": equipo_obj.sede.codigo_sede,
                    "nombre": equipo_obj.sede.nombre,
                    "direccion": equipo_obj.sede.direccion,
                }

            servicio = None
            if equipo_obj.servicio:
                servicio = {
                    "codigo_servicio": equipo_obj.servicio.codigo_servicio,
                    "nombre": equipo_obj.servicio.nombre,
                    "sede": equipo_obj.servicio.sede.codigo_sede if equipo_obj.servicio.sede else None
                }

            # Relaciones múltiples (FK reversas)
            historial = list(Historial.objects.filter(equipo=equipo_obj).values())
            documentos = list(Documento.objects.filter(equipo=equipo_obj).values())
            condiciones = list(CondicionesFuncionamiento.objects.filter(equipo=equipo_obj).values())
            metrologia_admin = list(MetrologiaAdministrativa.objects.filter(equipo=equipo_obj).values())
            metrologia_tecnica = list(MetrologiaTecnica.objects.filter(equipo=equipo_obj).values())

            return JsonResponse({
                "Message": "Success",
                "equipo": equipo,
                "sede": sede,
                "servicio": servicio,
                "historial": historial,
                "documentos": documentos,
                "condiciones": condiciones,
                "metrologia_admin": metrologia_admin,
                "metrologia_tecnica": metrologia_tecnica
            }, safe=False)

        # Si no enviaron código → lista normal
        equipos = list(Equipo.objects.values())
        return JsonResponse({"Message": "Success", "equipos": equipos})



    # ---------------------- POST ----------------------
    def post(self, request):
        data = json.loads(request.body)

        # Buscar FK: sede
        sede_obj = None
        if data.get("sede"):
            try:
                sede_obj = Sede.objects.get(codigo_sede=data["sede"])
            except Sede.DoesNotExist:
                return JsonResponse({"Message": "Código de sede no válido"})

        # Buscar FK: area
        area_obj = None
        if data.get("area"):
            try:
                area_obj = Area.objects.get(codigo_area=data["area"])
            except Area.DoesNotExist:
                return JsonResponse({"Message": "Código de área no válido"})

        # Crear el equipo
        Equipo.objects.create(
            codigo_inventario=data["codigo_inventario"],
            #proceso=data.get("proceso"), #Se quita y ya
            nombre=data["nombre"],
            codigo_ips=data.get("codigo_ips"),
            codigo_ecri=data.get("codigo_ecri"),
            responsable=data.get("responsable"),
            sede=sede_obj,
            area=area_obj,
            ubicacion=data.get("ubicacion"),
            motivo_cambio_ubi=data.get("motivo_cambio_ubi"),
            marca=data.get("marca"),
            modelo=data.get("modelo"),
            serie=data.get("serie"),
            clasificacion_misional=data.get("clasificacion_misional"),
            clasificacion_ips=data.get("clasificacion_ips"),
            clasificacion_riesgo=data.get("clasificacion_riesgo"),
            registro_invima=data.get("registro_invima"),

            modificacionUbi=data.get("modificacionUbi"),
            modificacionactivo=data.get("modificacionactivo"),
            modificacionCodigo=data.get("modificacionCodigo"),

            activo=data.get("activo", True),
            fecha_baja=data.get("fecha_baja"),
            motivo_baja=data.get("motivo_baja"),
        )

        return JsonResponse({"Message": "Equipo creado exitosamente"})


    # ---------------------- PUT ----------------------
    def put(self, request, codigo_inventario):
       # en put(self, request, codigo_inventario):
        data = json.loads(request.body)
        try:
            equipo = Equipo.objects.get(codigo_inventario=codigo_inventario)
        except Equipo.DoesNotExist:
            return JsonResponse({"Message": "Equipo no encontrado"}, status=404)

        # update FK sede
        if data.get("sede"):
            try:
                equipo.sede = Sede.objects.get(codigo_sede=data["sede"])
            except Sede.DoesNotExist:
                return JsonResponse({"Message": "Código de sede no válido"}, status=400)

        # servicio
        if data.get("servicio"):
            try:
                equipo.servicio = Servicio.objects.get(codigo_servicio=data["servicio"])
            except Servicio.DoesNotExist:
                return JsonResponse({"Message": "Código de servicio no válido"}, status=400)

        # ubicacion
        if data.get("ubicacion"):
            try:
                equipo.ubicacion = Ubicacion.objects.get(id_ubicacion=int(data["ubicacion"]))
            except (ValueError, Ubicacion.DoesNotExist):
                try:
                    equipo.ubicacion = Ubicacion.objects.get(nombre__iexact=data["ubicacion"])
                except Ubicacion.DoesNotExist:
                    # opcional: crear nueva ubicacion?
                    equipo.ubicacion = None

        # actualizar otros campos
        for campo, valor in data.items():
            if hasattr(equipo, campo) and campo not in ("sede", "servicio", "ubicacion"):
                setattr(equipo, campo, valor)

        equipo.save()
        return JsonResponse({"Message": "Equipo actualizado correctamente"})


    # ---------------------- DELETE ----------------------
    def delete(self, request, codigo_inventario):
        count, _ = Equipo.objects.filter(codigo_inventario=codigo_inventario).delete()
        if count:
            return JsonResponse({"Message": "Equipo eliminado"})
        return JsonResponse({"Message": "Equipo no encontrado"})

@method_decorator(csrf_exempt, name='dispatch')
class EquipoView(View):

    def get(self, request, codigo_inventario=None):
        # 1. Búsqueda exacta por ID (URL)
        if codigo_inventario:
            equipo = list(Equipo.objects.filter(codigo_inventario=codigo_inventario).values())
            if equipo:
                return JsonResponse({"Message": "Success", "equipo": equipo[0]})
            else:
                return JsonResponse({"Message": "Equipo no encontrado"}, status=404)
        
        # INICIO DE CAMBIOS PARA FILTROS
        
        # Obtener queryset base (todos los equipos)
        queryset = Equipo.objects.all()

        # 2. Filtro de búsqueda general (?q=)
        query = request.GET.get('q', '').strip()
        if query:
            # Aplicar filtro general a nombre y código de inventario
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(codigo_inventario__icontains=query)
            )

        # 3. Filtros Específicos (AJUSTADO PARA MATCH CON EL FRONTEND)
        
        # Leemos los nombres de parámetros que envía el frontend:
        sede_nombre = request.GET.get('sede__nombre')
        servicio_nombre = request.GET.get('servicio__nombre')
        marca = request.GET.get('marca')
        modelo = request.GET.get('modelo')
        serie = request.GET.get('serie')
        codigo_ips = request.GET.get('codigo_ips')
        registro_invima = request.GET.get('registro_invima')
        # ubicacion = request.GET.get('ubicacion') # Comentado, ya que no lo envías en tu frontend

        # Aplicación de los filtros al queryset

        if sede_nombre:
            # Filtrar por el nombre de la sede (relación inversa __nombre)
            queryset = queryset.filter(sede__nombre=sede_nombre)
        
        if servicio_nombre:
            # Filtrar por el nombre del servicio/área (relación inversa __nombre)
            queryset = queryset.filter(servicio__nombre=servicio_nombre)
            
        # NUEVOS FILTROS AÑADIDOS
        if marca:
            # Filtrar por marca
            queryset = queryset.filter(marca=marca)
            
        if modelo:
            # Filtrar por modelo
            queryset = queryset.filter(modelo=modelo)
            
        if serie:
            # Filtrar por serie
            queryset = queryset.filter(serie=serie)
            
        if codigo_ips:
            # Filtrar por código IPS
            queryset = queryset.filter(codigo_ips=codigo_ips)

        # Convertir a lista de valores
        # Traemos solo lo necesario para la tabla de resultados
        equipos = list(queryset.values(
            'codigo_inventario', 
            'nombre', 
            'marca', 
            'modelo', 
            'sede__nombre', 
            'servicio__nombre',
            'serie',
            'codigo_ips',
            'registro_invima',
            'clasificacion_riesgo'
        ))

        if equipos:
            return JsonResponse({"Message": "Success", "equipos": equipos})
        else:
            return JsonResponse({"Message": "No se encontraron equipos con esos filtros", "equipos": []})
        
        # ---------------------- POST ----------------------
    def post(self, request):
        """
        Crea un Equipo + objetos relacionados opcionales.
        Reglas:
         - Campos string vacíos -> 'NI'
         - activo siempre True al crear
         - sede obligatorio (valida existencia)
         - servicio: si no existe, se crea (según requerimiento)
         - ubicacion: acepta id o nombre; si nombre no existe -> crear nueva
         - Campos de fecha se guardan como string (ISO) tal como vienen
         - Si vienen bloques de 'historial', 'documentos', 'metrologia_admin', 'metrologia_tecnica', 'condiciones' -> crear
        """
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"Message": "JSON inválido"}, status=400)

        # --- Validaciones básicas obligatorias ---
        required = ["sede", "nombre", "codigo_inventario", "ubicacion"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return JsonResponse({"Message": f"Faltan campos obligatorios: {', '.join(missing)}"}, status=400)

        # --- Sede (obligatoria) ---
        try:
            sede_obj = Sede.objects.get(codigo_sede=data["sede"])
        except Sede.DoesNotExist:
            return JsonResponse({"Message": "Codigo de sede no valido"}, status=400)

        # --- Servicio: si viene y no existe -> crear ---
        servicio_obj = None
        if data.get("servicio"):
            svc = data.get("servicio")
            # si envían código de servicio (código_servicio) intentamos por código, si no por nombre
            try:
                servicio_obj = Servicio.objects.get(codigo_servicio=svc)
            except Servicio.DoesNotExist:
                # intentar buscar por nombre
                try:
                    servicio_obj = Servicio.objects.get(nombre__iexact=svc, sede=sede_obj)
                except Servicio.DoesNotExist:
                    # crear nuevo servicio con código generado sencillo
                    codigo_gen = f"SVC-{sede_obj.codigo_sede}-{svc[:10].upper().replace(' ','')}"
                    servicio_obj = Servicio.objects.create(
                        codigo_servicio=codigo_gen,
                        sede=sede_obj,
                        nombre=svc
                    )

        # --- Ubicación: id o nombre; crear si nombre no existe ---
        ubicacion_obj = None
        if data.get("ubicacion"):
            try:
                ubicacion_obj = Ubicacion.objects.get(id_ubicacion=int(data["ubicacion"]))
            except (ValueError, TypeError, Ubicacion.DoesNotExist):
                # buscar por nombre
                try:
                    ubicacion_obj = Ubicacion.objects.get(nombre__iexact=data["ubicacion"])
                except Ubicacion.DoesNotExist:
                    # crear nueva ubicacion
                    ubicacion_obj = Ubicacion.objects.create(nombre=data["ubicacion"])

        # --- Multi-select eje misional (si viene lista) ---
        clas_misional = data.get("clasificacion_misional")
        if isinstance(clas_misional, list):
            clas_misional = "/".join([c for c in clas_misional if c])
        # si viene string lo dejamos tal cual

        # --- Helper: rellenar 'NI' por defecto para campos vacíos (strings) ---
        def ni_or(val):
            if val is None:
                return "NI"
            if isinstance(val, str) and val.strip() == "":
                return "NI"
            return val

        # Campos string del modelo (según tu modelo en el PDF)
        # (ajusta si tu modelo añade/quita campos)
        payload = {
            "codigo_inventario": data["codigo_inventario"],
            "nombre": data.get("nombre"),
            "codigo_ips": ni_or(data.get("codigo_ips")),
            "codigo_ecri": ni_or(data.get("codigo_ecri")),
            "responsable": ni_or(data.get("responsable")),
            "sede": sede_obj,
            "servicio": servicio_obj,
            "ubicacion": ubicacion_obj,
            "marca": ni_or(data.get("marca")),
            "modelo": data.get("modelo"),  # tu requisito: modelo no se puede cambiar (lo guardamos exacto)
            "serie": ni_or(data.get("serie")),
            "clasificacion_misional": ni_or(clas_misional),
            "clasificacion_ips": ni_or(data.get("clasificacion_ips")),
            "clasificacion_riesgo": ni_or(data.get("clasificacion_riesgo")),
            "registro_invima": ni_or(data.get("registro_invima")),
            "modificacionUbi": ni_or(data.get("modificacionUbi")),
            "modificacionactivo": ni_or(data.get("modificacionactivo")),
            "activo": True,  # FORZADO a True
            "fecha_baja": ni_or(data.get("fecha_baja")),
            "motivo_baja": ni_or(data.get("motivo_baja")),
        }

        # Insertar equipo (evitar sobre-escribir campos que no están en modelo)
        try:
            Equipo.objects.create(**payload)
        except Exception as e:
            return JsonResponse({"Message": "Error creando equipo", "detail": str(e)}, status=500)

        # --- Si viene 'historial' crear registro ---
        if data.get("historial"):
            h = data.get("historial")
            try:
                Historial.objects.create(
                    id_historial=h.get("id_historial") or f"H-{data['codigo_inventario']}",
                    equipo=Equipo.objects.get(codigo_inventario=data["codigo_inventario"]),
                    tiempo_vida_anos=ni_or(h.get("tiempo_vida_anos")),
                    fecha_adquisicion=str(h.get("fecha_adquisicion")) if h.get("fecha_adquisicion") else "NI",
                    propietario=ni_or(h.get("propietario")),
                    fecha_fabricacion=ni_or(h.get("fecha_fabricacion")),
                    nit=ni_or(h.get("nit")),
                    proveedor=ni_or(h.get("proveedor")),
                    garantia=bool(h.get("garantia")),
                    fecha_caducidad_garantia=ni_or(h.get("fecha_caducidad_garantia")),
                    forma_adquisicion=ni_or(h.get("forma_adquisicion")),
                    tipo_documento=ni_or(h.get("tipo_documento")),
                    numero_documento=ni_or(h.get("numero_documento")),
                    valor_compra=ni_or(h.get("valor_compra")),
                )
            except Exception:
                # no abortamos la creación del equipo por un error en historial
                pass

        # --- Documentos ---
        if data.get("documentos"):
            d = data.get("documentos")
            try:
                Documento.objects.create(
                    id_documento=d.get("id_documento") or f"D-{data['codigo_inventario']}",
                    equipo=Equipo.objects.get(codigo_inventario=data["codigo_inventario"]),
                    hoja_vida=bool(d.get("hoja_vida")),
                    registro_importacion=bool(d.get("registro_importacion")),
                    manual_operacion=bool(d.get("manual_operacion")),
                    manual_mantenimiento=bool(d.get("manual_mantenimiento")),
                    guia_uso=bool(d.get("guia_uso")),
                    instructivo_rapido=bool(d.get("instructivo_rapido")),
                    protocolo_mto_prev=bool(d.get("protocolo_mto_prev")),
                    frecuencia_metrologica_fabricante=ni_or(d.get("frecuencia_metrologica_fabricante")),
                    observaciones=ni_or(d.get("observaciones")),
                )
            except Exception:
                pass

        # --- Metrologia Administrativa ---
        if data.get("metrologia_admin"):
            m = data.get("metrologia_admin")
            try:
                MetrologiaAdministrativa.objects.create(
                    id_metrologia_adm=m.get("id_metrologia_adm") or f"MA-{data['codigo_inventario']}",
                    equipo=Equipo.objects.get(codigo_inventario=data["codigo_inventario"]),
                    mantenimiento=bool(m.get("mantenimiento")),
                    frecuencia_mantenimiento_anual=ni_or(m.get("frecuencia_mantenimiento_anual")),
                    calibracion=bool(m.get("calibracion")),
                    frecuencia_calibracion_anual=ni_or(m.get("frecuencia_calibracion_anual")),
                )
            except Exception:
                pass

        # --- Metrologia Tecnica ---
        if data.get("metrologia_tecnica"):
            t = data.get("metrologia_tecnica")
            try:
                MetrologiaTecnica.objects.create(
                    id_metrologia_tecnica=t.get("id_metrologia_tecnica") or f"MT-{data['codigo_inventario']}",
                    equipo=Equipo.objects.get(codigo_inventario=data["codigo_inventario"]),
                    magnitud=ni_or(t.get("magnitud")),
                    rango_equipo=ni_or(t.get("rango_equipo")),
                    resolucion=ni_or(t.get("resolucion")),
                    rango_trabajo=ni_or(t.get("rango_trabajo")),
                    error_maximo_permitido=ni_or(t.get("error_maximo_permitido")),
                )
            except Exception:
                pass

        # --- Condiciones de funcionamiento ---
        if data.get("condiciones"):
            c = data.get("condiciones")
            try:
                CondicionesFuncionamiento.objects.create(
                    id_condiciones=c.get("id_condiciones") or f"CF-{data['codigo_inventario']}",
                    equipo=Equipo.objects.get(codigo_inventario=data["codigo_inventario"]),
                    voltaje=ni_or(c.get("voltaje")),
                    corriente=ni_or(c.get("corriente")),
                    humedad_relativa=ni_or(c.get("humedad_relativa")),
                    temperatura=ni_or(c.get("temperatura")),
                    dimensiones=ni_or(c.get("dimensiones")),
                    peso=ni_or(c.get("peso")),
                    otros=ni_or(c.get("otros")),
                )
            except Exception:
                pass

        return JsonResponse({"Message": "Equipo creado exitosamente"})

    def put(self, request, codigo_inventario=None):
            """
            Actualiza un Equipo existente + objetos relacionados.
            """
            try:
                data = json.loads(request.body)
            except Exception:
                return JsonResponse({"Message": "JSON inválido"}, status=400)

            # 1. Validar que el equipo exista
            if not codigo_inventario:
                return JsonResponse({"Message": "Debe proporcionar el código de inventario en la URL"}, status=400)

            try:
                equipo = Equipo.objects.get(codigo_inventario=codigo_inventario)
            except Equipo.DoesNotExist:
                return JsonResponse({"Message": "Equipo no encontrado"}, status=404)

            # --- Helper: rellenar 'NI' por defecto ---
            def ni_or(val):
                if val is None:
                    return "NI"
                if isinstance(val, str) and val.strip() == "":
                    return "NI"
                return val

            # 2. Procesar Relaciones (Sede, Servicio, Ubicación)
            # --- Sede ---
            if data.get("sede"):
                try:
                    sede_obj = Sede.objects.get(codigo_sede=data["sede"])
                    equipo.sede = sede_obj
                except Sede.DoesNotExist:
                    return JsonResponse({"Message": "Codigo de sede no valido"}, status=400)

            # --- Servicio ---
            if data.get("servicio"):
                svc = data.get("servicio")
                try:
                    # Intenta buscar por código
                    servicio_obj = Servicio.objects.get(codigo_servicio=svc)
                except Servicio.DoesNotExist:
                    try:
                        # Intenta buscar por nombre
                        servicio_obj = Servicio.objects.get(nombre__iexact=svc, sede=equipo.sede)
                    except Servicio.DoesNotExist:
                        # Crear nuevo
                        codigo_gen = f"SVC-{equipo.sede.codigo_sede}-{svc[:10].upper().replace(' ','')}"
                        servicio_obj = Servicio.objects.create(
                            codigo_servicio=codigo_gen,
                            sede=equipo.sede,
                            nombre=svc
                        )
                equipo.servicio = servicio_obj

            # --- Ubicación ---
            if data.get("ubicacion"):
                try:
                    ubicacion_obj = Ubicacion.objects.get(id_ubicacion=int(data["ubicacion"]))
                except (ValueError, TypeError, Ubicacion.DoesNotExist):
                    try:
                        ubicacion_obj = Ubicacion.objects.get(nombre__iexact=data["ubicacion"])
                    except Ubicacion.DoesNotExist:
                        ubicacion_obj = Ubicacion.objects.create(nombre=data["ubicacion"])
                equipo.ubicacion = ubicacion_obj

            # 3. Actualizar campos directos del Equipo
            equipo.nombre = data.get("nombre", equipo.nombre)
            equipo.codigo_ips = ni_or(data.get("codigo_ips"))
            equipo.codigo_ecri = ni_or(data.get("codigo_ecri"))
            equipo.responsable = ni_or(data.get("responsable"))
            equipo.marca = ni_or(data.get("marca"))
            # El modelo NO se actualiza según tus reglas, pero si quisieras: 
            # equipo.modelo = data.get("modelo", equipo.modelo) 
            equipo.serie = ni_or(data.get("serie"))
            
            # Multi-select eje misional
            clas_misional = data.get("clasificacion_misional")
            if isinstance(clas_misional, list):
                equipo.clasificacion_misional = "/".join([c for c in clas_misional if c])
            elif clas_misional:
                equipo.clasificacion_misional = ni_or(clas_misional)

            equipo.clasificacion_ips = ni_or(data.get("clasificacion_ips"))
            equipo.clasificacion_riesgo = ni_or(data.get("clasificacion_riesgo"))
            equipo.registro_invima = ni_or(data.get("registro_invima"))
            
            # Campos de baja / activo
            equipo.activo = data.get("activo", True) # Por defecto True si no viene
            equipo.fecha_baja = ni_or(data.get("fecha_baja"))
            equipo.motivo_baja = ni_or(data.get("motivo_baja"))

            try:
                equipo.save()
            except Exception as e:
                return JsonResponse({"Message": "Error actualizando equipo", "detail": str(e)}, status=500)

            # 4. Actualizar o Crear Objetos Relacionados (Update or Create)
            
            # --- Historial ---
            if data.get("historial"):
                h = data.get("historial")
                defaults_h = {
                    "tiempo_vida_anos": ni_or(h.get("tiempo_vida_anos")),
                    "fecha_adquisicion": str(h.get("fecha_adquisicion")) if h.get("fecha_adquisicion") else "NI",
                    "propietario": ni_or(h.get("propietario")),
                    "fecha_fabricacion": ni_or(h.get("fecha_fabricacion")),
                    "nit": ni_or(h.get("nit")),
                    "proveedor": ni_or(h.get("proveedor")),
                    "garantia": bool(h.get("garantia")),
                    "fecha_caducidad_garantia": ni_or(h.get("fecha_caducidad_garantia")),
                    "forma_adquisicion": ni_or(h.get("forma_adquisicion")),
                    "tipo_documento": ni_or(h.get("tipo_documento")),
                    "numero_documento": ni_or(h.get("numero_documento")),
                    "valor_compra": ni_or(h.get("valor_compra")),
                    # Si no existe, usamos este ID para crear
                    "id_historial": h.get("id_historial") or f"H-{equipo.codigo_inventario}"
                }
                # Buscamos por equipo (relación OneToOne o ForeignKey inversa)
                Historial.objects.update_or_create(equipo=equipo, defaults=defaults_h)

            # --- Documentos ---
            if data.get("documentos"):
                d = data.get("documentos")
                defaults_d = {
                    "hoja_vida": bool(d.get("hoja_vida")),
                    "registro_importacion": bool(d.get("registro_importacion")),
                    "manual_operacion": bool(d.get("manual_operacion")),
                    "manual_mantenimiento": bool(d.get("manual_mantenimiento")),
                    "guia_uso": bool(d.get("guia_uso")),
                    "instructivo_rapido": bool(d.get("instructivo_rapido")),
                    "protocolo_mto_prev": bool(d.get("protocolo_mto_prev")),
                    "frecuencia_metrologica_fabricante": ni_or(d.get("frecuencia_metrologica_fabricante")),
                    "observaciones": ni_or(d.get("observaciones")),
                    "id_documento": d.get("id_documento") or f"D-{equipo.codigo_inventario}"
                }
                Documento.objects.update_or_create(equipo=equipo, defaults=defaults_d)

            # --- Metrologia Administrativa ---
            if data.get("metrologia_admin"):
                m = data.get("metrologia_admin")
                defaults_ma = {
                    "mantenimiento": bool(m.get("mantenimiento")),
                    "frecuencia_mantenimiento_anual": ni_or(m.get("frecuencia_mantenimiento_anual")),
                    "calibracion": bool(m.get("calibracion")),
                    "frecuencia_calibracion_anual": ni_or(m.get("frecuencia_calibracion_anual")),
                    "id_metrologia_adm": m.get("id_metrologia_adm") or f"MA-{equipo.codigo_inventario}"
                }
                MetrologiaAdministrativa.objects.update_or_create(equipo=equipo, defaults=defaults_ma)

            # --- Metrologia Tecnica ---
            if data.get("metrologia_tecnica"):
                t = data.get("metrologia_tecnica")
                defaults_mt = {
                    "magnitud": ni_or(t.get("magnitud")),
                    "rango_equipo": ni_or(t.get("rango_equipo")),
                    "resolucion": ni_or(t.get("resolucion")),
                    "rango_trabajo": ni_or(t.get("rango_trabajo")),
                    "error_maximo_permitido": ni_or(t.get("error_maximo_permitido")),
                    "id_metrologia_tecnica": t.get("id_metrologia_tecnica") or f"MT-{equipo.codigo_inventario}"
                }
                MetrologiaTecnica.objects.update_or_create(equipo=equipo, defaults=defaults_mt)

            # --- Condiciones de funcionamiento ---
            if data.get("condiciones"):
                c = data.get("condiciones")
                defaults_cf = {
                    "voltaje": ni_or(c.get("voltaje")),
                    "corriente": ni_or(c.get("corriente")),
                    "humedad_relativa": ni_or(c.get("humedad_relativa")),
                    "temperatura": ni_or(c.get("temperatura")),
                    "dimensiones": ni_or(c.get("dimensiones")),
                    "peso": ni_or(c.get("peso")),
                    "otros": ni_or(c.get("otros")),
                    "id_condiciones": c.get("id_condiciones") or f"CF-{equipo.codigo_inventario}"
                }
                CondicionesFuncionamiento.objects.update_or_create(equipo=equipo, defaults=defaults_cf)

            return JsonResponse({"Message": "Equipo actualizado exitosamente"})

    # ---------------------- AUTOCOMPLETE ----------------------
@csrf_exempt
def autocomplete_equipo(request):
    campo = request.GET.get("campo")
    q = request.GET.get("q", "").strip()

    # Campos que SÍ pertenecen a Equipo
    campos_equipo = ["marca", "modelo", "responsable"]

    # ============================
    #   EQUIPO (marca, modelo, responsable)
    # ============================
    if campo in campos_equipo:
        resultados = (
            Equipo.objects.filter(**{f"{campo}__icontains": q})
            .exclude(**{campo: None})
            .exclude(**{campo: ""})
            .values_list(campo, flat=True)
            .distinct()
        )
        return JsonResponse({"Message": "Success", "resultados": list(resultados)})

    # ============================
    #   HISTORIAL (proveedor, propietario)
    # ============================
    if campo in ["proveedor", "propietario"]:
        resultados = (
            Historial.objects.filter(**{f"{campo}__icontains": q})
            .exclude(**{campo: None})
            .exclude(**{campo: ""})
            .values_list(campo, flat=True)
            .distinct()
        )
        return JsonResponse({"Message": "Success", "resultados": list(resultados)})

    # ============================
    #   METROLOGÍA TÉCNICA (magnitud)
    # ============================
    if campo == "magnitud":
        resultados = (
            MetrologiaTecnica.objects.filter(magnitud__icontains=q)
            .exclude(magnitud=None)
            .exclude(magnitud="")
            .values_list("magnitud", flat=True)
            .distinct()
        )
        return JsonResponse({"Message": "Success", "resultados": list(resultados)})

    return JsonResponse({"Message": "Campo no permitido"}, status=400)


















@method_decorator(csrf_exempt, name='dispatch')
class SedeView(View):

    # ---------------------- GET ----------------------
    def get(self, request, codigo_sede=None):
        if codigo_sede:
            sede = list(Sede.objects.filter(codigo_sede=codigo_sede).values())
            if sede:
                return JsonResponse({"Message": "Success", "sede": sede[0]})
            else:
                return JsonResponse({"Message": "Sede no encontrada"})
        else:
            sedes = list(Sede.objects.values())
            if sedes:
                return JsonResponse({"Message": "Success", "sedes": sedes})
            else:
                return JsonResponse({"Message": "No hay sedes registradas"})

    # ---------------------- POST ----------------------
    def post(self, request):
        data = json.loads(request.body)

        # Crear la sede
        Sede.objects.create(
            codigo_sede=data["codigo_sede"],
            nombre=data["nombre"],
            direccion=data.get("direccion")  # puede ser null
        )

        return JsonResponse({"Message": "Sede creada exitosamente"})

    # ---------------------- PUT ----------------------
    def put(self, request, codigo_sede):
        data = json.loads(request.body)

        try:
            sede = Sede.objects.get(codigo_sede=codigo_sede)
        except Sede.DoesNotExist:
            return JsonResponse({"Message": "Sede no encontrada"})

        # Actualizar datos
        if "nombre" in data:
            sede.nombre = data["nombre"]
        if "direccion" in data:
            sede.direccion = data["direccion"]

        sede.save()
        return JsonResponse({"Message": "Sede actualizada correctamente"})

    # ---------------------- DELETE ----------------------
    def delete(self, request, codigo_sede):
        count, _ = Sede.objects.filter(codigo_sede=codigo_sede).delete()
        if count:
            return JsonResponse({"Message": "Sede eliminada correctamente"})
        return JsonResponse({"Message": "Sede no encontrada"})
    
@method_decorator(csrf_exempt, name='dispatch')
class HistorialView(View):

    # ---------------------- GET ----------------------
    def get(self, request, id_historial=None):

        if id_historial:
            historial = list(Historial.objects.filter(id_historial=id_historial).values())
            if historial:
                return JsonResponse({"Message": "Success", "historial": historial[0]})
            else:
                return JsonResponse({"Message": "Historial no encontrado"})
        
        else:
            historiales = list(Historial.objects.values())
            if historiales:
                return JsonResponse({"Message": "Success", "historiales": historiales})
            else:
                return JsonResponse({"Message": "No hay historiales registrados"})


    # ---------------------- POST ----------------------
    def post(self, request):
        data = json.loads(request.body)

        # FK equipo obligatorio
        try:
            equipo_obj = Equipo.objects.get(codigo_inventario=data["equipo"])
        except Equipo.DoesNotExist:
            return JsonResponse({"Message": "Código de equipo no válido"})

        Historial.objects.create(
            id_historial=data["id_historial"],
            equipo=equipo_obj,
            tiempo_vida_anos=data.get("tiempo_vida_anos"),
            fecha_adquisicion=data.get("fecha_adquisicion"),
            propietario=data.get("propietario"),
            fecha_fabricacion=data.get("fecha_fabricacion"),
            nit=data.get("nit"),
            proveedor=data.get("proveedor"),
            garantia=data.get("garantia", False),
            fecha_caducidad_garantia=data.get("fecha_caducidad_garantia"),
            forma_adquisicion=data.get("forma_adquisicion"),
            tipo_documento=data.get("tipo_documento"),
            numero_documento=data.get("numero_documento"),
        )

        return JsonResponse({"Message": "Historial creado exitosamente"})


    # ---------------------- PUT ----------------------
    def put(self, request, id_historial):
        data = json.loads(request.body)

        try:
            historial = Historial.objects.get(id_historial=id_historial)
        except Historial.DoesNotExist:
            return JsonResponse({"Message": "Historial no encontrado"})

        # ---- Validar FK equipo ----
        if "equipo" in data:
            try:
                historial.equipo = Equipo.objects.get(codigo_inventario=data["equipo"])
            except Equipo.DoesNotExist:
                return JsonResponse({"Message": "Código de equipo no válido"})

        # ---- Actualizar otros campos ----
        for campo, valor in data.items():
            if campo == "equipo":
                continue  # ya lo manejamos arriba

            if hasattr(historial, campo):
                setattr(historial, campo, valor)

        historial.save()
        return JsonResponse({"Message": "Historial actualizado correctamente"})


    # ---------------------- DELETE ----------------------
    def delete(self, request, id_historial):
        count, _ = Historial.objects.filter(id_historial=id_historial).delete()
        if count:
            return JsonResponse({"Message": "Historial eliminado"})
        return JsonResponse({"Message": "Historial no encontrado"})
    
@method_decorator(csrf_exempt, name='dispatch')
class DocumentoView(View):

    # ---------------------- GET ----------------------
    def get(self, request, id_documento=None):

        if id_documento:
            documento = list(Documento.objects.filter(id_documento=id_documento).values())
            if documento:
                return JsonResponse({"Message": "Success", "documento": documento[0]})
            else:
                return JsonResponse({"Message": "Documento no encontrado"})
        else:
            documentos = list(Documento.objects.values())
            if documentos:
                return JsonResponse({"Message": "Success", "documentos": documentos})
            else:
                return JsonResponse({"Message": "No hay documentos registrados"})


    # ---------------------- POST ----------------------
    def post(self, request):
        data = json.loads(request.body)

        # Validar FK de equipo
        try:
            equipo_obj = Equipo.objects.get(codigo_inventario=data["equipo"])
        except Equipo.DoesNotExist:
            return JsonResponse({"Message": "Código de equipo no válido"})

        # Crear documento
        Documento.objects.create(
            id_documento=data["id_documento"],
            equipo=equipo_obj,
            hoja_vida=data.get("hoja_vida", False),
            registro_importacion=data.get("registro_importacion", False),
            manual_operacion=data.get("manual_operacion", False),
            manual_mantenimiento=data.get("manual_mantenimiento", False),
            guia_uso=data.get("guia_uso", False),
            instructivo_rapido=data.get("instructivo_rapido", False),
            protocolo_mto_prev=data.get("protocolo_mto_prev", False),
            frecuencia_metrologica_fabricante=data.get("frecuencia_metrologica_fabricante"),
            observaciones=data.get("observaciones"),
        )

        return JsonResponse({"Message": "Documento creado exitosamente"})


    # ---------------------- PUT ----------------------
    def put(self, request, id_documento):
        data = json.loads(request.body)

        try:
            documento = Documento.objects.get(id_documento=id_documento)
        except Documento.DoesNotExist:
            return JsonResponse({"Message": "Documento no encontrado"})

        # Validar FK equipo
        if "equipo" in data:
            try:
                documento.equipo = Equipo.objects.get(codigo_inventario=data["equipo"])
            except Equipo.DoesNotExist:
                return JsonResponse({"Message": "Código de equipo no válido"})

        # Actualizar campos normales
        for campo, valor in data.items():
            if campo == "equipo":
                continue  # ya lo manejamos arriba

            if hasattr(documento, campo):
                setattr(documento, campo, valor)

        documento.save()
        return JsonResponse({"Message": "Documento actualizado correctamente"})


    # ---------------------- DELETE ----------------------
    def delete(self, request, id_documento):
        count, _ = Documento.objects.filter(id_documento=id_documento).delete()
        if count:
            return JsonResponse({"Message": "Documento eliminado"})
        return JsonResponse({"Message": "Documento no encontrado"})

@method_decorator(csrf_exempt, name='dispatch')  
class MetrologiaAdministrativaView(View):

    # ---------------------- GET ----------------------
    def get(self, request, id_metrologia_adm=None):
        if id_metrologia_adm:
            registro = list(MetrologiaAdministrativa.objects.filter(id_metrologia_adm=id_metrologia_adm).values())

            if registro:
                return JsonResponse({"Message": "Success", "metrologia_adm": registro[0]})
            else:
                return JsonResponse({"Message": "Registro no encontrado"})
        else:
            registros = list(MetrologiaAdministrativa.objects.values())
            if registros:
                return JsonResponse({"Message": "Success", "metrologia_adm": registros})
            else:
                return JsonResponse({"Message": "No hay registros"})

    # ---------------------- POST ----------------------
    def post(self, request):
        data = json.loads(request.body)

        # Validar FK: equipo
        try:
            equipo_obj = Equipo.objects.get(codigo_inventario=data["equipo"])
        except Equipo.DoesNotExist:
            return JsonResponse({"Message": "Equipo no válido"})

        MetrologiaAdministrativa.objects.create(
            id_metrologia_adm=data["id_metrologia_adm"],
            equipo=equipo_obj,
            mantenimiento=data.get("mantenimiento", False),
            frecuencia_mantenimiento_anual=data.get("frecuencia_mantenimiento_anual"),
            calibracion=data.get("calibracion", False),
            frecuencia_calibracion_anual=data.get("frecuencia_calibracion_anual")
        )

        return JsonResponse({"Message": "Metrología Administrativa creada exitosamente"})

    # ---------------------- PUT ----------------------
    def put(self, request, id_metrologia_adm):
        data = json.loads(request.body)

        try:
            registro = MetrologiaAdministrativa.objects.get(id_metrologia_adm=id_metrologia_adm)
        except MetrologiaAdministrativa.DoesNotExist:
            return JsonResponse({"Message": "Registro no encontrado"})

        # Validar FK: equipo
        if "equipo" in data:
            try:
                registro.equipo = Equipo.objects.get(codigo_inventario=data["equipo"])
            except Equipo.DoesNotExist:
                return JsonResponse({"Message": "Equipo no válido"})

        # Actualizar otros campos
        for campo in ["mantenimiento", "frecuencia_mantenimiento_anual",
                      "calibracion", "frecuencia_calibracion_anual"]:
            if campo in data:
                setattr(registro, campo, data[campo])

        registro.save()
        return JsonResponse({"Message": "Registro actualizado correctamente"})

    # ---------------------- DELETE ----------------------
    def delete(self, request, id_metrologia_adm):
        deleted, _ = MetrologiaAdministrativa.objects.filter(id_metrologia_adm=id_metrologia_adm).delete()
        if deleted:
            return JsonResponse({"Message": "Registro eliminado"})
        return JsonResponse({"Message": "Registro no encontrado"})
    
# views.py

@method_decorator(csrf_exempt, name='dispatch')
class MetrologiaTecnicaView(View):

    # ---------------------- GET ----------------------
    def get(self, request, id_metrologia_tecnica=None):
        if id_metrologia_tecnica:
            met = list(MetrologiaTecnica.objects.filter(
                id_metrologia_tecnica=id_metrologia_tecnica
            ).values())

            if met:
                return JsonResponse({"Message": "Success", "metrologia_tecnica": met[0]})
            else:
                return JsonResponse({"Message": "Metrología Técnica no encontrada"})
        else:
            met_list = list(MetrologiaTecnica.objects.values())
            if met_list:
                return JsonResponse({"Message": "Success", "metrologia_tecnica": met_list})
            else:
                return JsonResponse({"Message": "No hay registros de Metrología Técnica"})

    # ---------------------- POST ----------------------
    def post(self, request):
        data = json.loads(request.body)

        # validar FK equipo
        try:
            equipo_obj = Equipo.objects.get(codigo_inventario=data["equipo"])
        except Equipo.DoesNotExist:
            return JsonResponse({"Message": "Código de equipo no válido"})

        MetrologiaTecnica.objects.create(
            id_metrologia_tecnica=data["id_metrologia_tecnica"],
            equipo=equipo_obj,
            magnitud=data.get("magnitud"),
            rango_equipo=data.get("rango_equipo"),
            resolucion=data.get("resolucion"),
            rango_trabajo=data.get("rango_trabajo"),
            error_maximo_permitido=data.get("error_maximo_permitido"),
        )

        return JsonResponse({"Message": "Metrología Técnica creada exitosamente"})

    # ---------------------- PUT ----------------------
    def put(self, request, id_metrologia_tecnica):
        data = json.loads(request.body)

        try:
            met = MetrologiaTecnica.objects.get(id_metrologia_tecnica=id_metrologia_tecnica)
        except MetrologiaTecnica.DoesNotExist:
            return JsonResponse({"Message": "Metrología Técnica no encontrada"})

        # validar FK equipo si viene
        if data.get("equipo"):
            try:
                met.equipo = Equipo.objects.get(codigo_inventario=data["equipo"])
            except Equipo.DoesNotExist:
                return JsonResponse({"Message": "Código de equipo no válido"})

        # actualizar campos restantes
        campos_actualizables = [
            "magnitud", "rango_equipo", "resolucion",
            "rango_trabajo", "error_maximo_permitido"
        ]

        for campo in campos_actualizables:
            if campo in data:
                setattr(met, campo, data[campo])

        met.save()
        return JsonResponse({"Message": "Metrología Técnica actualizada correctamente"})

    # ---------------------- DELETE ----------------------
    def delete(self, request, id_metrologia_tecnica):
        count, _ = MetrologiaTecnica.objects.filter(
            id_metrologia_tecnica=id_metrologia_tecnica
        ).delete()

        if count:
            return JsonResponse({"Message": "Metrología Técnica eliminada"})
        return JsonResponse({"Message": "Metrología Técnica no encontrada"})
    
# views.py

@method_decorator(csrf_exempt, name='dispatch')
class CondicionesFuncionamientoView(View):

    # ---------------------- GET ----------------------
    def get(self, request, id_condiciones=None):
        if id_condiciones:
            cond = list(
                CondicionesFuncionamiento.objects.filter(id_condiciones=id_condiciones).values()
            )

            if cond:
                return JsonResponse({"Message": "Success", "condiciones": cond[0]})
            else:
                return JsonResponse({"Message": "Condición de funcionamiento no encontrada"})
        else:
            cond_list = list(CondicionesFuncionamiento.objects.values())

            if cond_list:
                return JsonResponse({"Message": "Success", "condiciones": cond_list})
            else:
                return JsonResponse({"Message": "No hay registros de condiciones de funcionamiento"})

    # ---------------------- POST ----------------------
    def post(self, request):
        data = json.loads(request.body)

        # validar FK equipo
        try:
            equipo_obj = Equipo.objects.get(codigo_inventario=data["equipo"])
        except Equipo.DoesNotExist:
            return JsonResponse({"Message": "Código de equipo no válido"})

        CondicionesFuncionamiento.objects.create(
            id_condiciones=data["id_condiciones"],
            equipo=equipo_obj,
            voltaje=data.get("voltaje"),
            corriente=data.get("corriente"),
            humedad_relativa=data.get("humedad_relativa"),
            temperatura=data.get("temperatura"),
            dimensiones=data.get("dimensiones"),
            peso=data.get("peso"),
            otros=data.get("otros"),
        )

        return JsonResponse({"Message": "Condiciones de funcionamiento creadas exitosamente"})

    # ---------------------- PUT ----------------------
    def put(self, request, id_condiciones):
        data = json.loads(request.body)

        try:
            cond = CondicionesFuncionamiento.objects.get(id_condiciones=id_condiciones)
        except CondicionesFuncionamiento.DoesNotExist:
            return JsonResponse({"Message": "Condición no encontrada"})

        # validar FK equipo si viene
        if data.get("equipo"):
            try:
                cond.equipo = Equipo.objects.get(codigo_inventario=data["equipo"])
            except Equipo.DoesNotExist:
                return JsonResponse({"Message": "Código de equipo no válido"})

        # campos a actualizar
        campos = [
            "voltaje", "corriente", "humedad_relativa", "temperatura",
            "dimensiones", "peso", "otros"
        ]

        for campo in campos:
            if campo in data:
                setattr(cond, campo, data[campo])

        cond.save()
        return JsonResponse({"Message": "Condición actualizada correctamente"})

    # ---------------------- DELETE ----------------------
    def delete(self, request, id_condiciones):
        count, _ = CondicionesFuncionamiento.objects.filter(
            id_condiciones=id_condiciones
        ).delete()

        if count:
            return JsonResponse({"Message": "Condición eliminada"})
        return JsonResponse({"Message": "Condición no encontrada"})


@method_decorator(csrf_exempt, name="dispatch")
class UbicacionView(View):

    def get(self, request):
        return JsonResponse({"Message": "Success", "ubicaciones": list(Ubicacion.objects.all().values())})

    def post(self, request):
        datos = json.loads(request.body)
        Ubicacion.objects.create(nombre=datos["nombre"])
        return JsonResponse({"Message": "Ubicación creada"})
    
@method_decorator(csrf_exempt, name="dispatch")
class RegistroActividadesView(View):

    def get(self, request):
        return JsonResponse({"Message": "Success", "actividades": list(RegistroActividades.objects.all().values())})

    def post(self, request):
        datos = json.loads(request.body)
        equipo = Equipo.objects.get(id=datos["equipo_id"])
        RegistroActividades.objects.create(
            equipo=equipo,
            descripcion=datos["descripcion"],
            fecha=datos.get("fecha", "")
        )
        return JsonResponse({"Message": "Actividad registrada"})

@method_decorator(csrf_exempt, name="dispatch")
class ServicioView(View):

    def get(self, request):
        return JsonResponse({"Message": "Success", "servicios": list(Servicio.objects.all().values())})

    def post(self, request):
        datos = json.loads(request.body)
        Servicio.objects.create(nombre=datos["nombre"])
        return JsonResponse({"Message": "Servicio creado"})

    def delete(self, request, id):
        try:
            Servicio.objects.get(id=id).delete()
        except:
            return JsonResponse({"Message": "No existe el servicio"})
        return JsonResponse({"Message": "Servicio eliminado"})