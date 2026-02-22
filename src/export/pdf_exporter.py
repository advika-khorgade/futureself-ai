"""Export decisions to PDF."""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
from ..schemas import AgentState


class PDFExporter:
    """Export decision analysis to PDF."""
    
    @staticmethod
    def export_decision(state: AgentState, username: str = "User") -> BytesIO:
        """
        Export decision analysis to PDF.
        
        Returns:
            BytesIO buffer containing PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("🔮 FutureSelf AI", title_style))
        story.append(Paragraph("Decision Analysis Report", styles['Heading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Metadata
        rec = state.recommendation
        metadata = [
            ["Generated:", datetime.now().strftime("%B %d, %Y at %I:%M %p")],
            ["User:", username],
            ["Decision:", state.decision_input.decision[:100] + "..." if len(state.decision_input.decision) > 100 else state.decision_input.decision]
        ]
        
        t = Table(metadata, colWidths=[1.5*inch, 5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t)
        story.append(Spacer(1, 0.5*inch))
        
        # Recommendation Summary
        story.append(Paragraph("Strategic Recommendation", heading_style))
        
        summary_data = [
            ["Recommendation:", rec.recommendation],
            ["Confidence Level:", f"{rec.confidence_level:.0%}"],
            ["Risk Score:", f"{rec.overall_risk_score:.1f}/10"],
            ["Opportunity Score:", f"{rec.overall_opportunity_score:.1f}/10"]
        ]
        
        t = Table(summary_data, colWidths=[2*inch, 4.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t)
        story.append(Spacer(1, 0.3*inch))
        
        # Risk-Reward Balance
        story.append(Paragraph(rec.risk_reward_balance, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Key Insights
        story.append(Paragraph("Key Insights", heading_style))
        for i, insight in enumerate(rec.key_insights, 1):
            story.append(Paragraph(f"{i}. {insight}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Next Steps
        story.append(Paragraph("Next Steps", heading_style))
        for action in rec.next_steps:
            story.append(Paragraph(
                f"<b>[{action.priority.upper()}]</b> {action.action}",
                styles['Normal']
            ))
            story.append(Paragraph(
                f"<i>Timeframe: {action.timeframe}</i>",
                styles['Normal']
            ))
            story.append(Spacer(1, 0.1*inch))
        
        # Page break before detailed analysis
        story.append(PageBreak())
        
        # Risk Analysis
        story.append(Paragraph("Risk Analysis", heading_style))
        risk_data = [["Factor", "Score", "Severity", "Reasoning"]]
        for risk in state.risk_output.risk_scores:
            risk_data.append([
                risk.factor_name,
                f"{risk.score:.1f}/10",
                risk.severity.upper(),
                risk.reasoning[:100] + "..." if len(risk.reasoning) > 100 else risk.reasoning
            ])
        
        t = Table(risk_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 3.4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        story.append(t)
        story.append(Spacer(1, 0.3*inch))
        
        # Opportunity Analysis
        story.append(Paragraph("Opportunity Analysis", heading_style))
        opp_data = [["Factor", "Score", "Potential", "Reasoning"]]
        for opp in state.opportunity_output.opportunity_scores:
            opp_data.append([
                opp.factor_name,
                f"{opp.score:.1f}/10",
                opp.potential.upper(),
                opp.reasoning[:100] + "..." if len(opp.reasoning) > 100 else opp.reasoning
            ])
        
        t = Table(opp_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 3.4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        story.append(t)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "Generated by FutureSelf AI - Decision Intelligence Platform",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
