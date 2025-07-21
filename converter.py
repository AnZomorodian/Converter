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
        elif file_extension in ['.html', '.htm']:
            success = convert_html_to_pdf(input_path, output_path, quality)
        elif file_extension == '.xml':
            success = convert_xml_to_pdf(input_path, output_path, quality)
        elif file_extension == '.json':
            success = convert_json_to_pdf(input_path, output_path, quality)
        elif file_extension == '.md':
            success = convert_markdown_to_pdf(input_path, output_path, quality)
        elif file_extension in ['.py', '.js', '.css']:
            success = convert_code_to_pdf(input_path, output_path, quality)
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

def convert_html_to_pdf(input_path, output_path, quality='high'):
    """Convert HTML files to PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        import html
        
        # Read HTML file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple HTML to text conversion (basic)
        content = html.unescape(content)
        # Remove HTML tags (basic approach)
        import re
        content = re.sub('<[^<]+?>', '', content)
        
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
        logging.error(f"HTML conversion error: {str(e)}")
        return False

def convert_xml_to_pdf(input_path, output_path, quality='high'):
    """Convert XML files to PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Read XML file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add XML content as preformatted text
        pre = Preformatted(content, styles['Code'])
        story.append(pre)
        
        pdf_doc.build(story)
        return True
    
    except Exception as e:
        logging.error(f"XML conversion error: {str(e)}")
        return False

def convert_json_to_pdf(input_path, output_path, quality='high'):
    """Convert JSON files to PDF"""
    try:
        import json
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Read and format JSON file
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Create PDF
        pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add formatted JSON as preformatted text
        pre = Preformatted(formatted_json, styles['Code'])
        story.append(pre)
        
        pdf_doc.build(story)
        return True
    
    except Exception as e:
        logging.error(f"JSON conversion error: {str(e)}")
        return False

def convert_markdown_to_pdf(input_path, output_path, quality='high'):
    """Convert Markdown files to PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        import re
        
        # Read Markdown file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic markdown to text conversion
        # Remove markdown syntax (basic approach)
        content = re.sub(r'#+\s*', '', content)  # Headers
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)  # Italic
        content = re.sub(r'`(.*?)`', r'\1', content)  # Code
        
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
        logging.error(f"Markdown conversion error: {str(e)}")
        return False

def convert_code_to_pdf(input_path, output_path, quality='high'):
    """Convert code files (Python, JavaScript, CSS) to PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Read code file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add filename as header
        file_extension = Path(input_path).suffix.upper()
        header = Paragraph(f"{file_extension[1:]} Code File", styles['Heading1'])
        story.append(header)
        story.append(Spacer(1, 20))
        
        # Add code content as preformatted text
        pre = Preformatted(content, styles['Code'])
        story.append(pre)
        
        pdf_doc.build(story)
        return True
    
    except Exception as e:
        logging.error(f"Code conversion error: {str(e)}")
        return False

