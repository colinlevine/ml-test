#!/usr/bin/env python3
"""
Script to count and analyze training examples in the sav-micro dataset.
"""

import json
import os

def count_training_examples(file_path):
    """Count the number of training examples in the JSON dataset."""
    try:
        print("📊 Loading and analyzing dataset...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("❌ Error: Dataset is not a list format")
            return 0
        
        count = len(data)
        print(f"📈 Total training examples: {count}")
        
        # Classification analysis
        safe_count = 0
        threat_count = 0
        malformed_count = 0
        
        for i, example in enumerate(data):
            if 'messages' not in example:
                print(f"⚠️  Example {i+1} missing 'messages' key")
                continue
                
            # Find the assistant response
            for message in example['messages']:
                if message['role'] == 'assistant':
                    try:
                        response = json.loads(message['content'])
                        classification = response.get('classification', 'UNKNOWN')
                        if classification == 'SAFE':
                            safe_count += 1
                        elif classification == 'THREAT':
                            threat_count += 1
                        else:
                            print(f"⚠️  Unknown classification in example {i+1}: {classification}")
                    except json.JSONDecodeError as e:
                        malformed_count += 1
                        print(f"❌ Malformed JSON in example {i+1}")
                    break
        
        # Results summary
        print(f"\n🏷️  Classification Breakdown:")
        print(f"   SAFE examples: {safe_count}")
        print(f"   THREAT examples: {threat_count}")
        if malformed_count > 0:
            print(f"   Malformed examples: {malformed_count}")
        
        classified_total = safe_count + threat_count
        print(f"   Total classified: {classified_total}")
        
        # Percentages
        if count > 0:
            print(f"\n📊 Distribution:")
            print(f"   SAFE: {safe_count/count*100:.1f}%")
            print(f"   THREAT: {threat_count/count*100:.1f}%")
        
        # Dataset status
        print(f"\n🎯 Dataset Status:")
        if count >= 200:
            print(f"   ✅ Target reached: {count}/200 examples")
        else:
            print(f"   🔄 In progress: {count}/200 examples ({200-count} remaining)")
        
        # Balance assessment
        if safe_count > 0 and threat_count > 0:
            ratio = safe_count / threat_count
            if 0.8 <= ratio <= 1.2:
                print(f"   ⚖️  Well balanced SAFE/THREAT ratio: {ratio:.2f}")
            else:
                print(f"   ⚠️  Imbalanced SAFE/THREAT ratio: {ratio:.2f}")
        
        return count
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return 0
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

def main():
    dataset_path = "datasets/eval-extended.json"
    
    print("🤖 Sav-micro Dataset Analyzer")
    print("=" * 35)
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset file not found: {dataset_path}")
        return
    
    # File info
    file_size = os.path.getsize(dataset_path)
    print(f"📁 File: {dataset_path}")
    print(f"💾 Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    # Count and analyze
    count = count_training_examples(dataset_path)
    
    if count > 0:
        print(f"\n🎉 Analysis complete! Dataset ready for training.")
    else:
        print(f"\n❌ Dataset analysis failed!")

if __name__ == "__main__":
    main()

def main():
    # Dataset file path
    dataset_path = "datasets/training-extended.json"
    
    print("Sav-micro Dataset Counter")
    print("=" * 30)
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    # Get file size
    file_size = os.path.getsize(dataset_path)
    print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    # Count examples
    count = count_training_examples(dataset_path)
    
    if count > 0:
        print(f"\n✅ Dataset validation successful!")
        print(f"Ready for training with {count} examples.")
    else:
        print(f"\n❌ Dataset validation failed!")

if __name__ == "__main__":
    main()
