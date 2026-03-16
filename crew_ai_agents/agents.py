from dotenv import load_dotenv
load_dotenv()  # must be first

import os
os.environ["OPENAI_MODEL_NAME"] = "gpt-4-0125-preview"

from crewai import Agent
from tools import yt_tool
from crewai import Agent
from tools import yt_tool


# ---------------- BLOG RESEARCHER AGENT ---------------- #

blog_researcher = Agent(
    role="Blog Researcher from YouTube Videos",

    goal="Get the relevant video content for the topic {topic} from YouTube channels",

    verbose=True,
    memory=True,

    backstory=(
        "You are an expert in understanding technical videos related to "
        "Artificial Intelligence, Data Science, Machine Learning, and "
        "Generative AI. Your job is to extract meaningful insights from "
        "YouTube videos and gather valuable research information that "
        "can later be used to create high quality blog content."
    ),

    tools=[yt_tool],

    allow_delegation=True
)


# ---------------- BLOG WRITER AGENT ---------------- #

blog_writer = Agent(
    role="Tech Blog Writer",

    goal="Write engaging and insightful tech blogs based on the topic {topic} using the researched video content",

    verbose=True,
    memory=True,

    backstory=(
        "You are a professional technology blog writer who specializes in "
        "turning complex technical concepts into simple and engaging stories. "
        "You write blogs about AI, Machine Learning, Data Science, and "
        "Generative AI in a way that is easy to understand for readers while "
        "keeping the content informative and engaging."
    ),

    tools=[],

    allow_delegation=True
)