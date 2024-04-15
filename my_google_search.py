import json
from datasets import load_dataset
class MyGoogleSearch:

    def __init__(self):
        self.data = self.get_data()

    def get_data(self):
        with open("data.json", "r") as f:
            data = json.load(f)
        return data

    def upload_file(self, path_to_new_data):
        try:
            with open(path_to_new_data, "r") as f:
                new_data = json.load(f)
                if type(new_data) == list:
                    self.data.extend(new_data)
                elif type(new_data) == dict:
                    self.data.append(new_data)
                else:
                    raise Exception("Invalid data format")

            with open("data.json", "w") as f:
                json.dump(self.data, f)
            return 0
        except:
            return -1

    def remove_file(self, title):
        title = title.replace("\n", "")
        data_to_remove = next((x for x in self.data if x["title"].replace("\n", "") == title), None)
        if not data_to_remove:
            return -1
        else:
            self.data.remove(data_to_remove)
            with open("data.json", "w") as f:
                json.dump(self.data, f)
            return 0

    def list_files(self):
        return [x["title"] for x in self.data]

    def search(self, search_query):
        search_query = search_query.split()
        relevant_files = []
        for item in self.data:
            content = item["text"].lower()
            if all(i in content for i in search_query):
                relevant_files.append(item)

        total_files = len(relevant_files)
        if total_files > 10:
            relevant_files = relevant_files[:10]

        return total_files, relevant_files