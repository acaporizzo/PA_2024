#from fpdf import FPDF

class GeneradorReporte:
    def _init_(self, formato):
        self.formato = formato

    def generar_reporte(self, reclamos, estadisticas, formato="PDF"):
        pass
    
class GeneradorReportePDF:
    def generar_reporte_pdf(self, reclamos, estadisticas):
        pass

class GeneradorReporteHTML:
    def generar_reporte_html(self, reclamos, estadisticas):
        pass