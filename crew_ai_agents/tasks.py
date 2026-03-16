from crewai import Task
from tools import yt_tool
from agents import blog_writer, blog_researcher


# ---------------- RESEARCH TASK ---------------- #

research_task = Task(
    description=(
        "Identify the YouTube video related to the topic: {topic}. "
        "Extract detailed information about the video including the main ideas, "
        "key concepts discussed, and insights shared by the creator. "
        "Focus on understanding the core message and educational value of the video."
    ),

    expected_output=(
        "A comprehensive 3 paragraph report explaining the topic covered in the video, "
        "including the main concepts, important insights, and key takeaways."
    ),

    tools=[yt_tool],

    agent=blog_researcher,
)


# ---------------- WRITING TASK ---------------- #

write_task = Task(
    description=(
        "Using the research report provided, write a detailed and engaging blog post "
        "about the topic: {topic}. The blog should clearly explain the ideas from the video "
        "in a way that is easy to understand for readers."
    ),

    expected_output=(
        "A well-structured blog article with:\n"
        "- An engaging title\n"
        "- An introduction\n"
        "- Multiple informative sections\n"
        "- Bullet points for key takeaways\n"
        "- A short conclusion summarizing the topic\n\n"
        "The blog should be informative, clear, and around 500-700 words."
    ),

    agent=blog_writer,
)