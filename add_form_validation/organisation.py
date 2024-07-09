from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from submission import submit_proto
from query import query_proto, FormStatus, FormField

organisation = Agent(
    name="organisation",
    port=8001,
    seed="org secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(organisation.wallet.address())

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

# organisation.include(query_proto)
# organisation.include(submit_proto)
print(organisation.address)


for (number, status) in FORMS.items():
    organisation._storage.set(number, status)

if __name__ == "__main__":
    organisation.run()
