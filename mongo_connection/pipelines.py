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
                "collectionName": 1,
                "sinopsys": {
                    "$substrCP": ["$sinopsys", 0, 3500]
                },
                "federalEstatal": 1,
                "state": 1,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                "urlAttach": {
                    "$cond": {
                        "if": {"$eq": ["$urlAttach", "na"]},
                        "then": [],
                        "else": {
                            "$cond": {
                                "if": {"$eq": ["$urlAttach", "N/A"]},
                                "then": [],
                                "else": {
                                    "$map": {
                                        "input": "$urlAttach",
                                        "as": "attachment",
                                        "in": {
                                            "urlAttach": "$$attachment.urlAttach",
                                            "sinopsys": {
                                                "$substrCP": ["$$attachment.sinopsys", 0, 3500]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
            }
        }
    ]
    return pipeline


def get_pipeline_pdf_optimized(query: dict) -> list[dict]:
    pipeline = [
        {
            "$match": query
        },
        {
            "$project": {
                "title": 1,
                "urlPage": 1,
                "collectionName": 1,
                "sinopsys": {
                    "$substrCP": ["$sinopsys", 0, 3500]
                },
                "federalEstatal": 1,
                "state": 1,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                "urlAttach": {
                    "$cond": {
                        "if": {"$eq": ["$urlAttach", "na"]},
                        "then": [],
                        "else": {
                            "$cond": {
                                "if": {"$eq": ["$urlAttach", "N/A"]},
                                "then": [],
                                "else": {
                                    "$map": {
                                        "input": "$urlAttach",
                                        "as": "attachment",
                                        "in": {
                                            "urlAttach": "$$attachment.urlAttach",
                                            "sinopsys": {
                                                "$substrCP": ["$$attachment.sinopsys", 0, 3500]
                                            }
                                        }
                                    }
                                }
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
                    "$substrCP": ["$sinopsys", 0, 3500]
                },
                "urlAttach": {
                    "$cond": {
                        "if": {"$eq": ["$urlAttach", "na"]},
                        "then": [],
                        "else": {
                            "$cond": {
                                "if": {"$eq": ["$urlAttach", "N/A"]},
                                "then": [],
                                "else": {
                                    "$map": {
                                        "input": "$urlAttach",
                                        "as": "attachment",
                                        "in": {
                                            "urlAttach": "$$attachment.urlAttach",
                                            "sinopsys": {
                                                "$substrCP": ["$$attachment.sinopsys", 0, 3500]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
            }
        }
    ]
    return pipeline


def get_base64_urlAttach_from_dof_collection(id: ObjectId):
    pipeline = [
        {
            "$match": {"_id": id}
        },
        {
            "$project": {
                "urlAttach": {
                    "$cond": {
                        "if": {"$eq": ["$urlAttach", "na"]},
                        "then": [],
                        "else": {
                            "$cond": {
                                "if": {"$eq": ["$urlAttach", "N/A"]},
                                "then": [],
                                "else": {
                                    "$map": {
                                        "input": "$urlAttach",
                                        "as": "attachment",
                                        "in": {
                                            "urlAttach": "$$attachment.urlAttach",
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
            }
        }
    ]
    return pipeline


def get_sinopsys_of_urlAttach_from_dof_collection(id: ObjectId):
    pipeline = [
        {
            "$match": {"_id": id}
        },
        {
            "$project": {
                "urlAttach": {
                    "$cond": {
                        "if": {"$eq": ["$urlAttach", "na"]},
                        "then": [],
                        "else": {
                            "$cond": {
                                "if": {"$eq": ["$urlAttach", "N/A"]},
                                "then": [],
                                "else": {
                                    "$map": {
                                        "input": "$urlAttach",
                                        "as": "attachment",
                                        "in": {
                                            "sinopsys": {
                                                "$substrCP": ["$$attachment.sinopsys", 0, 3500]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
            }
        }
    ]
    return pipeline
