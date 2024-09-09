import torch
import torchvision.transforms as transforms
from PIL import Image
from models.lenet import LeNet
def load_model(model_path='lenet.pth'):
    # Load the trained LeNet model
    model = LeNet(num_classes=10)  
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    return model


def image_classification(file):
    # Check if the file extension is 'png'
    # Load the trained model
    model = load_model()
    # Load and preprocess the image
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),
    ])
    image = Image.open(file).convert('L')  # Convert to grayscale
    image = transform(image).unsqueeze(0)  # Add batch dimension

    # Perform image classification
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        classification_result = predicted.item()

    return f"Classification result: {classification_result}"

if __name__ == '__main__':
    file='avatar.png'
    classification_result = image_classification(file)
    assistant_content = f"Classification result: {classification_result}"
    print(assistant_content)
