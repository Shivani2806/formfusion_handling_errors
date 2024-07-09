from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from models import query_proto, submit_proto, FormStatus, FormField, SubmissionData

organisation = Agent(
    name="organisation",
    port=8001,
    seed="org secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(str(organisation.wallet.address()))

organisation.include(query_proto)
organisation.include(submit_proto)

FORMS = {
    1: FormStatus(
        body="This is an internship application form",
        title="Internship Session",
        description="Form to apply for internship",
        fields=[
            FormField(name="Name", required=True, data_type="str").dict(),
            FormField(name="Email", required=True, data_type="str").dict(),
            FormField(name="Phone", required=True, data_type="str").dict(),
            FormField(name="Resume", required=True, data_type="str").dict()
        ]
    ).dict()
}

for (number, status) in FORMS.items():
    organisation._storage.set(number, status)
    organisation.logger.info(f"Form {number} set with status: {status}")

@submit_proto.on_message(model=SubmitFormRequest, replies=SubmitFormResponse)
async def handle_submit_request(ctx: Context, sender: str, msg: SubmitFormRequest):
    # Retrieve the form based on the title
    form = next(
        (FormStatus(**status) for num, status in ctx.storage._data.items()
         if isinstance(num, int) and status['title'] == msg.title),
        None
    )

    if not form:
        await ctx.send(sender, SubmitFormResponse(success=False, error_message="Form not found."))
        return

    # Validate the fields
    errors = []
    for field in form.fields:
        field_name = field['name']
        if field_name not in msg.fields:
            if field['required']:
                errors.append(f"Field '{field_name}' is required.")
        else:
            field_value = msg.fields[field_name]
            if field['data_type'] == "str" and not isinstance(field_value, str):
                errors.append(f"Field '{field_name}' must be a string.")
            elif field['data_type'] == "int" and not isinstance(field_value, int):
                errors.append(f"Field '{field_name}' must be an integer.")
            elif field['data_type'] == "float" and not isinstance(field_value, float):
                errors.append(f"Field '{field_name}' must be a float.")

    if errors:
        await ctx.send(sender, SubmitFormResponse(success=False, error_message="; ".join(errors)))
        return

    # Persist the submitted data
    submission_data = SubmissionData(title=msg.title, fields=msg.fields).dict()
    existing_submissions = ctx.storage.get("submissions", [])
    existing_submissions.append(submission_data)
    ctx.storage.set("submissions", existing_submissions)
    
    ctx.logger.info(f"Form submission stored: {submission_data}")

    # Send success response
    await ctx.send(sender, SubmitFormResponse(success=True))

if __name__ == "__main__":
    organisation.run()