def add_password_to_pdf(pdf_path, password):
    """Add password protection to PDF using PyPDF2"""
    try:
        from PyPDF2 import PdfReader, PdfWriter
        import os
        
        # Read the original PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # Add all pages to writer
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)
        
        # Encrypt with password
        writer.encrypt(password)
        
        # Create temporary file path
        temp_path = f"{pdf_path}.temp"
        
        # Write encrypted PDF to temp file
        with open(temp_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Replace original with encrypted version
        os.replace(temp_path, pdf_path)
        
        logging.info(f"Successfully added password protection to PDF")
        return True
    
    except Exception as e:
        logging.error(f"Password protection error: {str(e)}")
        return False

def convert_image_format(input_path, output_path, target_format='jpg', quality=95):
    """
    Convert between different image formats - IMPROVED VERSION
    """
    try:
        from PIL import Image
        import os
        
        # Ensure output path has correct extension
        output_dir = os.path.dirname(output_path)
        output_name = os.path.splitext(os.path.basename(output_path))[0]
        
        # Set correct file extension based on target format
        if target_format.lower() in ['jpg', 'jpeg']:
            output_path = os.path.join(output_dir, f"{output_name}.jpg")
        elif target_format.lower() == 'png':
            output_path = os.path.join(output_dir, f"{output_name}.png")
        elif target_format.lower() == 'webp':
            output_path = os.path.join(output_dir, f"{output_name}.webp")
        elif target_format.lower() == 'bmp':
            output_path = os.path.join(output_dir, f"{output_name}.bmp")
        elif target_format.lower() in ['tiff', 'tif']:
            output_path = os.path.join(output_dir, f"{output_name}.tiff")
        else:
            logging.error(f"Unsupported target format: {target_format}")
            return False, None
        
        # Open and convert the image
        with Image.open(input_path) as img:
            # Log original format and mode for debugging
            logging.info(f"Converting from {img.format} ({img.mode}) to {target_format.upper()}")
            
            # Handle transparency and mode conversion based on target format
            if target_format.lower() in ['jpg', 'jpeg']:
                # JPEG doesn't support transparency - convert to RGB with white background
                if img.mode in ['RGBA', 'LA', 'P']:
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode not in ['RGB', 'L']:
                    img = img.convert('RGB')
                    
            elif target_format.lower() == 'png':
                # PNG supports all modes, prefer RGBA for transparency
                if img.mode not in ['RGBA', 'RGB', 'L', 'LA', 'P']:
                    img = img.convert('RGBA')
                    
            elif target_format.lower() == 'bmp':
                # BMP doesn't support transparency - convert to RGB
                if img.mode in ['RGBA', 'LA', 'P']:
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode not in ['RGB', 'L']:
                    img = img.convert('RGB')
                    
            elif target_format.lower() in ['tiff', 'tif']:
                # TIFF supports most modes including RGBA
                if img.mode not in ['RGBA', 'RGB', 'L', 'LA', 'CMYK']:
                    img = img.convert('RGBA')
                    
            elif target_format.lower() == 'webp':
                # WebP supports RGBA and RGB
                if img.mode not in ['RGBA', 'RGB']:
                    img = img.convert('RGBA' if 'transparency' in img.info or img.mode in ['RGBA', 'LA'] else 'RGB')
                    
            elif target_format.lower() == 'gif':
                # GIF requires P mode (palette) or L mode
                if img.mode not in ['P', 'L']:
                    # Convert to P mode for GIF with optimized palette
                    img = img.convert('P')
                    
            elif target_format.lower() == 'ico':
                # ICO typically uses RGBA
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                    
            elif target_format.lower() in ['eps', 'pdf']:
                # EPS and PDF require RGB mode
                if img.mode != 'RGB':
                    if img.mode in ['RGBA', 'LA']:
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img)
                        img = background
                    else:
                        img = img.convert('RGB')
            else:
                # For other formats, try to preserve the original mode or convert to RGB
                if img.mode not in ['RGB', 'RGBA', 'L', 'LA']:
                    img = img.convert('RGB')
            
            # Save in target format with appropriate settings
            if target_format.lower() in ['jpg', 'jpeg']:
                img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            elif target_format.lower() == 'png':
                img.save(output_path, 'PNG', optimize=True, compress_level=6)
            elif target_format.lower() == 'webp':
                img.save(output_path, 'WEBP', quality=quality, optimize=True, method=6)
            elif target_format.lower() == 'bmp':
                # BMP doesn't support quality or compression settings
                img.save(output_path, 'BMP')
            elif target_format.lower() in ['tiff', 'tif']:
                # TIFF compression without quality setting for compatibility
                img.save(output_path, 'TIFF', compression='lzw')
            elif target_format.lower() == 'gif':
                # Convert to P mode for GIF and handle transparency
                if img.mode not in ['P', 'L']:
                    img = img.convert('P')
                img.save(output_path, 'GIF', optimize=True)
            elif target_format.lower() == 'ico':
                # ICO format for icons
                img.save(output_path, 'ICO')
            elif target_format.lower() == 'tga':
                # TGA format
                img.save(output_path, 'TGA')
            elif target_format.lower() in ['jp2', 'jpeg2000']:
                # JPEG 2000 format (simplified saving)
                try:
                    img.save(output_path, 'JPEG2000')
                except Exception:
                    # Fallback to JPEG if JPEG2000 not supported
                    output_path = output_path.rsplit('.', 1)[0] + '.jpg'
                    img.save(output_path, 'JPEG', quality=quality)
            elif target_format.lower() == 'eps':
                # EPS format (PostScript) - convert to RGB first
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, 'EPS')
            elif target_format.lower() == 'pdf':
                # PDF format - ensure RGB mode
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, 'PDF', resolution=100.0)
            
        logging.info(f"Successfully converted image to {target_format.upper()} format: {output_path}")
        return True, output_path
        
    except Exception as e:
        logging.error(f"Image format conversion error: {str(e)}")
        return False, None

