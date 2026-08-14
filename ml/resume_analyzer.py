import re
import os
import shutil

from pypdf import PdfReader


# ============================================================
# SKILL KNOWLEDGE BASE
# ============================================================

SKILL_CATEGORIES = {

    "Programming Languages": [
        "Python",
        "Java",
        "C++",
        "C",
        "JavaScript"
    ],

    "Web Technologies": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Angular",
        "Node.js"
    ],

    "Data Science & Machine Learning": [
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "Natural Language Processing",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "TensorFlow",
        "PyTorch"
    ],

    "Machine Learning Algorithms": [
        "Random Forest",
        "SVM",
        "Support Vector Machine",
        "Linear Regression",
        "Logistic Regression",
        "Decision Tree",
        "K-Means",
        "KNN",
        "Collaborative Filtering"
    ],

    "Databases": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Oracle"
    ],

    "Data Visualization & BI": [
        "Power BI",
        "Tableau",
        "Excel",
        "MS Excel",
        "Matplotlib"
    ],

    "Cloud & DevOps": [
        "AWS",
        "Azure",
        "Microsoft Azure",
        "Google Cloud",
        "GCP",
        "Docker",
        "Kubernetes",
        "Git",
        "GitHub"
    ],

    "Enterprise & Business Tools": [
        "ERP",
        "MS Word",
        "MS PowerPoint",
        "Microsoft Office"
    ]
}


# ============================================================
# FIND TESSERACT
# ============================================================

def configure_tesseract():
    """
    Configure Tesseract OCR for both Windows and Linux/Streamlit Cloud.
    """

    import pytesseract

    # --------------------------------------------------------
    # 1. Check whether tesseract is already in PATH
    # --------------------------------------------------------

    tesseract_executable = shutil.which("tesseract")

    if tesseract_executable:

        pytesseract.pytesseract.tesseract_cmd = (
            tesseract_executable
        )

        return tesseract_executable

    # --------------------------------------------------------
    # 2. Windows fallback
    # --------------------------------------------------------

    windows_paths = [

        r"C:\Program Files\Tesseract-OCR\tesseract.exe",

        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]

    for path in windows_paths:

        if os.path.exists(path):

            pytesseract.pytesseract.tesseract_cmd = path

            return path

    # --------------------------------------------------------
    # 3. Nothing found
    # --------------------------------------------------------

    return None


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):

    """
    Extract text from a PDF.

    First:
        Try normal PDF text extraction.

    If no readable text is found:
        Convert PDF pages to images and use Tesseract OCR.

    Works on:
        Windows
        Streamlit Cloud / Linux
    """

    # ========================================================
    # STEP 1 — NORMAL PDF TEXT EXTRACTION
    # ========================================================

    extracted_text = ""

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            text = page.extract_text()

            if text:

                extracted_text += text + "\n"

    except Exception as error:

        print(
            f"⚠️ Normal PDF extraction failed: {error}"
        )

    # ========================================================
    # CHECK WHETHER TEXT WAS FOUND
    # ========================================================

    if extracted_text.strip():

        print(
            "✓ Text extracted using PDF text extraction"
        )

        return extracted_text

    # ========================================================
    # STEP 2 — OCR FALLBACK
    # ========================================================

    print(
        "⚠️ No readable text found."
    )

    print(
        "🔍 Switching to OCR..."
    )

    try:

        import pytesseract

        from pdf2image import convert_from_path

        # ----------------------------------------------------
        # CONFIGURE TESSERACT
        # ----------------------------------------------------

        tesseract_executable = configure_tesseract()

        if not tesseract_executable:

            print(
                "❌ Tesseract OCR executable was not found."
            )

            print(
                "Please install Tesseract or configure it in PATH."
            )

            return ""

        print(
            f"✓ Tesseract found: {tesseract_executable}"
        )

        # ----------------------------------------------------
        # CONVERT PDF TO IMAGES
        # ----------------------------------------------------

        pages = convert_from_path(
            pdf_path,
            dpi=300
        )

        # ----------------------------------------------------
        # OCR EACH PAGE
        # ----------------------------------------------------

        ocr_text = ""

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            print(
                f"🔍 OCR processing page {page_number}..."
            )

            text = pytesseract.image_to_string(
                page,
                lang="eng"
            )

            ocr_text += text + "\n"

        # ----------------------------------------------------
        # VERIFY OCR RESULT
        # ----------------------------------------------------

        if ocr_text.strip():

            print(
                "✓ Text successfully extracted using OCR"
            )

            return ocr_text

        print(
            "❌ OCR completed but no readable text was found."
        )

        return ""

    except Exception as error:

        print(
            f"❌ OCR processing failed: {error}"
        )

        return ""


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(resume_text):

    """
    Detect skills from resume text.
    """

    found_skills = []

    if not resume_text:

        return found_skills

    normalized_text = re.sub(
        r"\s+",
        " ",
        resume_text
    )

    for category, skills in SKILL_CATEGORIES.items():

        for skill in skills:

            pattern = (
                rf"(?<!\w)"
                rf"{re.escape(skill)}"
                rf"(?!\w)"
            )

            if re.search(
                pattern,
                normalized_text,
                re.IGNORECASE
            ):

                if skill not in found_skills:

                    found_skills.append(skill)

    return found_skills


# ============================================================
# CREATE CANDIDATE PROFILE
# ============================================================

def create_candidate_profile(
    resume_text,
    candidate_skills
):

    """
    Create structured candidate profile.
    """

    # --------------------------------------------------------
    # Extract candidate name
    # --------------------------------------------------------

    name = "Unknown Candidate"

    if resume_text:

        lines = [
            line.strip()
            for line in resume_text.splitlines()
            if line.strip()
        ]

        if lines:

            first_line = lines[0]

            # Ignore obvious non-name lines
            if (
                len(first_line) < 60
                and not re.search(
                    r"@|http|www\.|resume|curriculum",
                    first_line,
                    re.IGNORECASE
                )
            ):

                name = first_line

    # --------------------------------------------------------
    # Categorize skills
    # --------------------------------------------------------

    categorized_skills = {}

    for category, skills in SKILL_CATEGORIES.items():

        matched = []

        for skill in skills:

            if skill in candidate_skills:

                matched.append(skill)

        if matched:

            categorized_skills[category] = matched

    # --------------------------------------------------------
    # Candidate profile
    # --------------------------------------------------------

    return {

        "name": name,

        "skills": categorized_skills,

        "resume_text_length": len(
            resume_text
        ) if resume_text else 0
    }


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    resume_path = "data/resume.pdf"

    print(
        "\n===== RESUME ANALYZER ====="
    )

    resume_text = extract_text_from_pdf(
        resume_path
    )

    print(
        "\n===== RESUME TEXT ====="
    )

    print(resume_text)

    skills = extract_skills(
        resume_text
    )

    print(
        "\n===== DETECTED SKILLS ====="
    )

    for skill in skills:

        print(
            f"✓ {skill}"
        )

    profile = create_candidate_profile(
        resume_text,
        skills
    )

    print(
        "\n===== CANDIDATE PROFILE ====="
    )

    print(profile)

