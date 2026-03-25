import torch
from torchvision import transforms
from PIL import Image
from model.custom_nn import SkinDiseaseCNN
from dataset.dataset_loader import get_loaders

def predict(image_path):
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # 1. Load Data Info (for class names)
    _, _, _, classes = get_loaders()
    
    # 2. Load the Final Model
    model = SkinDiseaseCNN(num_classes=len(classes)).to(DEVICE)
    checkpoint = torch.load('checkpoints/best_model.pth', map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    # 3. Preprocess the Image (Must match the Training transforms)
    img = Image.open(image_path).convert('RGB')
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img_tensor = preprocess(img).unsqueeze(0).to(DEVICE)
    
    # 4. Final Verdict!
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        conf, pred = torch.max(probs, 1)
        
    print(f"\n🩺 PREDICTION FOR: {image_path}")
    print(f"   Disease:    {classes[pred.item()]}")
    print(f"   Confidence: {100*conf.item():.2f}%")

if __name__ == "__main__":
    # Change 'test_image.jpg' to any image you want to test!
    predict('test_image.jpg')
