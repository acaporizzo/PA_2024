from fpdf import FPDF

class GeneradorReporte:
    def _init_(self):
        self.pdf = FPDF()

    def generar_reporte(self, reclamos, estadisticas, formato="PDF"):
        if formato == "PDF":
            return self._generar_pdf(reclamos, estadisticas)
        elif formato == "HTML":
            return self._generar_html(reclamos, estadisticas)
    
    def _generar_pdf(self, reclamos, estadisticas):
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(200, 10, txt="Reporte de Reclamos", ln=True, align='C')
        self.pdf.cell(200, 10, txt=f"Total de Reclamos: {estadisticas['total_reclamos']}", ln=True)
        self.pdf.cell(200, 10, txt=f"En Proceso: {estadisticas['porcentaje_en_proceso']}%", ln=True)
        self.pdf.cell(200, 10, txt=f"Resueltos: {estadisticas['porcentaje_resueltos']}%", ln=True)
        self.pdf.cell(200, 10, txt=f"Pendientes: {estadisticas['porcentaje_pendientes']}%", ln=True)

        for reclamo in reclamos:
            self.pdf.cell(200, 10, txt=f"ID: {reclamo.id_reclamo} - {reclamo.contenido[:50]}", ln=True)
        self.pdf.output("reporte_reclamos.pdf")
        return "PDF generado: reporte_reclamos.pdf"

    def _generar_html(self, reclamos, estadisticas):
        html = "<html><head><title>Reporte de Reclamos</title></head><body>"
        html += "<h1>Reporte de Reclamos</h1>"
        html += f"<p>Total de Reclamos: {estadisticas['total_reclamos']}</p>"
        html += f"<p>En Proceso: {estadisticas['porcentaje_en_proceso']}%</p>"
        html += f"<p>Resueltos: {estadisticas['porcentaje_resueltos']}%</p>"
        html += f"<p>Pendientes: {estadisticas['porcentaje_pendientes']}%</p>"

        html += "<ul>"
        for reclamo in reclamos:
            html += f"<li>ID: {reclamo.id_reclamo} - {reclamo.contenido[:50]}</li>"
        html += "</ul></body></html>"
        with open("reporte_reclamos.html", "w") as file:
            file.write(html)

        return "HTML generado: reporte_reclamos.html"
