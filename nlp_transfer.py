from openai import OpenAI

API_KEY = "Your_API_key"
PROJECT_ID = "Your_project_id"
ORGANIZATION_ID = "Your_organization_id"

client = OpenAI(
    api_key=API_KEY,
    project=PROJECT_ID,
    organization=ORGANIZATION_ID
)

def generate_mongodb_query(user_input):
    prompt = f"""
You are an expert MongoDB query generator for the 'pokemon_market' database.

Database Schema:
---

1. card_informations
- _id, id, name, subtypes, hp, types, attacks, weaknesses, artist, nationalPokedexNumbers, rarity, set_id

Example document:
{{
  _id: ObjectId('68056cbdf55f45963e2308a2'),
  id: 'swsh8-1',
  name: 'Caterpie',
  subtypes: [ 'Basic' ],
  hp: 50,
  types: [ 'Grass' ],
  attacks: [
    {{
      name: 'Flock',
      cost: [ 'Colorless' ],
      convertedEnergyCost: 1,
      damage: '',
      text: 'Search your deck for a Caterpie and put it onto your Bench. Then, shuffle your deck.'
    }},
    {{
      name: 'Bug Bite',
      cost: [ 'Grass' ],
      convertedEnergyCost: 1,
      damage: '10',
      text: ''
    }}
  ],
  weaknesses: [ {{ type: 'Fire', value: '×2' }} ],
  artist: 'Mitsuhiro Arita',
  rarity: 'Common',
  nationalPokedexNumbers: [ 10 ],
  set_id: 'swsh8'
}}


---

2. card_price
- name, set_id, price, title

Example document:
{{
  title: '2x Caterpie',
  price: '1.00',
  name: 'Caterpie',
  set_id: 'swsh8'
}}

---

3. card_sets
- id
- name
- series
- releaseDate
- legalities
- total
- generation

Example document:
{{
  id: 'base1',
  name: 'Base',
  series: 'Base',
  total: 102,
  releaseDate: '1999/01/09',
  generation: 'Generation 1'
}}

---

4. deck_cards
- _id, deck_id, id, name, rarity, count

Example document:
{{
  _id: ObjectId('6806b267902b61f198d11d04'),
  deck_id: 'd-bw10-1',
  id: 'bw10-10',
  name: 'Genesect',
  rarity: 'Rare Holo',
  count: 1
}}

---

5. pokemon_decks
- id, name, types

Example document:
{{
  id: 'd-bw10-1',
  name: 'Mind Wipe',
  types: ['Grass', 'Psychic']
}}

---

6. pokemon_game
- game_id, title_japanese, title_english, release_date_japan, generation, generation_short, platform, starter_pokemon, legendary_pokemon, mythical_pokemon, main_character

Example document:
{{
  _id: ObjectId('6806ad75902b61f198d11bf5'),
  game_id: 1,
  title_japanese: 'ポケットモンスター 赤・緑',
  title_english: 'Pokémon Red and Green',
  release_date_japan: '1996-02-27',
  generation: 'Generation 1',
  generation_short: 'base',
  platform: 'Game Boy',
  starter_pokemon: [ 'Charmander', 'Squirtle', 'Bulbasaur' ],
  legendary_pokemon: [ 'Articuno', 'Zapdos', 'Moltres', 'Mewtwo' ],
  mythical_pokemon: [ 'Mew' ],
  main_character: [ 'Red', 'Blue' ]
}}

---

7. pokemon_movies
- movie_id, japanese_title, english_title, release_date_japan, generation, generation_short, featured_pokemon

Example document:
{{
  _id: ObjectId('6806ae12902b61f198d11c30'),
  movie_id: 1,
  japanese_title: 'ミュウツーの逆襲',
  english_title: 'Pokémon: The First Movie - Mewtwo Strikes Back',
  release_date_japan: '1998-07-18',
  generation: 'Generation 1',
  generation_short: 'base',
  featured_pokemon: [ 'Mewtwo', 'Mew' ]
}}

---

8. pokemon_information
- id, name, type, base, volutions

Example document:
{{
  _id: ObjectId('6806bd8b902b61f198d12c8d'),
  id: 1,
  name: 'Bulbasaur',
  type: [ 'Grass', 'Poison' ],
  base: {{
    HP: 45,
    Attack: 49,
    Defense: 49,
    'Sp. Attack': 65,
    'Sp. Defense': 65,
    Speed: 45
  }},
  evolution: {{ next: [ [ '2', 'Level 16' ] ] }}
}}

---

Important Relationships (Join Rules):

- card_informations.name = card_price.name
- card_informations.set_id = card_sets.id
- card_price.set_id = card_sets.id  
- card_price is the relational table for card_informations and card_sets

- deck_cards.deck_id = pokemon_decks.id
- deck_cards.name = card_informations.name  
- deck_cards is the relational table for card_informations and pokemon_decks

- pokemon_game.generation = pokemon_movies.generation = card_sets.generation
- pokemon_game <=> pokemon_movies: many-to-many
- pokemon_movies <=> card_sets: many-to-many

- pokemon_information.name = card_informations.name = deck_cards.name  
- pokemon_information => card_informations: one-to-many

---

Query Output Format:
Depending on user intent, output one of the following JSON formats:

1. Find (simple query):
{{
  "collection": "collection_name",
  "operation": "find",
  "filter": {{ }},
  "projection": {{ }} (optional),
  "sort": {{ }} (optional),
  "limit": int (optional),
  "skip": int (optional)
}}

2. General Format for Aggregation (complex query):
{{
  "collection": "collection_name",
  "operation": "aggregate",
  "pipeline": [{{ }}, {{ }}]
}}

3. Insert:
{{
  "collection": "collection_name",
  "operation": "insert",
  "document": {{ }}
}}

4. Update:
{{
  "collection": "collection_name",
  "operation": "update",
  "filter": {{ }},
  "update": {{ }}
}}

5. Delete:
{{
  "collection": "collection_name",
  "operation": "delete",
  "filter": {{ }}
}}

6. Specific Join AGGREGATE:
{{
  "collection": "card_informations",
  "operation": "aggregate",
  "pipeline": [
    {{ "$match": {{ "types": "Grass" }} }},
    {{ "$lookup": {{
      "from": "card_price",
      "localField": "name",
      "foreignField": "name",
      "as": "price_info"
    }} }},
    {{ "$unwind": "$price_info" }},
    {{ "$project": {{ "name": 1, "hp": 1, "price": "$price_info.price" }} }}
  ]
}}

Rules:
- When querying the card_informations collection, always include the "id" field (the custom Pokémon card ID, not "_id") in the output projection.
- Always infer the correct collection(s) based on user intent and keywords (e.g., price + hp → card_informations + card_price).
- If multiple collections are involved, use `$lookup`.
- For joining card_informations and card_price, always match using both `name` and `set_id`, not just `name`.
- Use $lookup with $expr and a pipeline to match multiple fields (e.g., name and set_id) when joining.
- If the `$lookup` result (e.g., `price_info`) contains multiple documents, apply `$unwind` to extract the first match.
- When filtering prices, convert string prices like "$1.00" to numerical values before using `$lt`, `$gt`, etc.
- For "operation": "update", do not use $set. Just include the updated fields directly like this
- Do not use $set, $inc, or any other operator in "update" — treat it as a replacement document with updated fields only.
- For insert operations:
  - If inserting a single document, use `"operation": "insert"` and `"document": { ... }`
  - If inserting multiple documents, use `"operation": "insert_many"` and `"documents": [ ... ]`
- When both positive (e.g., "Fire-type") and negative (e.g., "not Wind-type") conditions are mentioned, combine them using `$all` or direct match with `$nin`.
- This applies to any field — types, rarity, platform, generation, etc.
- For array fields (e.g., `"types"`), use `$unwind` before applying `$group`, `$count`, or `$project`.
- If the user's query involves counting (e.g., "how many"), prefer using:
  - `find` + result length for simple filters,
  - or `$count` within aggregation if a cleaner result is needed.
- Do not return full documents when only count is asked — return just the count.
- Only output a valid JSON query. No explanations. No comments.

User Query: {user_input}

MongoDB Query:
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for generating MongoDB queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,  
        max_tokens=800,   
    )

    mongo_query = response.choices[0].message.content.strip()
    return mongo_query
