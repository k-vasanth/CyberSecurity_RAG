import json
class FeedbackStore:
    def save(self, feedback_data, file_path="feedback.json"):
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(json.dumps(feedback_data) + "\n")
