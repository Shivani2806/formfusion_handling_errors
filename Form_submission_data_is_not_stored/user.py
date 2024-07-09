from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from models import QueryFormRequest, SubmitFormRequest

ORGANISATION_ADDRESS = "agent1qw50wcs4nd723ya9j8mwxglnhs2kzzhh0et0yl34vr75hualsyqvqdzl990"

user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(str(user.wallet.address()))

Form_query = QueryFormRequest(
    body="UGAC",
    title="Internship Session",
)

EXPECTED_FIELDS = {
    "Name": "John Doe",
    "Email": "john.doe@example.com",
    "Phone": "1234567890",
    "Resume": "link_to_resume.pdf"
}

@user.on_interval(period=5.0, messages=QueryFormRequest)
async def interval(ctx: Context):
    completed = ctx.storage.get("completed")

    if not completed:
        await ctx.send(ORGANISATION_ADDRESS, Form_query)
        ctx.logger.info("Form query sent.")

@user.on_interval(period=10.0, messages=SubmitFormRequest)
async def submit_form(ctx: Context):
    if not ctx.storage.get("completed"):
        form_submission = SubmitFormRequest(title="Internship Session", fields=EXPECTED_FIELDS)
        await ctx.send(ORGANISATION_ADDRESS, form_submission)
        ctx.logger.info("Form submission sent.")

if __name__ == "__main__":
    user.run()
