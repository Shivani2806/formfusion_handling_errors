from uagents import Context, Model, Protocol
from query import FormStatus, FormField
from typing import List, Dict, Any


class SubmitFormRequest(Model):
    title: str
    fields:  Dict[str, Any]


class SubmitFormResponse(Model):
    success: bool


submit_proto = Protocol()


@submit_proto.on_message(model=SubmitFormRequest, replies=SubmitFormResponse)
async def handle_submit_request(ctx: Context, sender: str, msg: SubmitFormRequest):
    forms = {
        num: FormStatus(**status)
        for num, status in ctx.storage._data.items()
        if status['title'] == msg.title
    }

    if not forms:
        await ctx.send(sender, SubmitFormResponse(success=False, error_message="Form not found."))
        return


    errors = []
    for field in forms.fields:
        field_name = field.name
        if field_name not in msg.fields:
            if field.required:
                errors.append(f"Field '{field_name}' is required.")
        else:
            field_value = msg.fields[field_name]
            if field.data_type == "str" and not isinstance(field_value, str):
                errors.append(f"Field '{field_name}' must be a string.")
            elif field.data_type == "int" and not isinstance(field_value, int):
                errors.append(f"Field '{field_name}' must be an integer.")
            elif field.data_type == "float" and not isinstance(field_value, float):
                errors.append(f"Field '{field_name}' must be a float.")

    if errors:
        await ctx.send(sender, SubmitFormResponse(success=False, error_message="; ".join(errors)))
        return

    # If validation passes
    await ctx.send(sender, SubmitFormResponse(success=True))
