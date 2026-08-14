from ml.resume_analyzer import (
    extract_text_from_pdf,
    extract_skills,
    create_candidate_profile
)

from ml.job_analyser import (
    load_job_description,
    extract_job_skills,
    classify_skill_importance
)

from ml.skill_gap_engine import (
    flatten_candidate_skills,
    calculate_skill_gap,
    calculate_category_weighted_match,
    get_skill_priorities,
    find_skill_evidence
)


# ============================================================
# FILE PATHS
# ============================================================

RESUME_PATH = "data/resume.pdf"
JOB_DESCRIPTION_PATH = "data/job_description.txt"


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    print("\n" + "=" * 60)
    print("              SKILLFORGE AI")
    print("        Resume & Job Skill Analyzer")
    print("=" * 60)


    # ========================================================
    # STEP 1 — RESUME ANALYSIS
    # ========================================================

    print("\n[1/3] Analyzing resume...")

    resume_text = extract_text_from_pdf(
        RESUME_PATH
    )

    candidate_skills = extract_skills(
        resume_text
    )

    candidate_profile = create_candidate_profile(
        resume_text,
        candidate_skills
    )

    print(
        f"✓ Resume analyzed: "
        f"{candidate_profile['name']}"
    )


    # ========================================================
    # STEP 2 — JOB ANALYSIS
    # ========================================================

    print("\n[2/3] Analyzing job description...")

    job_description = load_job_description(
        JOB_DESCRIPTION_PATH
    )

    job_skills = extract_job_skills(
        job_description
    )

    categorized_job_skills = classify_skill_importance(
        job_description,
        job_skills
    )

    print(
        f"✓ Detected "
        f"{len(job_skills)} job skills"
    )


    # ========================================================
    # STEP 3 — SKILL GAP ANALYSIS
    # ========================================================

    print("\n[3/3] Calculating skill gap...")

    candidate_skill_list = flatten_candidate_skills(
        candidate_profile
    )


    # --------------------------------------------------------
    # Basic matching
    # --------------------------------------------------------

    basic_result = calculate_skill_gap(
        candidate_skill_list,
        job_skills
    )


    # --------------------------------------------------------
    # Category weighted scoring
    # --------------------------------------------------------

    scoring_result = calculate_category_weighted_match(
        candidate_skill_list,
        categorized_job_skills
    )


    # --------------------------------------------------------
    # Learning priorities
    # --------------------------------------------------------

    priorities = get_skill_priorities(
        candidate_skill_list,
        categorized_job_skills
    )


    # ========================================================
    # SKILL EVIDENCE ANALYSIS
    # ========================================================

    evidence_details = []

    for category, skills in categorized_job_skills.items():

        for skill in skills:

            evidence = find_skill_evidence(
                skill,
                candidate_skill_list
            )

            evidence["category"] = category

            evidence_details.append(
                evidence
            )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")

    print("=" * 60)
    print("              SKILLFORGE AI REPORT")
    print("=" * 60)


    print(
        f"\nCandidate: "
        f"{candidate_profile['name']}"
    )


    print(
        f"\n🎯 Overall Match: "
        f"{scoring_result['overall_score']}%"
    )


    print(
        f"📊 Basic Match: "
        f"{basic_result['match_percentage']}%"
    )


    # ========================================================
    # CATEGORY PERFORMANCE
    # ========================================================

    print("\n" + "-" * 60)
    print("📊 CATEGORY PERFORMANCE")
    print("-" * 60)


    for category, data in (
        scoring_result["category_scores"].items()
    ):

        print(f"\n{category}")

        print(
            f"  Match: "
            f"{data['matched']}/"
            f"{data['total']} "
            f"({data['percentage']}%)"
        )

        print(
            f"  Weight: "
            f"{data['weight'] * 100}%"
        )

        print(
            f"  Contribution: "
            f"{data['contribution']}%"
        )


    # ========================================================
    # SMART SKILL EVIDENCE
    # ========================================================

    print("\n" + "-" * 60)
    print("🔍 SMART SKILL EVIDENCE")
    print("-" * 60)


    for category in [
        "Required",
        "Preferred",
        "Nice to Have"
    ]:

        if category == "Required":
            print("\n🔴 REQUIRED SKILLS")

        elif category == "Preferred":
            print("\n🟡 PREFERRED SKILLS")

        else:
            print("\n🟢 NICE TO HAVE")


        for evidence in evidence_details:

            if evidence["category"] != category:
                continue


            skill = evidence["skill"]


            # ------------------------------------------------
            # DIRECT MATCH
            # ------------------------------------------------

            if evidence["direct_match"]:

                print(
                    f"  ✓ {skill} "
                    f"[Direct Match]"
                )


            # ------------------------------------------------
            # RELATED EVIDENCE
            # ------------------------------------------------

            elif evidence["evidence_score"] > 0:

                related = ", ".join(
                    evidence["related_skills"]
                )

                print(
                    f"  ⚡ {skill} "
                    f"[{evidence['evidence_level']} Evidence - "
                    f"{evidence['evidence_score']}%]"
                )

                print(
                    f"      Related: {related}"
                )


            # ------------------------------------------------
            # MISSING
            # ------------------------------------------------

            else:

                print(
                    f"  ✗ {skill} "
                    f"[Missing]"
                )


    # ========================================================
    # LEARNING PRIORITY
    # ========================================================

    print("\n" + "-" * 60)
    print("📚 LEARNING PRIORITY")
    print("-" * 60)


    if priorities:

        for index, item in enumerate(
            priorities,
            start=1
        ):

            print(
                f"  {index}. "
                f"{item['skill']} "
                f"[{item['category']}]"
            )

    else:

        print(
            "  🎉 No skill gaps detected!"
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "-" * 60)
    print("📌 SUMMARY")
    print("-" * 60)


    print(
        f"  Matching Skills: "
        f"{len(scoring_result['matching_skills'])}"
    )


    print(
        f"  Missing Skills: "
        f"{len(scoring_result['missing_skills'])}"
    )


    print(
        f"  Overall Score: "
        f"{scoring_result['overall_score']}%"
    )


    print("\n" + "=" * 60)
    print("          END OF SKILLFORGE AI REPORT")
    print("=" * 60)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()