import re


# ============================================================
# JOB SKILL KNOWLEDGE BASE
# ============================================================

JOB_SKILLS = [

    # ========================================================
    # PROGRAMMING LANGUAGES
    # ========================================================

    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "Go",
    "Golang",
    "Rust",
    "Kotlin",
    "Swift",
    "R",
    "PHP",
    "Ruby",
    "Scala",
    "Dart",

    # ========================================================
    # WEB DEVELOPMENT
    # ========================================================

    "HTML",
    "CSS",
    "React",
    "React.js",
    "Angular",
    "Vue",
    "Vue.js",
    "Next.js",
    "Node.js",
    "Express",
    "Express.js",
    "Bootstrap",
    "Tailwind CSS",

    # ========================================================
    # BACKEND / API
    # ========================================================

    "FastAPI",
    "Flask",
    "Django",
    "Spring",
    "Spring Boot",
    "Spring Framework",
    "REST API",
    "RESTful API",
    "GraphQL",
    "Microservices",

    # ========================================================
    # DATABASES
    # ========================================================

    "SQL",
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "Oracle",
    "SQL Server",
    "MongoDB",
    "Redis",
    "Cassandra",
    "DynamoDB",

    # ========================================================
    # AI / MACHINE LEARNING
    # ========================================================

    "Artificial Intelligence",
    "AI",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",
    "Generative AI",
    "GenAI",
    "Large Language Models",
    "LLM",
    "LLMs",
    "Reinforcement Learning",

    # ========================================================
    # MACHINE LEARNING LIBRARIES
    # ========================================================

    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "XGBoost",
    "LightGBM",
    "Hugging Face",
    "Transformers",

    # ========================================================
    # DATA SCIENCE
    # ========================================================

    "Pandas",
    "NumPy",
    "SciPy",
    "Matplotlib",
    "Seaborn",
    "Plotly",
    "Jupyter",
    "Jupyter Notebook",
    "Statistics",
    "Data Analysis",
    "Data Science",
    "Data Visualization",

    # ========================================================
    # ML ALGORITHMS
    # ========================================================

    "Random Forest",
    "Support Vector Machine",
    "SVM",
    "Linear Regression",
    "Logistic Regression",
    "Decision Tree",
    "K-Means",
    "KNN",
    "K-Nearest Neighbors",
    "Naive Bayes",
    "Neural Networks",
    "CNN",
    "Convolutional Neural Network",
    "RNN",
    "LSTM",
    "Collaborative Filtering",

    # ========================================================
    # BIG DATA
    # ========================================================

    "Apache Spark",
    "Spark",
    "Hadoop",
    "Hive",
    "Kafka",
    "PySpark",
    "Databricks",

    # ========================================================
    # CLOUD
    # ========================================================

    "AWS",
    "Amazon Web Services",
    "Microsoft Azure",
    "Azure",
    "Google Cloud",
    "GCP",
    "Google Cloud Platform",

    # ========================================================
    # DEVOPS
    # ========================================================

    "Git",
    "GitHub",
    "GitLab",
    "Bitbucket",
    "Docker",
    "Kubernetes",
    "Jenkins",
    "CI/CD",
    "Terraform",
    "Ansible",

    # ========================================================
    # OPERATING SYSTEMS
    # ========================================================

    "Linux",
    "Unix",
    "Windows",

    # ========================================================
    # DATA / BI TOOLS
    # ========================================================

    "Power BI",
    "Tableau",
    "Excel",
    "MS Excel",
    "Looker",
    "QlikView",

    # ========================================================
    # ENTERPRISE / PRODUCTIVITY
    # ========================================================

    "Jira",
    "Confluence",
    "SAP",
    "Salesforce",
    "ERP",

    # ========================================================
    # TESTING
    # ========================================================

    "Selenium",
    "JUnit",
    "PyTest",
    "pytest",
    "Postman",

    # ========================================================
    # OTHER IMPORTANT TECHNOLOGIES
    # ========================================================

    "MATLAB",
    "OpenCV",
    "CUDA",
    "GitHub Actions"
]


# ============================================================
# LOAD JOB DESCRIPTION
# ============================================================

def load_job_description(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# EXTRACT JOB SKILLS
# ============================================================

def extract_job_skills(job_description):

    found_skills = []

    normalized_text = re.sub(
        r"\s+",
        " ",
        job_description
    )

    for skill in JOB_SKILLS:

        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(
            pattern,
            normalized_text,
            re.IGNORECASE
        ):

            if skill not in found_skills:
                found_skills.append(skill)

    return found_skills


# ============================================================
# CLASSIFY SKILL IMPORTANCE
# ============================================================

def classify_skill_importance(
    job_description,
    skills
):

    result = {
        "Required": [],
        "Preferred": [],
        "Nice to Have": []
    }

    # Split description into sentences
    sentences = re.split(
        r"[.!?\n]+",
        job_description
    )

    for skill in skills:

        skill_found = False

        for sentence in sentences:

            if not re.search(
                rf"(?<!\w){re.escape(skill)}(?!\w)",
                sentence,
                re.IGNORECASE
            ):
                continue

            skill_found = True

            sentence_lower = sentence.lower()


            # ================================================
            # NICE TO HAVE
            # ================================================

            nice_words = [
                "nice to have",
                "bonus",
                "plus",
                "advantage"
            ]

            if any(
                word in sentence_lower
                for word in nice_words
            ):

                result["Nice to Have"].append(skill)

                break


            # ================================================
            # PREFERRED
            # ================================================

            preferred_words = [
                "preferred",
                "prefer",
                "desired",
                "preferred qualification",
                "preferred skill"
            ]

            if any(
                word in sentence_lower
                for word in preferred_words
            ):

                result["Preferred"].append(skill)

                break


            # ================================================
            # REQUIRED
            # ================================================

            required_words = [
                "required",
                "must have",
                "mandatory",
                "essential",
                "strong",
                "good knowledge",
                "experience in",
                "experience with",
                "knowledge of",
                "skills in",
                "skills",
                "proficiency"
            ]

            if any(
                word in sentence_lower
                for word in required_words
            ):

                result["Required"].append(skill)

                break


            # ================================================
            # DEFAULT
            # ================================================

            result["Required"].append(skill)

            break


        # If skill wasn't matched to any sentence
        if not skill_found:

            result["Required"].append(skill)


    return result


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    job_path = "data/job_description.txt"

    job_description = load_job_description(
        job_path
    )

    skills = extract_job_skills(
        job_description
    )

    categorized = classify_skill_importance(
        job_description,
        skills
    )


    print("\n===== JOB REQUIRED SKILLS =====")

    for skill in skills:
        print(f"✓ {skill}")


    print("\n===== SKILL IMPORTANCE =====")


    print("\n🔴 REQUIRED:")

    for skill in categorized["Required"]:
        print(f"  ✓ {skill}")


    print("\n🟡 PREFERRED:")

    for skill in categorized["Preferred"]:
        print(f"  ✓ {skill}")


    print("\n🟢 NICE TO HAVE:")

    for skill in categorized["Nice to Have"]:
        print(f"  ✓ {skill}")