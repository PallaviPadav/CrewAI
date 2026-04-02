from crewai import Crew, Agent, Task, LLM
from crewai_tools import SerperDevTool
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')


def generate_news(topic, temp):
    search_tool = SerperDevTool()

    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        max_tokens=300,
        temperature= temp
    )

    agent_news = Agent(
        goal=f"You are a news provider who gives both International and domestic news on {topic} from reliable web source",
        role="Breaking News Reporter",
        backstory=(
            "You are an authentic breaking news provider with web search skills. "
            "You excel in finding international, national, and local news. "
            f"You update the user with at least 10 news points for {topic} each points containing summary. "
            "You give a summary of news in three to four sentences for each point. "
            "Provide citations or sources for every news."
        ),
        llm=llm,
        tools=[search_tool],
    )

    task_news_creation = Task(
        description=f"""
        1. Do extensive web search on {topic} including:
            - Recent happenings and news
            - Provide more than 5 points
            - Each point should conatin brief summary.
            - Viewpoints of locals, experts, etc.
            - Government and political responses

        2. Include all relevant citations, sources and date of the news.
        """,
        expected_output="""
        A detailed breaking news containing:
        - Provide more than five breaking news 
        - Headlines with date and place
        - Summary of key findings
        - Analysis of current affairs
        - Verified facts and statistics
        - Citations and source links
        - Clear sections and bullet points
        """,
        agent=agent_news
    )

    crew = Crew(
        tasks=[task_news_creation],
        agents=[agent_news],
        verbose=True
    )

    result = crew.kickoff(inputs={"topic": topic})

    # Save to markdown
    filename = f"Breaking_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    content = result.raw if hasattr(result, "raw") else result

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return content, filename