import streamlit as st

from ml.resume_analyzer import (
    extract_text_from_pdf,
    extract_skills,
    create_candidate_profile
)

from ml.job_analyser import (
    extract_job_skills,
    classify_skill_importance
)

from ml.skill_gap_engine import (
    flatten_candidate_skills,
    calculate_skill_gap,
    calculate_category_weighted_match,
    get_skill_priorities
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SkillForge AI",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🎯 SkillForge AI")

st.subheader(
    "AI-Powered Resume & Job Skill Analyzer"
)

st.write(
    "Upload your resume and provide a job description "
    "to discover your skill match, skill gaps and learning priorities."
)


# ============================================================
# INPUT SECTION
# ============================================================

st.divider()

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder="Paste the job description..."
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
):

    if uploaded_resume is None:

        st.error(
            "Please upload a resume PDF."
        )

        st.stop()


    if not job_description.strip():

        st.error(
            "Please enter a job description."
        )

        st.stop()


    # ========================================================
    # SAVE TEMPORARY RESUME
    # ========================================================

    temp_resume_path = "data/uploaded_resume.pdf"

    with open(
        temp_resume_path,
        "wb"
    ) as file:

        file.write(
            uploaded_resume.getbuffer()
        )


    # ========================================================
    # RESUME ANALYSIS
    # ========================================================

    with st.spinner(
        "🔍 Analyzing resume..."
    ):

        resume_text = extract_text_from_pdf(
            temp_resume_path
        )

        candidate_skills = extract_skills(
            resume_text
        )

        candidate_profile = create_candidate_profile(
            resume_text,
            candidate_skills
        )


    # ========================================================
    # JOB ANALYSIS
    # ========================================================

    with st.spinner(
        "💼 Analyzing job description..."
    ):

        job_skills = extract_job_skills(
            job_description
        )

        categorized_job_skills = (
            classify_skill_importance(
                job_description,
                job_skills
            )
        )


    # ========================================================
    # SKILL GAP ANALYSIS
    # ========================================================

    with st.spinner(
        "🧠 Calculating skill gap..."
    ):

        candidate_skill_list = (
            flatten_candidate_skills(
                candidate_profile
            )
        )

        basic_result = calculate_skill_gap(
            candidate_skill_list,
            job_skills
        )

        scoring_result = (
            calculate_category_weighted_match(
                candidate_skill_list,
                categorized_job_skills
            )
        )

        priorities = get_skill_priorities(
            candidate_skill_list,
            categorized_job_skills
        )


    # ========================================================
    # CANDIDATE
    # ========================================================

    st.divider()

    st.header(
        f"👤 Candidate: {candidate_profile['name']}"
    )


    # ========================================================
    # SCORE CARDS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🎯 Overall Match",
            f"{scoring_result['overall_score']}%"
        )


    with col2:

        st.metric(
            "📊 Basic Match",
            f"{basic_result['match_percentage']}%"
        )


    with col3:

        st.metric(
            "🧠 Skills Detected",
            len(candidate_skill_list)
        )


    # ========================================================
    # CATEGORY PERFORMANCE
    # ========================================================

    st.divider()

    st.header("📊 Category Performance")


    category_data = scoring_result[
        "category_scores"
    ]


    for category, data in category_data.items():

        if category == "Required":

            icon = "🔴"

        elif category == "Preferred":

            icon = "🟡"

        else:

            icon = "🟢"


        st.subheader(
            f"{icon} {category}"
        )

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Score",
                f"{data['percentage']}%"
            )


        with col2:

            st.metric(
                "Weight",
                f"{data['weight'] * 100}%"
            )


        with col3:

            st.metric(
                "Contribution",
                f"{data['contribution']}%"
            )


        st.progress(
            min(
                data["percentage"] / 100,
                1.0
            )
        )


    # ========================================================
    # SMART SKILL EVIDENCE
    # ========================================================

    st.divider()

    st.header(
        "🔍 Smart Skill Evidence"
    )


    evidence_lookup = {
        item["skill"]: item
        for item in scoring_result[
            "evidence_details"
        ]
    }


    for category in [
        "Required",
        "Preferred",
        "Nice to Have"
    ]:

        if category == "Required":

            icon = "🔴"

        elif category == "Preferred":

            icon = "🟡"

        else:

            icon = "🟢"


        st.subheader(
            f"{icon} {category}"
        )


        for skill in categorized_job_skills.get(
            category,
            []
        ):

            evidence = evidence_lookup.get(
                skill
            )


            if not evidence:
                continue


            if evidence["direct_match"]:

                st.success(
                    f"✓ {skill} — Direct Match"
                )


            elif evidence["evidence_score"] > 0:

                related = ", ".join(
                    evidence["related_skills"]
                )

                st.warning(
                    f"⚡ {skill} — "
                    f"{evidence['evidence_level']} Evidence "
                    f"({evidence['evidence_score']}%)\n\n"
                    f"Related: {related}"
                )


            else:

                st.error(
                    f"✗ {skill} — Missing"
                )


    # ========================================================
    # LEARNING PRIORITY
    # ========================================================

    st.divider()

    st.header(
        "📚 Learning Priority"
    )


    if priorities:

        for index, item in enumerate(
            priorities,
            start=1
        ):

            st.write(
                f"**{index}. {item['skill']}** "
                f"— {item['category']}"
            )

    else:

        st.success(
            "🎉 No skill gaps detected!"
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.divider()

    st.header("📌 Summary")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Matching Skills",
            len(
                scoring_result[
                    "matching_skills"
                ]
            )
        )


    with col2:

        st.metric(
            "Missing Skills",
            len(
                scoring_result[
                    "missing_skills"
                ]
            )
        )


    with col3:

        st.metric(
            "Overall Score",
            f"{scoring_result['overall_score']}%"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SkillForge AI — Resume & Job Skill Analyzer"
)