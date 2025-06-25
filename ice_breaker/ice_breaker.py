from typing import Tuple
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import person_intel_parser, PersonIntel
from third_parties.linkedin import scrape_linkedin_profile


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    """
    Generates a summary, facts, topics of interest, and ice breakers based only on LinkedIn profile data.
    """
    # Lookup LinkedIn profile
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    # Prompt template for LLM to generate conversation insights
    summary_template = """
    You are a professional conversation coach and expert in human profiling.
    Based on the following detailed LinkedIn information about a person, generate the following:
    1. A concise yet engaging professional summary (3-5 sentences) that highlights:
       - Their current role and company (if available)
       - Their key skills and areas of expertise
       - Notable achievements or projects
       - Any relevant certifications or educational background
    2. Two unique and interesting facts about them. These can be drawn from their skills, experience, education, achievements, or personal interests.
    3. Three specific topics that are likely to interest them, based on their work, background, hobbies, certifications, or areas of study.
    4. Two creative, natural-sounding ice breaker questions to start a conversation with them, personalized based on their background, interests, or achievements.

    Ensure the tone is friendly, professional, and suitable for networking or casual conversation.
    
    LinkedIn Information:
    {linkedin_information}

    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(linkedin_information=linkedin_data)
    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    result = ice_break(name="Tushar Chourse")  # Replace with any name to test
    print(result)
