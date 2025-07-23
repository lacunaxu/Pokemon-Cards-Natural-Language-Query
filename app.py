# app.py

from mongodb import MongoDBHandler
from nlp_transfer import generate_mongodb_query
import json

def execute_query(mongo_handler, mongo_query: dict):
    operation = mongo_query["operation"]
    collection_name = mongo_query["collection"]

    if operation == "find":
        return mongo_handler.find(
            collection_name=collection_name,
            filter_query=mongo_query.get("filter", {}),
            projection=mongo_query.get("projection"),
            sort=mongo_query.get("sort"),
            limit=mongo_query.get("limit"),
            skip=mongo_query.get("skip")
        )

    elif operation == "aggregate":
        return mongo_handler.aggregate(
            collection_name=collection_name,
            pipeline=mongo_query["pipeline"]
        )

    elif operation == "insert":
        inserted_id = mongo_handler.insert_one(
            collection_name=collection_name,
            document=mongo_query["document"]
        )
        print(f"Successful insert, and the result is：{inserted_id}")
        latest_docs = mongo_handler.find(
            collection_name=collection_name,
            filter_query={},
            sort={"_id": -1},
            limit=3
        )
        return latest_docs

    elif operation == "insert_many":
        inserted_ids = mongo_handler.insert_many(
            collection_name=collection_name,
            documents=mongo_query["documents"]
        )
        print(f"Successful insert {len(inserted_ids)} results")
        latest_docs = mongo_handler.find(
            collection_name=collection_name,
            filter_query={},
            sort={"_id": -1},
            limit=3
        )
        return latest_docs

    elif operation == "update":
        modified_count = mongo_handler.update_one(
            collection_name=collection_name,
            filter_query=mongo_query["filter"],
            update_values=mongo_query["update"]
        )
        print(f"Successful update {modified_count} results")
        updated_doc = mongo_handler.find(
            collection_name=collection_name,
            filter_query=mongo_query["filter"],
            limit=1
        )
        return updated_doc

    elif operation == "delete":
        deleted_target = mongo_handler.find(
            collection_name=collection_name,
            filter_query=mongo_query["filter"],
            limit=1
        )
        deleted_count = mongo_handler.delete_one(
            collection_name=collection_name,
            filter_query=mongo_query["filter"]
        )
        print(f"Successful delete {deleted_count} results")

        if deleted_target:
            deleted_doc = deleted_target[0]
            deleted_id = deleted_doc["_id"]

            neighbors = mongo_handler.find(
                collection_name=collection_name,
                filter_query={"_id": {"$gt": deleted_id}},
                sort={"_id": 1},
                limit=1
            ) + mongo_handler.find(
                collection_name=collection_name,
                filter_query={"_id": {"$lt": deleted_id}},
                sort={"_id": -1},
                limit=1
            )
            return neighbors
        else:
            return []

    else:
        return "Unsupported operation."


def main():
    print("Welcome to the Pokémon Market Natural Language Query System. ^V^ ")
    print("Enter an English natural language question and type 'exit' to exit the program.")

    mongo_handler = MongoDBHandler()

    while True:
        user_input = input("\n Please enter your natural language query: ").strip()
        if not user_input:
            continue 


        if user_input.lower() == "exit":
            print("You have successfully exited the program!!")
            print("goodbye!!")
            break

        try:
            mongo_query_text = generate_mongodb_query(user_input)
            mongo_query = json.loads(mongo_query_text) 

            print("\nGenerated MongoDB query:")
            print(json.dumps(mongo_query, indent=2, ensure_ascii=False))

            result = execute_query(mongo_handler, mongo_query)

            print("\nMongoDB query results:")
            if isinstance(result, list):
                if not result:
                    print("The result is empty")
                else:
                    for idx, doc in enumerate(result):
                        if idx >= 3:
                            break
                        if '_id' in doc:
                            doc['_id'] = str(doc['_id'])
                        print(json.dumps(doc, indent=2, ensure_ascii=False))

                    print(f"\nWe have total {len(result)} results")
            else:
                print(result)

        except Exception as e:
            print(f"Error: {e}")

    mongo_handler.close()

if __name__ == "__main__":
    main()

