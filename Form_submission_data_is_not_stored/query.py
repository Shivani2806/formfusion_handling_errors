from typing import Any, Dict, List, Optional
from uagents import Context, Model, Protocol

class FormField(Model):
    name: str
    required: bool
    data_type: str  # e.g., "str", "int", "float", etc.

class FormStatus(Model):
    body: str
    title: str
    description: str
    fields: List[FormField]  # Use FormField model

class QueryFormRequest(Model):
    body: str
    title: str

class QueryFormResponse(Model):
    forms: Optional[FormStatus] = None

class GetTotalQueries(Model):
    pass

class TotalQueries(Model):
    total_queries: int

query_proto = Protocol()

class SubmitFormRequest(Model):
    title: str
    fields: Dict[str, Any]  # Map field names to their values

class SubmitFormResponse(Model):
    success: bool
    error_message: Optional[str] = None  # Add error_message field

submit_proto = Protocol()

class SubmissionData(Model):
    title: str
    fields: Dict[str, Any]
query_proto = Protocol()


@query_proto.on_message(model=QueryFormRequest, replies=QueryFormResponse)
async def handle_query_request(ctx: Context, sender: str, msg: QueryFormRequest):
    form = next(
        (FormStatus(**status) for num, status in ctx.storage._data.items()
         if isinstance(num, int) and status['title'] == msg.title),
        None
    )

    if form:
        ctx.logger.info(f"Hi! Here's the form you were requesting for: {form}")
    else:
        ctx.logger.info(f"Form with title '{msg.title}' not found. ")

    await ctx.send(sender, QueryFormResponse(forms=form))

    total_queries = int(ctx.storage.get("total_queries") or 0)
    ctx.storage.set("total_queries", total_queries + 1)


@query_proto.on_query(model=GetTotalQueries, replies=TotalQueries)
async def handle_get_total_queries(ctx: Context, sender: str, _msg: GetTotalQueries):
    total_queries = int(ctx.storage.get("total_queries") or 0)
    await ctx.send(sender, TotalQueries(total_queries=total_queries))
