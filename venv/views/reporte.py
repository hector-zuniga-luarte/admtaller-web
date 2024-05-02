
import fastapi
from fastapi_chameleon import template
from viewmodels.reporte.reporte_valorizacion_taller_viewmodel import ReporteValorizacionTaller
from viewmodels.reporte.reporte_presupuesto_estimado_asignatura_viewmodel import ReportePresupuestoEstimadoAsignatura
from viewmodels.reporte.reporte_asignacion_registro_docentes_viewmodel import ReporteAsignacionRegistroDocentes
from viewmodels.reporte.reporte_resumen_producto_rango_fechas_viewmodel import ReporteResumenProductoRangoFechas
from viewmodels.reporte.reporte_detalle_producto_taller_rango_fechas_viewmodel import ReporteDetalleProductoTallerRangoFechas
from starlette.requests import Request
from starlette.responses import Response
from datetime import date

from infrastructure.fileexport import generar_excel
from infrastructure.fileexport import generar_pdf

router = fastapi.APIRouter()


@router.get("/reporte/1")
@template(template_file="reporte/valorizacion_taller.pt")
async def reporte_valorizacion_taller(request: Request):
    vm = ReporteValorizacionTaller(request)
    await vm.load()

    return vm.to_dict()


@router.get("/reporte/2")
@template(template_file="reporte/presupuesto_estimado_asignatura.pt")
async def reporte_presupuesto_estimado_asignatura(request: Request):
    vm = ReportePresupuestoEstimadoAsignatura(request)
    await vm.load()

    return vm.to_dict()


@router.get("/reporte/3")
@template(template_file="reporte/asignacion_registro_docentes.pt")
async def reporte_asignacion_registro_docentes(request: Request):
    vm = ReporteAsignacionRegistroDocentes(request)
    await vm.load()

    return vm.to_dict()


@router.get("/reporte/4")
@template(template_file="reporte/resumen_producto_rango_fechas.pt")
async def reporte_resumen_producto_rango_fechas(request: Request):
    vm = ReporteResumenProductoRangoFechas(request)
    await vm.load_empty()

    return vm.to_dict()


@router.post("/reporte/4/fecha_inicio/{fecha_inicio}/fecha_termino/{fecha_termino}")
@template(template_file="reporte/resumen_producto_rango_fechas.pt")
async def reporte_resumen_producto_rango_fechas_post(request: Request, fecha_inicio: date, fecha_termino: date):
    vm = ReporteResumenProductoRangoFechas(request)
    await vm.load(fecha_inicio, fecha_termino)

    return vm.to_dict()


@router.get("/reporte/5")
@template(template_file="reporte/detalle_producto_taller_rango_fechas.pt")
async def reporte_detalle_producto_taller_rango_fechas(request: Request):
    vm = ReporteDetalleProductoTallerRangoFechas(request)
    await vm.load_empty()

    return vm.to_dict()


@router.post("/reporte/5/fecha_inicio/{fecha_inicio}/fecha_termino/{fecha_termino}")
@template(template_file="reporte/detalle_producto_taller_rango_fechas.pt")
async def reporte_detalle_producto_taller_rango_fechas_post(request: Request, fecha_inicio: date, fecha_termino: date):
    vm = ReporteDetalleProductoTallerRangoFechas(request)
    await vm.load(fecha_inicio, fecha_termino)

    return vm.to_dict()


@router.get("/reporte/1/excel")
async def reporte_valorizacion_taller_excel(request: Request):
    vm = ReporteValorizacionTaller(request)
    await vm.load()

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.registros)

    # Devolver el Excel como una respuesta
    filename = "Reporte valorización talleres"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})


@router.get("/reporte/2/excel")
async def reporte_presupuesto_estimado_asignatura_excel(request: Request):
    vm = ReportePresupuestoEstimadoAsignatura(request)
    await vm.load()

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.registros)

    # Devolver el Excel como una respuesta
    filename = "Reporte presupuesto estimado asignaturas"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})


@router.get("/reporte/3/excel")
async def reporte_asignacion_registro_docentes_excel(request: Request):
    vm = ReporteAsignacionRegistroDocentes(request)
    await vm.load()

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.registros)

    # Devolver el Excel como una respuesta
    filename = "Reporte asignación-registro docentes"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})


@router.get("/reporte/4/excel/fecha_inicio/{fecha_inicio}/fecha_termino/{fecha_termino}")
async def reporte_resumen_producto_rango_fechas_excel(request: Request, fecha_inicio: date, fecha_termino: date):
    vm = ReporteResumenProductoRangoFechas(request)
    await vm.load(fecha_inicio, fecha_termino)

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.registros)

    # Devolver el Excel como una respuesta
    filename = f"{fecha_inicio} - {fecha_termino} - Reporte resumen producto rango fechas"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})


@router.get("/reporte/5/excel/fecha_inicio/{fecha_inicio}/fecha_termino/{fecha_termino}")
async def reporte_detalle_producto_taller_rango_fechas_excel(request: Request, fecha_inicio: date, fecha_termino: date):
    vm = ReporteDetalleProductoTallerRangoFechas(request)
    await vm.load(fecha_inicio, fecha_termino)

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.registros)

    # Devolver el Excel como una respuesta
    filename = f"{fecha_inicio} - {fecha_termino} - Reporte detalle producto talle rango fechas"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})


@router.get("/reporte/1/pdf")
async def reporte_valorizacion_taller_pdf(request: Request):
    vm = ReporteValorizacionTaller(request)
    await vm.load()

    # Generar el archivo PDF
    titulo = "Reporte valorización talleres"
    pdf_content = await generar_pdf(datos=vm.registros, titulo=titulo)

    # Devolver el PDF como una respuesta
    return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=" + titulo + ".pdf"})


@router.get("/reporte/2/pdf")
async def reporte_presupuesto_estimado_asignatura_pdf(request: Request):
    vm = ReportePresupuestoEstimadoAsignatura(request)
    await vm.load()

    # Generar el archivo PDF
    titulo = "Reporte presupuesto estimado asignaturas"
    subtitulo = f"Año académico {vm.ano_academ}"
    pdf_content = await generar_pdf(datos=vm.registros, titulo=titulo, subtitulo=subtitulo)

    # Devolver el PDF como una respuesta
    return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=" + titulo + ".pdf"})


@router.get("/reporte/3/pdf")
async def reporte_asignacion_registro_docentes_pdf(request: Request):
    vm = ReporteAsignacionRegistroDocentes(request)
    await vm.load()

    # Generar el archivo PDF
    titulo = "Reporte asignación-registro docentes"
    subtitulo = f"Año académico {vm.ano_academ}"
    pdf_content = await generar_pdf(datos=vm.registros, titulo=titulo, subtitulo=subtitulo)

    # Devolver el PDF como una respuesta
    return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=" + titulo + ".pdf"})
