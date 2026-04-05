from tools.calculator import calculator, DESCRIPTION as CALC_DESC
from tools.weather import weather, DESCRIPTION as WEATHER_DESC
from tools.web_search import web_search, DESCRIPTION as SEARCH_DESC
from tools.wikipedia_tool import wikipedia_search, DESCRIPTION as WIKI_DESC

TOOLS = {
    "calculator": calculator,
    "weather": weather,
    "web_search": web_search,
    "wikipedia": wikipedia_search,
}

TOOLS_DESCRIPTION = "\n\n".join([CALC_DESC, WEATHER_DESC, SEARCH_DESC, WIKI_DESC])

def get_tool(name: str):
    return TOOLS.get(name)