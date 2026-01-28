from fastapi import FastAPI, UploadFile, File
import shutil
import joblib
import os
import tempfile

from app.analyzer import SportsAnalyzer
from app.schemas import PlayerInput, InjuryInput
from fastapi.responses import FileResponse

app = FastAPI(title="Sports Analytics API")

analyzer = SportsAnalyzer("data/Footballer.csv")

# Train once (or skip if already trained)
if not os.path.exists("models/overall_model.pkl"):
    analyzer.train_and_save_models()

analyzer.overall_model = joblib.load("models/overall_model.pkl")
analyzer.value_model = joblib.load("models/value_model.pkl")


@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.post("/predict")
def predict_player(data: PlayerInput):
    features = [
        data.age, data.potential, data.stamina,
        data.strength, data.sprint_speed,
        data.work_rate_encoded
    ]

    overall, value = analyzer.predict(features)
    return {
    "predicted_overall": float(round(overall, 2)),
    "predicted_value_eur": float(round(value, 2))
}

    
    # return {
    #     "predicted_overall": round(overall, 2),
    #     "predicted_value_eur": round(value, 2)
    # }


@app.post("/injury-risk")
def injury_risk(data: InjuryInput):
    return {
        "injury_risk": analyzer.assess_injury_risk(
            data.age, data.stamina, data.work_rate
        )
    }


# @app.post("/process-video")
# def process_video(file: UploadFile = File(...)):
#     input_path = f"/tmp/{file.filename}"
#     output_path = f"/tmp/processed_{file.filename}"

#     with open(input_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     analyzer.process_video(input_path, output_path)
#     return {"output_video": output_path}

# @app.post("/process-video")
# def process_video(file: UploadFile = File(...)):
#     if not file.filename.lower().endswith(".mp4"):
#         return {"error": "Upload MP4 video only"}

#     input_path = f"/tmp/{file.filename}"
#     output_path = f"/tmp/processed_{file.filename}"

#     with open(input_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     analyzer.process_video(input_path, output_path)
#     return {"processed_video_path": output_path}



@app.post("/process-video")
def process_video(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".mp4"):
        return {"error": "Only MP4 videos are supported"}

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, file.filename)
        output_path = os.path.join(
            temp_dir, f"processed_{file.filename}"
        )

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        analyzer.process_video(input_path, output_path)

        # Optional: move output to permanent location
        final_output = os.path.join(
            os.getcwd(), f"processed_{file.filename}"
        )
        shutil.copy(output_path, final_output)

    return {
        "message": "Video processed successfully",
        "output_video": final_output
    }



@app.get("/download-video")
def download_video(path: str):
    return FileResponse(
        path,
        media_type="video/mp4",
        filename=path.split("\\")[-1]
    )
