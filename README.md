# ChatDB 74 - Pokémon Market Natural Language Query System

This project is a natural language interface built on top of a MongoDB database that allows users to query Pokémon card data using English. It uses OpenAI's GPT-3.5 to translate natural language into MongoDB queries, covering find, aggregate, insert, update, and delete operations.

---

## Project Structure

- `app.py` – Main controller that handles user input/output
- `nlp_transfer.py` – Generates structured queries using OpenAI GPT based on a custom prompt
- `mongodb.py` – Executes MongoDB operations using PyMongo
- `data_upload.ipynb` – Loads, cleans, and inserts Pokémon data into MongoDB
- `requirements.txt` – Python dependencies
- `README.md` – This guide
- `sample_data.json` – Sample top-5 rows from each collection
- `exported_full_data/` – Full data in JSON format
- `Sample Output/` – Screenshots of demo queries and results

---

## Dataset Collections

- `card_informations`
- `card_price`
- `card_sets`
- `deck_cards`
- `pokemon_decks`
- `pokemon_game`
- `pokemon_movies`
- `pokemon_information`

## How to Load the Data

The `data_upload.ipynb` notebook documents how the original datasets were cleaned and inserted into MongoDB. It shows the full data preparation process, but **it is not intended to be re-run for importing**.

To load the data into MongoDB for use with the system, use the `.json` files inside the `exported_full_data/` folder. Each file corresponds to one collection and can be imported using MongoDB tools such as:

```bash
mongoimport --db pokemon --collection card_informations --file exported_full_data/card_informations.json --jsonArray
```

Repeat this command for each collection by updating the collection name and file path.

---

## How to Run

1. **Clone the project or download from Google Drive**
   - [Google Drive Link](https://drive.google.com/drive/folders/1REMPq-IA7pmZ4wyQKgA-MygrNEzKkPUX?usp=drive_link)

2. **Start your MongoDB server**
   Make sure MongoDB is running on `localhost:27017`

3. **Install required libraries**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your OpenAI API key**
   - In `nlp_transfer.py`, replace the placeholder with your API credentials:
     ```python
     openai.api_key = "YOUR_API_KEY"
     openai.organization = "YOUR_ORG_ID"
     ```

5. **Run the app**
   ```bash
   python app.py
   ```

---

## Prerequisites

- Python 3.8 or above
- MongoDB installed and running (e.g., `mongod --dbpath ~/mongodb-data`)
- OpenAI account with valid API key

---

## API Key Notice

API key, project ID, and organization ID **have been removed** from the code.  
Please insert your personal OpenAI API credentials manually in `nlp_transfer.py`.

---

## Included Artifacts

- `README.md` – This file
- `requirements.txt` – Python dependencies
- `Dsci-551 presentation.pdf` – Demo slides
- `Sample Output/` – Folders with screenshots
- `exported_full_data/` – 8 full collection JSON files
- `sample_data.json` – Sample data output
- `.py` and `.ipynb` source files


## Test Commands

You can test queries such as:
- "Find all Pokémon cards with HP over 100"
- "Insert a new card called Testchu"
- "Show the price of Charizard"
- "How many movies were released in Generation 1?"

---

## Contact

This project was developed independently by a graduate student for DSCI-551. For questions or demo, please refer to the attached presentation or leave a comment in the classroom portal.
