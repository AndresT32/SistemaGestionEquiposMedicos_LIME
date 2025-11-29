from django.db.models import Count, F
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Equipo


def estadisticas_generales(request):

    sede = request.GET.get("sede")
    servicio = request.GET.get("servicio")

    equipos = Equipo.objects.all()

    # ===== APLICAR FILTROS =====
    if sede:
        equipos = equipos.filter(sede__nombre__iexact=sede.strip())

    if servicio:
        equipos = equipos.filter(servicio__nombre__iexact=servicio.strip())

    # ===== KPIs =====
    total_equipos = equipos.count()
    total_activos = equipos.filter(activo=True).count()
    total_inactivos = equipos.filter(activo=False).count()

    # ===== NUEVOS KPIs =====
    equipos_mantenimiento = equipos.filter(
        metrologiaadministrativa__mantenimiento=True
    ).count()

    equipos_calibracion = equipos.filter(
        metrologiaadministrativa__calibracion=True
    ).count()

    # ===== LISTA DE EQUIPOS QUE NECESITAN MANT / CALIB =====
    # CORREGIDO → tu modelo NO tiene id ni codigo
    lista_mant = equipos.filter(
        metrologiaadministrativa__mantenimiento=True
    ).values(
        "nombre",
        codigo=F("codigo_inventario")
    )

    lista_calib = equipos.filter(
        metrologiaadministrativa__calibracion=True
    ).values(
        "nombre",
        codigo=F("codigo_inventario")
    )


    # Unión sin duplicados
    lista_equipos_mant_calib = lista_mant.union(lista_calib)

    # ===== CLASIFICACIÓN DE RIESGO =====
    riesgo_counts = (
        equipos.values("clasificacion_riesgo")
        .annotate(total=Count("pk"))
        .order_by("clasificacion_riesgo")
    )

    # ===== TOP 5 MARCAS =====
    marcas_top = (
        equipos.values("marca")
        .annotate(total=Count("marca"))
        .order_by("-total")[:5]
    )

    # ===== EQUIPOS POR SEDE =====
    equipos_por_sede = (
        equipos.values(sede_nombre=F("sede__nombre"))
        .annotate(total=Count("pk"))
        .order_by("-total")
    )

    # ===== EQUIPOS POR SERVICIO =====
    equipos_por_servicio = (
        equipos.values(servicio_nombre=F("servicio__nombre"))
        .annotate(total=Count("pk"))
        .order_by("-total")
    )

    return JsonResponse({
        "resumen_general": {
            "total_equipos": total_equipos,
            "equipos_activos": total_activos,
            "equipos_inactivos": total_inactivos,

            # Nuevas métricas
            "requieren_mantenimiento": equipos_mantenimiento,
            "requieren_calibracion": equipos_calibracion,
        },

        # Nuevo: lista de equipos para mostrar nombre/código
        "equipos_mant_calib": list(lista_equipos_mant_calib),

        # Nuevo: clasificación INVIMA/NI
        "clasificacion_riesgo": list(riesgo_counts),

        "top_marcas": list(marcas_top),
        "por_sede": list(equipos_por_sede),
        "por_servicio": list(equipos_por_servicio),
    })


def catalogos_filtros(request):
    sedes = (
        Equipo.objects.values_list("sede__nombre", flat=True)
        .distinct()
        .order_by("sede__nombre")
    )

    servicios = (
        Equipo.objects.values_list("servicio__nombre", flat=True)
        .distinct()
        .order_by("servicio__nombre")
    )

    marcas = (
        Equipo.objects.values_list("marca", flat=True)
        .distinct()
        .order_by("marca")
    )

    return JsonResponse({
        "sedes": list(sedes),
        "servicios": list(servicios),
        "marcas": list(marcas),
    })
