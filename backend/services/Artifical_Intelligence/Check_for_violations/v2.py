from google import genai

# Nhớ tự nạp API Key của ông vào nha
client = genai.Client(api_key="AIzaSyCbX89NmlXQ-1gP9xgJMLb8CripJc1fybw")

print("Danh sách các model ông có thể xài:")
for model in client.models.list():
        print(model.name)