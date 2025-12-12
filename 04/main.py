from flask import Flask
from flask_restful import Api, Resource
import requests


app = Flask(__name__)

api = Api(app)


class StatusResource(Resource):
    def get(self):
        return {
            "status": "live"
        }


class PokemonByNameResource(Resource):
    def get(self, name):
        raw = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
        data = raw.json()
        return {
            "name": name,
            "experience": data["base_experience"],
            "height": "",
            "weight":"",
            "moves": ""
        }


api.add_resource(StatusResource, "/status/")
api.add_resource(PokemonByNameResource, "/pokemon/<name>")
