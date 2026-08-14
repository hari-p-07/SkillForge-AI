import streamlit as st
import tempfile
import os

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
    calculate_category_weighted_match,
    get_skill_priorities
)


# ============================================================
# PAGE CONFIGURATION
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
    "AI-Powered Resume & Job Skill Matching"
)

st.write(
    "Upload your resume and paste a job description "
    "to discover your skill match, skill gaps, and "
    "learning priorities."
)


st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

left_column, right_column = st.columns(2)


# ------------------------------------------------------------
# RESUME UPLOAD
# ------------------------------------------------------------

with left_column:

    st.header("📄 Upload Resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"]
    )


# ------------------------------------------------------------
# JOB DESCRIPTION
# ------------------------------------------------------------

with right_column:

    st.header("📋 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Python developer "
            "with experience in SQL, Git, Docker..."
        )
    )


st.divider()


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🔍 Analyze My Match",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if uploaded_resume is None:

        st.error(
            "⚠️ Please upload your resume PDF."
        )

    elif not job_description.strip():

        st.error(
            "⚠️ Please enter a job description."
        )

    else:

        try:

            # =================================================
            # SAVE UPLOADED RESUME TEMPORARILY
            # =================================================

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_resume.getvalue()
                )

                temp_resume_path = temp_file.name


            # =================================================
            # STEP 1 — RESUME ANALYSIS
            # =================================================

            with st.spinner(
                "🔍 Analyzing your resume..."
            ):

                resume_text = (
                    extract_text_from_pdf(
                        temp_resume_path
                    )
                )

                candidate_skills = (
                    extract_skills(
                        resume_text
                    )
                )

                candidate_profile = (
                    create_candidate_profile(
                        resume_text,
                        candidate_skills
                    )
                )


            # =================================================
            # STEP 2 — JOB ANALYSIS
            # =================================================

            with st.spinner(
                "🧠 Analyzing job requirements..."
            ):

                job_skills = (
                    extract_job_skills(
                        job_description
                    )
                )

                categorized_job_skills = (
                    classify_skill_importance(
                        job_description,
                        job_skills
                    )
                )


            # =================================================
            # STEP 3 — MATCHING
            # =================================================

            with st.spinner(
                "📊 Calculating your skill match..."
            ):

                candidate_skill_list = (
                    flatten_candidate_skills(
                        candidate_profile
                    )
                )

                scoring_result = (
                    calculate_category_weighted_match(
                        candidate_skill_list,
                        categorized_job_skills
                    )
                )

                priorities = (
                    get_skill_priorities(
                        candidate_skill_list,
                        categorized_job_skills
                    )
                )


            # =================================================
            # CLEANUP TEMPORARY FILE
            # =================================================

            os.remove(
                temp_resume_path
            )


            # =================================================
            # RESULTS
            # =================================================

            st.success(
                "✅ Analysis completed successfully!"
            )


            st.divider()


            # =================================================
            # CANDIDATE
            # =================================================

            st.header(
                f"👤 Candidate: "
                f"{candidate_profile['name']}"
            )


            # =================================================
            # OVERALL SCORE
            # =================================================

            overall_score = (
                scoring_result["overall_score"]
            )


            score_column, skill_column = st.columns(2)


            with score_column:

                st.metric(
                    "🎯 Overall Match",
                    f"{overall_score}%"
                )


            with skill_column:

                st.metric(
                    "🧠 Skills Detected",
                    len(candidate_skill_list)
                )


            st.divider()


            # =================================================
            # CATEGORY PERFORMANCE
            # =================================================

            st.header(
                "📊 Skill Category Performance"
            )


            category_data = (
                scoring_result[
                    "category_scores"
                ]
            )


            category_columns = st.columns(3)


            categories = [
                ("Required", "🔴"),
                ("Preferred", "🟡"),
                ("Nice to Have", "🟢")
            ]


            for column, (category, emoji) in zip(
                category_columns,
                categories
            ):

                data = category_data.get(
                    category,
                    {
                        "matched": 0,
                        "total": 0,
                        "percentage": 0
                    }
                )


                with column:

                    st.subheader(
                        f"{emoji} {category}"
                    )

                    st.metric(
                        "Match",
                        f"{data['percentage']}%"
                    )

                    st.write(
                        f"{data['matched']} / "
                        f"{data['total']} skills"
                    )


            st.divider()


            # =================================================
            # REQUIRED SKILLS
            # =================================================

            st.header(
                "🔴 Required Skills"
            )


            candidate_lookup = {
                skill.lower()
                for skill in candidate_skill_list
            }


            for skill in categorized_job_skills[
                "Required"
            ]:

                if skill.lower() in candidate_lookup:

                    st.success(
                        f"✓ {skill}"
                    )

                else:

                    st.error(
                        f"✗ {skill}"
                    )


            # =================================================
            # PREFERRED SKILLS
            # =================================================

            st.header(
                "🟡 Preferred Skills"
            )


            for skill in categorized_job_skills[
                "Preferred"
            ]:

                if skill.lower() in candidate_lookup:

                    st.success(
                        f"✓ {skill}"
                    )

                else:

                    st.warning(
                        f"✗ {skill}"
                    )


            # =================================================
            # NICE TO HAVE
            # =================================================

            st.header(
                "🟢 Nice to Have"
            )


            for skill in categorized_job_skills[
                "Nice to Have"
            ]:

                if skill.lower() in candidate_lookup:

                    st.success(
                        f"✓ {skill}"
                    )

                else:

                    st.info(
                        f"✗ {skill}"
                    )


            st.divider()


            # =================================================
            # LEARNING PRIORITY
            # =================================================

            st.header(
                "📚 Recommended Learning Priorities"
            )


            if priorities:

                for index, item in enumerate(
                    priorities,
                    start=1
                ):

                    category = item[
                        "category"
                    ]

                    skill = item[
                        "skill"
                    ]

                    if category == "Required":

                        st.error(
                            f"**{index}. {skill}** "
                            f"— Required"
                        )

                    elif category == "Preferred":

                        st.warning(
                            f"**{index}. {skill}** "
                            f"— Preferred"
                        )

                    else:

                        st.info(
                            f"**{index}. {skill}** "
                            f"— Nice to Have"
                        )

            else:

                st.success(
                    "🎉 No skill gaps detected!"
                )


            st.divider()


            # =================================================
            # FINAL MESSAGE
            # =================================================

            if overall_score >= 80:

                st.success(
                    "🌟 Strong candidate match!"
                )

            elif overall_score >= 60:

                st.info(
                    "👍 Good match. A few skill gaps "
                    "should be addressed."
                )

            elif overall_score >= 40:

                st.warning(
                    "⚠️ Moderate match. Focus on the "
                    "required missing skills."
                )

            else:

                st.error(
                    "🚨 Significant skill gaps detected. "
                    "Consider developing the priority skills."
                )


        except Exception as error:

            st.error(
                f"❌ Something went wrong:\n\n{error}"
            )