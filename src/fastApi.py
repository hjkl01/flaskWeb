from fastapi import FastAPI

from apis.index import index
from apis.local_cmd import local_run
from apis.ssh_cmd import ssh_cmd
from apis.send_request import send_request
from apis.logstash_alarm import run as alarm
from apis.cron_device_conf import cron_device_conf, cron_command_id, crons
from apis.ssh_ping import ssh_ping
from apis._nmap import run as nmap
from apis.test_delete import test_delete
from apis.test_view import test_view
from apis.run_commands import ansible_cmd, ansible_filename
from apis.files import files
from apis.search import search

app = FastAPI()

app.add_api_route('/', index)
app.add_api_route("/cmd", ssh_cmd, methods=["POST"])
app.add_api_route("/local_cmd", local_run, methods=["POST"])
app.add_api_route('/nmap', send_request)
app.add_api_route('/device', cron_device_conf, methods=["POST"])
app.add_api_route("/elk", alarm, methods=["POST"])
app.add_api_route("/ping", ssh_ping, methods=["POST"])
app.add_api_route("/test_ping", nmap)
app.add_api_route("/test_delete", test_delete)
app.add_api_route("/test_view", test_view)
app.add_api_route("/cron/{command_id}", cron_command_id)
app.add_api_route("/crons/", crons)
app.add_api_route("/ansible_cmd/{f}", ansible_cmd)
app.add_api_route("/ansible/{f}", ansible_filename)
app.add_api_route("/files/", files, methods=["POST"])
app.add_api_route("/search/{path}/{word}/{_from}/{_to}", search)

# gunicorn test:app -w 4 -k uvicorn.workers.UvicornWorker


# app.add_api_route("/item/{item_id}", read_item)
# app.add_api_route("/items/", create_item, methods=['POST'])

# async def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
#
#
# from pydantic import BaseModel
# class Item(BaseModel):
#     name: str
#     # description: str = None
#     price: float
#     # tax: float = None
#
#
# # @app.post("/items/")
# async def create_item(item: Item):
#     logger.info(item)
#     return item
