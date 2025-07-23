from pymongo import MongoClient
from typing import List, Dict, Any

class MongoDBHandler:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "pokemon_market_copy"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def find(self, collection_name: str, filter_query: Dict[str, Any], projection: Dict[str, int] = None, sort: Dict[str, int] = None, limit: int = None, skip: int = None) -> List[Dict[str, Any]]:
        collection = self.db[collection_name]
        cursor = collection.find(filter_query, projection)
        if sort:
            cursor = cursor.sort(list(sort.items()))
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    def aggregate(self, collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        collection = self.db[collection_name]
        return list(collection.aggregate(pipeline))

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        collection = self.db[collection_name]
        result = collection.insert_many(documents)
        return [str(inserted_id) for inserted_id in result.inserted_ids]

    def update_one(self, collection_name: str, filter_query: Dict[str, Any], update_values: Dict[str, Any]) -> int:
        collection = self.db[collection_name]
        result = collection.update_one(filter_query, {"$set": update_values})
        return result.modified_count

    def delete_one(self, collection_name: str, filter_query: Dict[str, Any]) -> int:
        collection = self.db[collection_name]
        result = collection.delete_one(filter_query)
        return result.deleted_count

    def close(self):
        self.client.close()
