import re
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
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):

    """
    Extract text from a PDF.

    First tries normal PDF text extraction using pypdf.
    If no usable text is found, automatically falls back
    to OCR using Tesseract.
    """

    from pypdf import PdfReader

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
        # TESSERACT LOCATION
        # ----------------------------------------------------

        tesseract_path = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        pytesseract.pytesseract.tesseract_cmd = (
            tesseract_path
        )


        # ----------------------------------------------------
        # CONVERT PDF PAGES TO IMAGES
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
            "❌ OCR could not extract any text."
        )


        return ""


    except Exception as error:

        print(
            f"❌ OCR failed: {error}"
        )

        return ""
    


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Normalize resume text for skill detection.
    """

    # Replace multiple spaces/newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(resume_text):
    """
    Detect known technical skills from resume text.
    """

    cleaned_text = clean_text(resume_text)

    detected_skills = []

    for category, skills in SKILL_CATEGORIES.items():

        for skill in skills:

            pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

            if re.search(
                pattern,
                cleaned_text,
                re.IGNORECASE
            ):

                if skill not in detected_skills:
                    detected_skills.append(skill)

    return detected_skills


# ============================================================
# CATEGORIZE SKILLS
# ============================================================

def categorize_skills(detected_skills):
    """
    Organize detected skills into categories.
    """

    categorized = {}

    for category, skills in SKILL_CATEGORIES.items():

        matched_skills = []

        for skill in skills:

            if skill in detected_skills:

                matched_skills.append(skill)

        if matched_skills:

            categorized[category] = matched_skills

    return categorized


# ============================================================
# EXTRACT CANDIDATE NAME
# ============================================================

def extract_candidate_name(resume_text):
    """
    Try to extract the candidate name from the beginning
    of the resume.
    """

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    if lines:
        return lines[0]

    return "Unknown Candidate"


# ============================================================
# CREATE CANDIDATE PROFILE
# ============================================================

def create_candidate_profile(
    resume_text,
    detected_skills
):
    """
    Create structured candidate information.
    """

    categorized_skills = categorize_skills(
        detected_skills
    )

    candidate_name = extract_candidate_name(
        resume_text
    )

    return {

        "name": candidate_name,

        "skills": categorized_skills,

        "resume_text_length": len(resume_text)
    }


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    resume_path = "data/resume.pdf"

    print("\n===== RESUME ANALYZER =====")

    resume_text = extract_text_from_pdf(
        resume_path
    )

    print("\n===== RESUME TEXT =====")

    print(resume_text)

    detected_skills = extract_skills(
        resume_text
    )

    print("\n===== DETECTED SKILLS =====")

    for skill in detected_skills:
        print(f"✓ {skill}")

    candidate_profile = create_candidate_profile(
        resume_text,
        detected_skills
    )

    print("\n===== CANDIDATE PROFILE =====")

    print(candidate_profile)