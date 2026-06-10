import time
import os
import google.generativeai as genai

# Configure your active API key
API_KEY = "AQ.Ab8RN6LrJWF71BqNTDthIzwnBmOrOVJt8s7FAcjXLluCV7x7IA"
genai.configure(api_key=AQ.Ab8RN6JIEADWCwjZ5FBnQqWUHlksNBsx-r1ERCp8b8U1rGjPKQ)

# Define a unique name for your custom model
TUNED_MODEL_NAME = "gyanmasti-core-v1"

print("🚀 Step 1: Initiating Cloud Training Job...")

try:
    # Trigger the fine-tuning job on Google Cloud infrastructure
    operation = genai.create_tuned_model(
        source_model="models/gemini-1.5-flash-001-tuning", # Use the stable tuning foundation block
        training_data="dataset.jsonl",                      # Links to your dataset file
        id=TUNED_MODEL_NAME,
        epoch_count=10,
        batch_size=16
    )
    
    print(f"✅ Training Job successfully initialized!")
    print("⏳ Step 2: Syncing weights on Google cloud systems. Please wait (Takes ~5 mins)...")
    
    # Track the cloud status loop until completed
    while not operation.done():
        print("🔄 Google Cloud state: Processing... Checking again in 30 seconds.")
        time.sleep(30)
        
    # Fetch result once done
    result = operation.result()
    print("\n🎉 SUCCESS! Your API is permanently trained.")
    print(f"👉 Copy this target model ID: tunedModels/{TUNED_MODEL_NAME}")

except Exception as e:
    print(f"\n❌ Pipeline failed. Error details: {str(e)}")
