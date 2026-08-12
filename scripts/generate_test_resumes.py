"""
Generate 3 distinct test PDF resumes for ATS parsing & job matching verification.
"""

import os
from fpdf import FPDF

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class ResumePDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def create_resume_pdf(filename: str, info: dict) -> None:
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Name Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, info["name"], new_x="LMARGIN", new_y="NEXT")

    # Title & Subtitle
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 7, f"{info['role']} | {info['experience']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        0,
        6,
        f"Email: {info['email']} | Phone: {info['phone']} | Location: {info['location']}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)

    # Horizontal Divider Line
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Professional Summary
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 7, "Professional Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, info["summary"])
    pdf.ln(4)

    # Technical & Core Skills
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 7, "Skills", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, ", ".join(info["skills"]))
    pdf.ln(4)

    # Target Roles
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 7, "Target Roles", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, ", ".join(info["target_roles"]))
    pdf.ln(4)

    # Projects
    if "projects" in info:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 7, "Key Projects", new_x="LMARGIN", new_y="NEXT")
        for proj in info["projects"]:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 6, proj["name"], new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 6, proj["details"])
            pdf.ln(2)

    # Experience Details
    if "experience_details" in info:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 7, "Work Experience", new_x="LMARGIN", new_y="NEXT")
        for exp in info["experience_details"]:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 6, f"{exp['title']} - {exp['company']}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(0, 5, exp["duration"], new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 6, exp["details"])
            pdf.ln(2)

    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)
    print(f"[CREATED] Generated: {filepath}")


def main():
    resumes = [
        {
            "filename": "ui_ux_fresher.pdf",
            "info": {
                "name": "Aisha Sharma",
                "role": "UI/UX Designer",
                "experience": "Fresher",
                "email": "aisha.sharma@example.com",
                "phone": "+91 98765 43210",
                "location": "Bengaluru, India",
                "summary": "Enthusiastic and creative UI/UX Designer passionate about crafting intuitive digital experiences, user research, wireframing, and interactive prototyping for mobile and web applications.",
                "skills": ["Figma", "Adobe XD", "Prototyping", "A/B Testing", "Wireframing", "User Research"],
                "target_roles": ["UI/UX Designer", "Product Designer"],
                "projects": [
                    {
                        "name": "FinTrack Mobile App Redesign",
                        "details": "Redesigned a personal finance tracking mobile application focusing on user onboarding flow, accessibility, interactive charting components, and usability testing.",
                    }
                ],
            },
        },
        {
            "filename": "mechanical_fresher.pdf",
            "info": {
                "name": "Rahul Verma",
                "role": "Mechanical Engineer",
                "experience": "Fresher",
                "email": "rahul.verma@example.com",
                "phone": "+91 98123 45678",
                "location": "Pune, India",
                "summary": "Detail-oriented Mechanical Engineering graduate with strong background in computer-aided design, thermal systems, fluid dynamics analysis, and precision manufacturing techniques.",
                "skills": ["AutoCAD", "SolidWorks", "Thermodynamics", "CNC Machining", "FEA Analysis", "MATLAB"],
                "target_roles": ["Mechanical Engineer", "CAD Designer"],
                "projects": [
                    {
                        "name": "Aerodynamic Drag Reduction Study",
                        "details": "Modeled vehicle chassis dynamics in SolidWorks and conducted CFD simulations to optimize surface airflow, reducing aerodynamic drag coefficient by 12%.",
                    }
                ],
            },
        },
        {
            "filename": "devops_senior.pdf",
            "info": {
                "name": "Vikram Singh",
                "role": "Senior Site Reliability Engineer",
                "experience": "5 Years Experience",
                "email": "vikram.singh@example.com",
                "phone": "+91 99000 11223",
                "location": "Remote / Hyderabad, India",
                "summary": "Senior Site Reliability & DevOps Engineer with 5+ years of experience designing scalable cloud architecture, automating CI/CD infrastructure pipelines, and maintaining 99.99% system uptime.",
                "skills": ["AWS", "Docker", "Kubernetes", "Terraform", "CI/CD", "Prometheus", "Python", "Golang"],
                "target_roles": ["DevOps Engineer", "SRE", "Cloud Architect"],
                "experience_details": [
                    {
                        "title": "Senior SRE",
                        "company": "CloudScale Systems",
                        "duration": "2021 - Present",
                        "details": "Architected Kubernetes clusters across AWS multi-region deployments using Terraform. Reduced deployment rollback rates by 40% through automated canary testing pipelines.",
                    }
                ],
            },
        },
    ]

    for item in resumes:
        create_resume_pdf(item["filename"], item["info"])


if __name__ == "__main__":
    main()
