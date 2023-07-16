from fastapi import FastAPI, HTTPException
import uvicorn
import json


app = FastAPI()


@app.get("/")
async def index():
    data = {
        "mantainer": "Diki Hamdani",
        "github": "https://github.com/Dikihmd01/",
        "endpoint": {
            "ms": {
                "all": "/bwf-rank/api/ms",
                "detail_by_rank": "/bwf-rank/api/ms/1",
            },
            "ws": {
                "all": "/bwf-rank/api/ws",
                "detail_by_rank": "/bwf-rank/api/ws/1",
            },
            "md": {
                "all": "/bwf-rank/api/md",
                "detail_by_rank": "/bwf-rank/api/md/1",
            },
            "wd": {
                "all": "/bwf-rank/api/ms",
                "detail_by_rank": "/bwf-rank/api/ms/1",
            },
            "xd": {
                "all": "/bwf-rank/api/ms",
                "detail_by_rank": "/bwf-rank/api/ms/1",
            },
        },
    }

    return data


def load_file(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)

    return data


@app.get("/bwf-rank/api/{category}")
async def get_rank(category):
    rank = load_file(f"./data/bwf-rank-{category}.json")

    return rank


@app.get("/bwf-rank/api/{category}/{rank}")
async def get_detail_rank(category, rank):
    data = load_file(f"./data/bwf-rank-{category}")
    filtered_data = [player for player in data if player["rank"] == rank]

    if not filtered_data:
        raise HTTPException(
            status_code=404, detail="No players found with the given rank"
        )

    return filtered_data
