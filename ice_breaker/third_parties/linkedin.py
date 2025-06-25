import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles using Proxycurl API"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/tchourse/d20d7be5f1dd8f757c4f168e01fa7c30/raw/7504afb4221c8ca00075fddc0932b6feb37a2dc5/tushar-chourse.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
        data = response.json()
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers = {
            "Authorization": f'Bearer {os.environ["PROXYCURL_API_KEY"]}'
        }
        params = {
            "url": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            headers=headers,
            params=params,
            timeout=10,
        )
        data = response.json()

    # Clean up data
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    # Remove profile_pic_url from groups if 'groups' key exists
    if "groups" in data:
        for group_dict in data["groups"]:
            group_dict.pop("profile_pic_url", None)

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/tusharchourse/",
            mock=True
        )
    )
