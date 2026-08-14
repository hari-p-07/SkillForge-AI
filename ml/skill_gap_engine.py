# ============================================================
# SKILL GAP ENGINE
# ============================================================


# ============================================================
# SKILL NORMALIZATION / ALIASES
# ============================================================

SKILL_ALIASES = {

    # Programming
    "py": "python",
    "python3": "python",

    "js": "javascript",
    "node js": "node.js",
    "nodejs": "node.js",

    # Machine Learning
    "ml": "machine learning",
    "machine-learning": "machine learning",

    "dl": "deep learning",
    "deep-learning": "deep learning",

    "ai": "artificial intelligence",

    # NLP
    "nlp": "nlp",
    "natural language processing": "nlp",
    "natural-language processing": "nlp",

    # Data Science
    "pd": "pandas",
    "np": "numpy",

    # Databases
    "mysql": "mysql",
    "postgres": "postgresql",
    "postgres db": "postgresql",

    # Cloud
    "amazon web services": "aws",
    "google cloud platform": "gcp",

    # Version control
    "version control": "git",
    "version control system": "git",

    # Machine Learning libraries
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    # APIs
    "rest api": "rest api",
    "restful api": "rest api"
}


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):
    """
    Convert a skill into a standard representation.
    """

    if not skill:
        return ""

    normalized = (
        skill
        .strip()
        .lower()
        .replace("_", " ")
    )

    normalized = " ".join(
        normalized.split()
    )

    return SKILL_ALIASES.get(
        normalized,
        normalized
    )


# ============================================================
# FLATTEN CANDIDATE SKILLS
# ============================================================

def flatten_candidate_skills(candidate_profile):
    """
    Convert categorized candidate skills into
    one flat list.
    """

    all_skills = []

    for category, skills in candidate_profile["skills"].items():

        all_skills.extend(skills)

    return all_skills


# ============================================================
# CREATE NORMALIZED CANDIDATE SET
# ============================================================

def create_normalized_skill_set(skills):
    """
    Create a normalized set of candidate skills.
    """

    return {
        normalize_skill(skill)
        for skill in skills
        if normalize_skill(skill)
    }


# ============================================================
# BASIC SKILL MATCHING
# ============================================================

def calculate_skill_gap(
    candidate_skills,
    required_skills
):
    """
    Calculate basic skill matching using
    normalized skill names.
    """

    candidate_set = create_normalized_skill_set(
        candidate_skills
    )

    required_set = create_normalized_skill_set(
        required_skills
    )

    matching_keys = (
        candidate_set &
        required_set
    )

    missing_keys = (
        required_set -
        candidate_set
    )


    # --------------------------------------------------------
    # Preserve original skill names
    # --------------------------------------------------------

    candidate_lookup = {}

    for skill in candidate_skills:

        key = normalize_skill(skill)

        if key not in candidate_lookup:

            candidate_lookup[key] = skill


    required_lookup = {}

    for skill in required_skills:

        key = normalize_skill(skill)

        if key not in required_lookup:

            required_lookup[key] = skill


    matching_skills = sorted(

        required_lookup[key]

        for key in matching_keys

        if key in required_lookup
    )


    missing_skills = sorted(

        required_lookup[key]

        for key in missing_keys

        if key in required_lookup
    )


    if required_set:

        match_percentage = (

            len(matching_keys)

            /

            len(required_set)

        ) * 100

    else:

        match_percentage = 0


    return {

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,

        "match_percentage": round(
            match_percentage,
            2
        )
    }


# ============================================================
# CATEGORY-WEIGHTED SCORING
# ============================================================

