from submission import SubmitFormRequest, SubmitFormResponse
from query import (
    QueryFormRequest,
    QueryFormResponse,
)
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

ORGANISATION_ADDRESS = "agent1qv7ztxd9cgc8g9jlyenkptw3t63g0h2pjmqaz4qu3q5jn37m5kkvj93d5js"

user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(user.wallet.address())

Form_query = QueryFormRequest(
    body="",

    title="Internship Session",

)
