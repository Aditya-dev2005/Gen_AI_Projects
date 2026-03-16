from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task
from dotenv import load_dotenv
load_dotenv()


# ---------------- CREATE CREW ---------------- #

crew = Crew(
    agents=[blog_researcher, blog_writer],

    tasks=[research_task, write_task],

    process=Process.sequential,

    memory=True,
    cache=True,

    max_rpm=100,
)


# ---------------- START EXECUTION ---------------- #

if __name__ == "__main__":

    result = crew.kickoff(
        inputs={"topic": "AI vs ML vs DL vs Data Science"}
    )

    print("\n\n===== FINAL BLOG OUTPUT =====\n")
    print(result)