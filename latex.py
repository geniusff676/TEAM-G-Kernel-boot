from flask import Flask, request, send_file, jsonify
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

app = Flask(__name__)

@app.route('/api/latex-to-pdf', methods=['POST'])
def latex_to_pdf():
    """
    Convert LaTeX code to PDF
    Expected JSON body: {"latex": "LaTeX code here"}
    """
    data = request.get_json()
    
    if not data or 'latex' not in data:
        return jsonify({'error': 'LaTeX content is required'}), 400
    
    latex_content = data['latex']
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # File paths
        tex_file = os.path.join(temp_dir, 'document.tex')
        pdf_file = os.path.join(temp_dir, 'document.pdf')
        
        # Write LaTeX content to file
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Compile LaTeX to PDF using pdflatex
        # Run twice to resolve references
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                capture_output=True,
                text=True,
                timeout=30
            )
        
        # Check if PDF was generated
        if not os.path.exists(pdf_file):
            error_log = result.stderr if result.stderr else result.stdout
            return jsonify({
                'error': 'Failed to compile LaTeX',
                'details': error_log
            }), 500
        
        # Send PDF file
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='document.pdf'
        )
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'LaTeX compilation timed out'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Cleanup temporary directory
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

@app.route('/api/latex-to-pdf/stream', methods=['POST'])
def latex_to_pdf_stream():
    """
    Convert LaTeX to PDF and return as response stream
    (Doesn't download, displays in browser)
    """
    data = request.get_json()
    
    if not data or 'latex' not in data:
        return jsonify({'error': 'LaTeX content is required'}), 400
    
    latex_content = data['latex']
    temp_dir = tempfile.mkdtemp()
    
    try:
        tex_file = os.path.join(temp_dir, 'document.tex')
        pdf_file = os.path.join(temp_dir, 'document.pdf')
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                capture_output=True,
                text=True,
                timeout=30
            )
        
        if not os.path.exists(pdf_file):
            error_log = result.stderr if result.stderr else result.stdout
            return jsonify({
                'error': 'Failed to compile LaTeX',
                'details': error_log
            }), 500
        
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=False
        )
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'LaTeX compilation timed out'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
