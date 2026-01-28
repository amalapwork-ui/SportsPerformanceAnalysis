import pandas as pd
import joblib
import cv2
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from ultralytics import YOLO


class SportsAnalyzer:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        self.yolo = YOLO("yolov8n.pt")
        self._preprocess()

    def _clean_currency(self, val):
        if isinstance(val, str):
            val = val.replace("€", "").replace("M", "e6").replace("K", "e3")
            return eval(val)
        return val

    def _preprocess(self):
        for col in ["Value", "Wage", "Release Clause"]:
            self.df[col] = self.df[col].apply(self._clean_currency)

        self.df.fillna(self.df.median(numeric_only=True), inplace=True)
        self.df["Work Rate Encoded"] = (
            self.df["Work Rate"].astype("category").cat.codes
        )

    def train_and_save_models(self):
        features = [
            "Age", "Potential", "Stamina",
            "Strength", "SprintSpeed", "Work Rate Encoded"
        ]

        X = self.df[features]
        y_overall = self.df["Overall"]
        y_value = self.df["Value"]

        overall_model = XGBRegressor(
            n_estimators=200, learning_rate=0.05, max_depth=6
        )
        overall_model.fit(X, y_overall)

        value_model = RandomForestRegressor(n_estimators=200)
        value_model.fit(X, y_value)

        joblib.dump(overall_model, "models/overall_model.pkl")
        joblib.dump(value_model, "models/value_model.pkl")

    def predict(self, features):
        overall = float(self.overall_model.predict([features])[0])
        value = float(self.value_model.predict([features])[0])
        return overall, value
    # def predict(self, features):
    #     overall = self.overall_model.predict([features])[0]
    #     value = self.value_model.predict([features])[0]
    #     return overall, value

    def assess_injury_risk(self, age, stamina, work_rate):
        risk_score = (
            (age / 40) * 0.4 +
            (1 - stamina / 100) * 0.4 +
            (work_rate / 5) * 0.2
        )

        if risk_score < 0.33:
            return "Low"
        elif risk_score < 0.66:
            return "Medium"
        return "High"

    # def process_video(self, input_path, output_path):
    #     cap = cv2.VideoCapture(input_path)
    #     out = cv2.VideoWriter(
    #         output_path,
    #         cv2.VideoWriter_fourcc(*"mp4v"),
    #         int(cap.get(5)),
    #         (int(cap.get(3)), int(cap.get(4)))
    #     )

    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if not ret:
    #             break

    #         results = self.yolo.track(frame, persist=True, classes=[0])
    #         out.write(results[0].plot())

    #     cap.release()
    #     out.release()
    def process_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            int(cap.get(5)),
            (int(cap.get(3)), int(cap.get(4)))
        )

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.yolo.track(frame, persist=True, classes=[0])
            out.write(results[0].plot())

        cap.release()
        out.release()
