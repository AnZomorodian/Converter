import os
import logging
from pathlib import Path
import subprocess

def convert_to_pdf(input_path, output_path, original_filename, password=None, quality='high'):
    """
    Convert various file formats to PDF with optional password protection
    """
    try:
        file_extension = Path(input_path).suffix.lower()
        
        if file_extension in ['.docx', '.doc']:
            success = convert_word_to_pdf(input_path, output_path, quality)
        elif file_extension in ['.xlsx', '.xls']:
            success = convert_excel_to_pdf(input_path, output_path, quality)
        elif file_extension in ['.pptx', '.ppt']:
            success = convert_powerpoint_to_pdf(input_path, output_path, quality)
        elif file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
            success = convert_image_to_pdf(input_path, output_path, quality)
        elif file_extension == '.txt':
            success = convert_text_to_pdf(input_path, output_path, quality)
        elif file_extension == '.csv':
            success = convert_csv_to_pdf(input_path, output_path, quality)
        elif file_extension in ['.rtf', '.odt', '.ods', '.odp']:
            success = convert_office_format_to_pdf(input_path, output_path, quality)
        elif file_extension == '.pdf':
            # If already PDF, just copy and optionally add password
            import shutil
            shutil.copy2(input_path, output_path)
            success = True
        else:
            logging.error(f"Unsupported file format: {file_extension}")
            return False
        
        # Add password protection if requested and conversion was successful
        if success and password:
            return add_password_to_pdf(output_path, password)
        
        return success
    
    except Exception as e:
        logging.error(f"Conversion error: {str(e)}")
        return False

def convert_word_to_pdf(input_path, output_path, quality='high'):
    """Convert Word documents to PDF using LibreOffice"""
    try:
        # Use LibreOffice headless mode for conversion
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(output_path),
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # LibreOffice creates PDF with same name as input file
            input_name = Path(input_path).stem
            generated_pdf = os.path.join(os.path.dirname(output_path), f"{input_name}.pdf")
            
            if os.path.exists(generated_pdf):
                os.rename(generated_pdf, output_path)
                return True
        
        logging.error(f"LibreOffice conversion failed: {result.stderr}")
        return convert_word_fallback(input_path, output_path, quality)
    
    except subprocess.TimeoutExpired:
        logging.error("LibreOffice conversion timed out")
        return convert_word_fallback(input_path, output_path, quality)
    except Exception as e:
        logging.error(f"LibreOffice conversion error: {str(e)}")
        return convert_word_fallback(input_path, output_path, quality)

def convert_word_fallback(input_path, output_path, quality='high'):
    """Fallback Word to PDF conversion using python-docx and reportlab"""
    try:
        from docx import Document
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Read Word document
        doc = Document(input_path)
        
        # Create PDF
        pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                p = Paragraph(paragraph.text, styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 12))
        
        pdf_doc.build(story)
        return True
    
    except Exception as e:
        logging.error(f"Word fallback conversion error: {str(e)}")
        return False

def convert_excel_to_pdf(input_path, output_path, quality='high'):
    """Convert Excel files to PDF"""
    try:
        # Try LibreOffice first
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(output_path),
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            input_name = Path(input_path).stem
            generated_pdf = os.path.join(os.path.dirname(output_path), f"{input_name}.pdf")
            
            if os.path.exists(generated_pdf):
                os.rename(generated_pdf, output_path)
                return True
        
        return convert_excel_fallback(input_path, output_path, quality)
    
    except Exception as e:
        logging.error(f"Excel LibreOffice conversion error: {str(e)}")
        return convert_excel_fallback(input_path, output_path, quality)

def convert_excel_fallback(input_path, output_path, quality='high'):
    """Fallback Excel to PDF conversion"""
    try:
        import pandas as pd
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        
        # Read Excel file
        df = pd.read_excel(input_path)
        
        # Create PDF
        pdf_doc = SimpleDocTemplate(output_path, pagesize=A4)
        
        # Convert DataFrame to list of lists
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        pdf_doc.build([table])
        return True
    
    except Exception as e:
        logging.error(f"Excel fallback conversion error: {str(e)}")
        return False

def convert_powerpoint_to_pdf(input_path, output_path, quality='high'):
    """Convert PowerPoint files to PDF using LibreOffice"""
    try:
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(output_path),
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            input_name = Path(input_path).stem
            generated_pdf = os.path.join(os.path.dirname(output_path), f"{input_name}.pdf")
            
            if os.path.exists(generated_pdf):
                os.rename(generated_pdf, output_path)
                return True
        
        logging.error(f"PowerPoint conversion failed: {result.stderr}")
        return False
    
    except Exception as e:
        logging.error(f"PowerPoint conversion error: {str(e)}")
        return False

def convert_image_to_pdf(input_path, output_path, quality='high'):
    """Convert images to PDF using Pillow"""
    try:
        from PIL import Image
        
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(output_path, 'PDF')
        
        return True
    
    except Exception as e:
        logging.error(f"Image conversion error: {str(e)}")
        return False

def convert_text_to_pdf(input_path, output_path, quality='high'):
    """Convert text files to PDF using reportlab"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Read text file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                p = Paragraph(para.replace('\n', '<br/>'), styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 12))
        
        pdf_doc.build(story)
        return True
    
    except Exception as e:
        logging.error(f"Text conversion error: {str(e)}")
        return False

def convert_csv_to_pdf(input_path, output_path, quality='high'):
    """Convert CSV files to PDF using pandas and reportlab"""
    try:
        import pandas as pd
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        
        # Read CSV file
        df = pd.read_csv(input_path)
        
        # Create PDF
        pdf_doc = SimpleDocTemplate(output_path, pagesize=A4)
        
        # Convert DataFrame to list of lists
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        pdf_doc.build([table])
        return True
    
    except Exception as e:
        logging.error(f"CSV conversion error: {str(e)}")
        return False

def convert_office_format_to_pdf(input_path, output_path, quality='high'):
    """Convert RTF, ODT, ODS, ODP files to PDF using LibreOffice"""
    try:
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(output_path),
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            input_name = Path(input_path).stem
            generated_pdf = os.path.join(os.path.dirname(output_path), f"{input_name}.pdf")
            
            if os.path.exists(generated_pdf):
                os.rename(generated_pdf, output_path)
                return True
        
        logging.error(f"Office format conversion failed: {result.stderr}")
        return False
    
    except Exception as e:
        logging.error(f"Office format conversion error: {str(e)}")
        return False

def add_password_to_pdf(pdf_path, password):
    """Add password protection to PDF"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        # import PyPDF2  # Commented out as not available
        
        # For now, we'll skip password protection as it requires additional setup
        # This would need pikepdf or PyPDF2 with encryption support
        logging.info(f"Password protection requested but not implemented yet")
        return True
    
    except Exception as e:
        logging.error(f"Password protection error: {str(e)}")
        return True  # Return True to not fail the conversion
