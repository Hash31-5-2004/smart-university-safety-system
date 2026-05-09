import pdfplumber
import os
from pathlib import Path

def extract_nist_guidelines(pdf_path: str, output_dir: str):
    """
    Extract text from NIST SP 800-53 PDF and save as text files
    """
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Split into sections (basic approach - split by control families)
    sections = split_into_sections(full_text)

    # Save each section as separate txt file
    for section_name, content in sections.items():
        output_file = os.path.join(output_dir, f"nist_{section_name.lower().replace(' ', '_')}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: NIST SP 800-53 - {section_name}\n\n")
            f.write(content)
        print(f"Saved: {output_file}")

def split_into_sections(text: str) -> dict:
    """
    Basic section splitting based on control family headers
    """
    # Common NIST control families
    families = [
        "Access Control", "Awareness and Training", "Audit and Accountability",
        "Security Assessment and Authorization", "Configuration Management",
        "Contingency Planning", "Identification and Authentication",
        "Incident Response", "Maintenance", "Media Protection",
        "Physical and Environmental Protection", "Planning",
        "Program Management", "Recovery", "Risk Assessment",
        "System and Services Acquisition", "System and Communications Protection",
        "System and Information Integrity"
    ]

    sections = {}
    lines = text.split('\n')
    current_section = "Introduction"
    current_content = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line starts a new family
        for family in families:
            if line.upper().startswith(family.upper()) or family.upper() in line.upper():
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = family
                current_content = [line]
                break
        else:
            current_content.append(line)

    # Add the last section
    if current_content:
        sections[current_section] = '\n'.join(current_content)

    return sections

if __name__ == "__main__":
    pdf_path = "data/knowledge_base/nist_sp800-53.pdf"
    output_dir = "data/knowledge_base"

    if os.path.exists(pdf_path):
        extract_nist_guidelines(pdf_path, output_dir)
        print("NIST guidelines extracted successfully!")
    else:
        print(f"PDF file not found: {pdf_path}")