def calculate_category_weighted_match(
    candidate_skills,
    categorized_job_skills
):
    """
    Calculate candidate suitability using
    category-level importance.

    Required      = 70%
    Preferred     = 20%
    Nice to Have  = 10%
    """

    category_weights = {

        "Required": 0.70,

        "Preferred": 0.20,

        "Nice to Have": 0.10
    }


    candidate_set = create_normalized_skill_set(
        candidate_skills
    )


    category_scores = {}

    overall_score = 0


    matching_skills = []

    missing_skills = []


    # ========================================================
    # PROCESS EACH CATEGORY
    # ========================================================

    for category, skills in categorized_job_skills.items():

        category_weight = category_weights.get(
            category,
            0
        )


        total_skills = len(skills)


        if total_skills == 0:

            category_scores[category] = {

                "matched": 0,

                "total": 0,

                "percentage": 0,

                "weight": category_weight,

                "contribution": 0
            }

            continue


        matched = 0


        for skill in skills:

            normalized_skill = normalize_skill(
                skill
            )


            if normalized_skill in candidate_set:

                matched += 1

                matching_skills.append(
                    skill
                )

            else:

                missing_skills.append(
                    skill
                )


        category_percentage = (

            matched

            /

            total_skills

        ) * 100


        category_contribution = (

            category_percentage

            *

            category_weight
        )


        overall_score += (
            category_contribution
        )


        category_scores[category] = {

            "matched": matched,

            "total": total_skills,

            "percentage": round(
                category_percentage,
                2
            ),

            "weight": category_weight,

            "contribution": round(
                category_contribution,
                2
            )
        }


    return {

        "overall_score": round(
            overall_score,
            2
        ),

        "category_scores": category_scores,

        "matching_skills": sorted(
            matching_skills
        ),

        "missing_skills": sorted(
            missing_skills
        )
    }


# ============================================================
# SKILL PRIORITY
# ============================================================

def get_skill_priorities(
    candidate_skills,
    categorized_job_skills
):
    """
    Generate a learning priority list.

    Required skills get highest priority,
    followed by preferred and nice-to-have.
    """

    candidate_set = create_normalized_skill_set(
        candidate_skills
    )


    priority_order = [

        "Required",

        "Preferred",

        "Nice to Have"
    ]


    priorities = []


    for category in priority_order:

        skills = categorized_job_skills.get(
            category,
            []
        )


        for skill in skills:

            normalized_skill = normalize_skill(
                skill
            )


            if normalized_skill not in candidate_set:

                priorities.append({

                    "skill": skill,

                    "category": category
                })


    return priorities


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    candidate_profile = {

        "name": "Test Candidate",

        "skills": {

            "Programming Languages": [

                "Python"
            ],

            "Data Science & Machine Learning": [

                "ML",

                "Pandas"
            ],

            "Databases": [

                "SQL"
            ]
        }
    }


    categorized_job_skills = {

        "Required": [

            "Python",

            "Machine Learning",

            "SQL",

            "Git"
        ],

        "Preferred": [

            "NLP",

            "FastAPI"
        ],

        "Nice to Have": [

            "AWS"
        ]
    }


    candidate_skills = flatten_candidate_skills(
        candidate_profile
    )


    result = calculate_category_weighted_match(

        candidate_skills,

        categorized_job_skills
    )


    priorities = get_skill_priorities(

        candidate_skills,

        categorized_job_skills
    )


    print("\n===== SKILLFORGE AI SMART MATCHING =====")


    print(
        f"\nOverall Score: "
        f"{result['overall_score']}%"
    )


    print("\n===== CATEGORY SCORES =====")


    for category, data in result[
        "category_scores"
    ].items():

        print(
            f"\n{category}"
        )

        print(
            f"  Matched: "
            f"{data['matched']}/"
            f"{data['total']}"
        )

        print(
            f"  Score: "
            f"{data['percentage']}%"
        )

        print(
            f"  Weight: "
            f"{data['weight'] * 100}%"
        )

        print(
            f"  Contribution: "
            f"{data['contribution']}%"
        )


    print("\n===== MATCHING SKILLS =====")

    for skill in result["matching_skills"]:

        print(
            f"  ✓ {skill}"
        )


    print("\n===== MISSING SKILLS =====")


    for skill in result["missing_skills"]:

        print(
            f"  ✗ {skill}"
        )


    print("\n===== MISSING SKILL PRIORITY =====")


    for index, item in enumerate(
        priorities,
        start=1
    ):

        print(
            f"{index}. "
            f"{item['skill']} "
            f"({item['category']})"
        )