def merge_pdfs(input_paths, output_path, file_order=None, passwords=None):
    """
    Merge multiple PDF files into one with advanced settings
    Args:
        input_paths: List of PDF file paths
        output_path: Output merged PDF path
        file_order: Optional list of indices to specify order (0-based)
        passwords: Optional dict of {file_path: password} for protected PDFs
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        import PyPDF2
        
        writer = PdfWriter()
        processed_files = []
        
        # Use custom order if specified, otherwise use original order
        if file_order:
            # Reorder input_paths based on file_order indices
            try:
                ordered_paths = [input_paths[i] for i in file_order if i < len(input_paths)]
                input_paths = ordered_paths
            except (IndexError, TypeError):
                logging.warning("Invalid file order specified, using original order")
        
        for i, path in enumerate(input_paths):
            if not os.path.exists(path):
                logging.warning(f"PDF file not found: {path}")
                continue
                
            try:
                # Get password for this file if provided
                password = passwords.get(path) if passwords else None
                
                # Try to open the PDF
                reader = PdfReader(path)
                
                # Handle password-protected PDFs
                if reader.is_encrypted:
                    if password:
                        try:
                            reader.decrypt(password)
                            logging.info(f"Successfully decrypted PDF: {os.path.basename(path)}")
                        except Exception as e:
                            logging.error(f"Failed to decrypt PDF {path} with provided password: {str(e)}")
                            continue
                    else:
                        logging.warning(f"PDF {path} is password-protected but no password provided")
                        continue
                
                # Add all pages from this PDF
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    writer.add_page(page)
                
                processed_files.append(os.path.basename(path))
                logging.info(f"Added {len(reader.pages)} pages from {os.path.basename(path)}")
                
            except Exception as e:
                logging.error(f"Error processing PDF {path}: {str(e)}")
                continue
        
        if not processed_files:
            logging.error("No valid PDF files were processed")
            return False
        
        # Write the merged PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logging.info(f"Successfully merged {len(processed_files)} PDFs: {', '.join(processed_files)}")
        return True
        
    except Exception as e:
        logging.error(f"PDF merge error: {str(e)}")
        return False

def convert_multiple_images_to_pdf(input_paths, output_path, quality='high'):
    """
    Convert multiple images into a single PDF
    """
    try:
        from PIL import Image
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, A4
        
        # Choose page size based on quality
        if quality == 'high':
            page_size = A4
        else:
            page_size = letter
        
        c = canvas.Canvas(output_path, pagesize=page_size)
        page_width, page_height = page_size
        
        for img_path in input_paths:
            if not os.path.exists(img_path):
                logging.warning(f"Image file not found: {img_path}")
                continue
                
            try:
                # Open and process image
                with Image.open(img_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ['RGBA', 'LA']:
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    
                    # Calculate scaling to fit page
                    img_width, img_height = img.size
                    scale_x = (page_width - 40) / img_width  # 20pt margin on each side
                    scale_y = (page_height - 40) / img_height  # 20pt margin on each side
                    scale = min(scale_x, scale_y)
                    
                    # Calculate centered position
                    new_width = img_width * scale
                    new_height = img_height * scale
                    x = (page_width - new_width) / 2
                    y = (page_height - new_height) / 2
                    
                    # Save temporary file for reportlab
                    temp_img_path = f"{img_path}_temp.jpg"
                    img.save(temp_img_path, 'JPEG', quality=85)
                    
                    # Add image to PDF
                    c.drawImage(temp_img_path, x, y, width=new_width, height=new_height)
                    c.showPage()
                    
                    # Clean up temp file
                    if os.path.exists(temp_img_path):
                        os.remove(temp_img_path)
                        
            except Exception as e:
                logging.error(f"Error processing image {img_path}: {str(e)}")
                continue
        
        c.save()
        logging.info(f"Successfully converted {len(input_paths)} images to PDF")
        return True
        
    except Exception as e:
        logging.error(f"Multiple images to PDF conversion error: {str(e)}")
        return False
