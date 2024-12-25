from pyclarify import Client

client = Client("./ClarifyCredentials_Test_cl6vk0j8613mgkgeindg.json")

from pyclarify import Signal
# test


signal = Signal(
    name = "Home temperature",
    description = "Temperature in the bedroom",
    labels = {"data-source": ["Raspberry Pi"], "location": ["Home"]}
)

response = client.save_signals(
    input_ids=["INPUT_ID"],
    signals=[signal],
    create_only=False
)

from pyclarify import DataFrame

data = DataFrame(
    series={"INPUT_ID_1": [1, None], "INPUT_ID_2": [None, 5]},
    times = ["2021-11-01T21:50:06Z",  "2021-11-02T21:50:06Z"],
)

response = client.insert(data)

response = client.select_signals(
    skip=10,
    limit=50,
    sort=["-id"]
)

from pyclarify import Item

client = Client("./clarify-credentials.json")

item = Item(
    name = "Home temperature",
    description = "Temperature in the bedroom",
    labels = {"data-source": ["Raspberry Pi"], "location": ["Home"]},
    visible=True
)
response = client.publish_signals(
    signal_ids=['<SIGNAL_ID>'],
    items=[item],
    create_only=False
)

from pyclarify.query import Filter, Regex

only_raspberries = Filter(
    fields={
        "labels.unit-type": Regex(value="Raspberry")
    }
)

response = client.select_items(
    filter=only_raspberries
)

response = client.data_frame(
    filter=only_raspberries,
    include=["item"]
)