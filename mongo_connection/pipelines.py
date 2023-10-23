from bson import ObjectId
def get_pipeline_pdf(id: ObjectId):
    pipeline = [
        {
            "$match": {"_id": id}
        },
        {
            "$project": {
                "title": 1,
                "urlPage": 1,
                "sinopsys": {
                    "$substrCP": ["$sinopsys", 0, 20341]
                },
                "federalEstatal": 1,
                "state": 1,
                "date": 1,
                "urlAttach": {
                    "$map": {
                        "input": "$urlAttach",
                        "as": "attachment",
                        "in": {
                            "urlAttach": "$$attachment.urlAttach",
                            "sinopsys": {
                                "$substrCP": ["$$attachment.sinopsys", 0, 20341]
                            }
                        }
                    }
                },
            }
        }
    ]
    return pipeline

def get_sinopsys_and_urlAttach(id: ObjectId):
    pipeline = [
        {
            "$match": {"_id": id}
        },
        {
            "$project": {
                "sinopsys": {
                    "$substrCP": ["$sinopsys", 0, 20341]
                },
                "urlAttach": {
                    "$map": {
                        "input": "$urlAttach",
                        "as": "attachment",
                        "in": {
                            "urlAttach": "$$attachment.urlAttach",
                            "sinopsys": {
                                "$substrCP": ["$$attachment.sinopsys", 0, 20341]
                            }
                        }
                    }
                },
            }
        }
    ]
    return pipeline
