from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Pokemon, pokemon_schema, pokemons_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/pokemon', methods = ['POST'])
@token_required
def create_pokemon(current_user_token):
    name = request.json['name']
    type = request.json['type']
    hp = request.json['hp']
    attack = request.json['attack']
    defense = request.json['defense']
    speed = request.json['speed']
    user_token = current_user_token.token

    print(f'Pokemon Token created: {current_user_token.token}')

    pokemon = Pokemon(name, type, hp, attack, defense, speed, user_token=user_token)

    db.session.add(pokemon)
    db.session.commit()

    response = pokemon_schema.dump(pokemon)
    return jsonify(response)

@api.route('/pokemon', methods = ['GET'])
@token_required
def get_pokemon(current_user_token):
    a_user = current_user_token.token
    all_pokemon = Pokemon.query.filter_by(user_token = a_user).all()
    response = pokemons_schema.dump(all_pokemon)
    return jsonify(response)

@api.route('/pokemon/<id>', methods = ['GET'])
@token_required
def getSinglePokemon(current_user_token, id):
    single_pokemon = Pokemon.query.get(id)
    response = pokemon_schema.dump(single_pokemon)
    return jsonify(response)

@api.route('/pokemon/<id>', methods = ['POST', 'PUT'])
@token_required
def update_pokemon(current_user_token, id):
    pokemon = Pokemon.query.get(id)
    pokemon.name = request.json['name']
    pokemon.type = request.json['type']
    pokemon.hp = request.json['hp']
    pokemon.attack = request.json['attack']
    pokemon.defense = request.json['defense']
    pokemon.speed = request.json['speed']
    pokemon.user_token = current_user_token.token

    db.session.commit()
    response = pokemon_schema.dump(pokemon)
    return jsonify(response)

@api.route('/pokemon/<id>', methods = ['DELETE'])
@token_required
def delete_pokemon(current_user_token, id):
    pokemon = Pokemon.query.get(id)
    db.session.delete(pokemon)
    db.session.commit()

    response = pokemon_schema.dump(pokemon)
    return jsonify(response)