# -*- coding: utf-8 -*-
"""
Utilitário para exportação de dados
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
from config.settings import EXPORTS_DIR
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

logger = logging.getLogger(__name__)

class ExportManager:
    """Gerenciador de exportações"""
    
    def __init__(self):
        self.export_dir = EXPORTS_DIR
        
    def export_to_excel(self, data, filename, sheet_name="Dados"):
        """Exportar dados para Excel"""
        try:
            if not data:
                raise ValueError("Não há dados para exportar")
            
            # Preparar nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            full_filename = f"{filename}_{timestamp}.xlsx"
            filepath = self.export_dir / full_filename
            
            # Criar DataFrame
            df = pd.DataFrame(data)
            
            # Exportar para Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Ajustar largura das colunas
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"Dados exportados para Excel: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao exportar para Excel: {e}")
            raise
    
    def export_to_csv(self, data, filename):
        """Exportar dados para CSV"""
        try:
            if not data:
                raise ValueError("Não há dados para exportar")
            
            # Preparar nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            full_filename = f"{filename}_{timestamp}.csv"
            filepath = self.export_dir / full_filename
            
            # Criar DataFrame e exportar
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"Dados exportados para CSV: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao exportar para CSV: {e}")
            raise
    
    def export_to_pdf(self, data, filename, title="Relatório"):
        """Exportar dados para PDF"""
        try:
            if not data:
                raise ValueError("Não há dados para exportar")
            
            # Preparar nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            full_filename = f"{filename}_{timestamp}.pdf"
            filepath = self.export_dir / full_filename
            
            # Criar documento PDF
            doc = SimpleDocTemplate(str(filepath), pagesize=A4)
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                alignment=1,  # Centro
                spaceAfter=30
            )
            
            # Título
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))
            
            # Preparar dados da tabela
            if data:
                # Cabeçalhos
                headers = list(data[0].keys())
                table_data = [headers]
                
                # Dados
                for row in data:
                    table_data.append([str(row.get(col, '')) for col in headers])
                
                # Criar tabela
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                
                elements.append(table)
            
            # Rodapé com data
            elements.append(Spacer(1, 20))
            footer = Paragraph(
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
                styles['Normal']
            )
            elements.append(footer)
            
            # Construir PDF
            doc.build(elements)
            
            logger.info(f"Dados exportados para PDF: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao exportar para PDF: {e}")
            raise
    
    def export_produtos(self, produtos, formato='xlsx'):
        """Exportar lista de produtos"""
        # Preparar dados para exportação
        export_data = []
        for produto in produtos:
            export_data.append({
                'Código': produto.get('codigo', ''),
                'Nome': produto.get('nome', ''),
                'Categoria': produto.get('categoria_nome', ''),
                'Fornecedor': produto.get('fornecedor_nome', ''),
                'Preço Compra': f"R$ {produto.get('preco_compra', 0):.2f}",
                'Preço Venda': f"R$ {produto.get('preco_venda', 0):.2f}",
                'Estoque Atual': produto.get('estoque_atual', 0),
                'Estoque Mínimo': produto.get('estoque_minimo', 0),
                'Unidade': produto.get('unidade', ''),
                'Localização': produto.get('localizacao', '')
            })
        
        # Exportar conforme formato
        if formato == 'xlsx':
            return self.export_to_excel(export_data, 'relatorio_produtos')
        elif formato == 'csv':
            return self.export_to_csv(export_data, 'relatorio_produtos')
        elif formato == 'pdf':
            return self.export_to_pdf(export_data, 'relatorio_produtos', 'Relatório de Produtos')
        else:
            raise ValueError(f"Formato não suportado: {formato}")
    
    def export_movimentacoes(self, movimentacoes, formato='xlsx'):
        """Exportar movimentações de estoque"""
        # Preparar dados para exportação
        export_data = []
        for mov in movimentacoes:
            export_data.append({
                'Data': mov.get('data_movimentacao', ''),
                'Produto': mov.get('produto_nome', ''),
                'Código': mov.get('produto_codigo', ''),
                'Tipo': mov.get('tipo', '').title(),
                'Quantidade': mov.get('quantidade', 0),
                'Preço Unitário': f"R$ {mov.get('preco_unitario', 0):.2f}",
                'Valor Total': f"R$ {mov.get('valor_total', 0):.2f}",
                'Motivo': mov.get('motivo', ''),
                'Documento': mov.get('documento', ''),
                'Usuário': mov.get('usuario', '')
            })
        
        # Exportar conforme formato
        if formato == 'xlsx':
            return self.export_to_excel(export_data, 'relatorio_movimentacoes')
        elif formato == 'csv':
            return self.export_to_csv(export_data, 'relatorio_movimentacoes')
        elif formato == 'pdf':
            return self.export_to_pdf(export_data, 'relatorio_movimentacoes', 'Relatório de Movimentações')
        else:
            raise ValueError(f"Formato não suportado: {formato}") 