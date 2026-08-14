# ============================================================
# SKILL GAP ENGINE
# ============================================================


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
# BASIC SKILL MATCHING
# ============================================================

def calculate_skill_gap(
    candidate_skills,
    required_skills
):
    """
    Calculate simple skill matching.

    This is kept for comparison with the
    advanced scoring system.
    """

    candidate_set = {
        skill.lower()
        for skill in candidate_skills
    }

    required_set = {
        skill.lower()
        for skill in required_skills
    }

    matching_keys = (
        candidate_set &
        required_set
    )

    missing_keys = (
        required_set -
        candidate_set
    )

    # Preserve original names
    candidate_lookup = {
        skill.lower(): skill
        for skill in candidate_skills
    }

    required_lookup = {
        skill.lower(): skill
        for skill in required_skills
    }

    matching_skills = sorted(
        candidate_lookup[key]
        for key in matching_keys
    )

    missing_skills = sorted(
        required_lookup[key]
        for key in missing_keys
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


    candidate_set = {
        skill.lower()
        for skill in candidate_skills
    }


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

                "weight": category_weight
            }

            continue


        matched = 0


        for skill in skills:

            if skill.lower() in candidate_set:

                matched += 1

                matching_skills.append(
                    skill
                )

            else:

                missing_skills.append(
                    skill
                )


        category_percentage = (
            matched /
            total_skills
        ) * 100


        category_contribution = (
            category_percentage *
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

    candidate_set = {
        skill.lower()
        for skill in candidate_skills
    }


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

            if skill.lower() not in candidate_set:

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

        "name": "Harish P",

        "skills": {

            "Programming Languages": [
                "Python",
                "Java"
            ],

            "Data Science & Machine Learning": [
                "Machine Learning",
                "Pandas",
                "NumPy"
            ],

            "Databases": [
                "SQL"
            ]
        }
    }


    categorized_job_skills = {

        "Required": [
            "Python",
            "Java",
            "SQL",
            "Git",
            "GitHub",
            "Docker"
        ],

        "Preferred": [
            "Machine Learning",
            "FastAPI",
            "Flask"
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


    print("\n===== SKILLFORGE AI SCORING =====")


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