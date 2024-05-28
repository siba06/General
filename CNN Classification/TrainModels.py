from Models import getModel
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, Subset
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import datetime
from torch import optim
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
import torch
from torchvision import transforms
from PIL import Image
from torchvision.datasets import ImageFolder
import torch.nn.functional as F
import os
from torchvision.models import resnet50, ResNet50_Weights
import optuna
import argparse
from torchsummary import summary


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

parser = argparse.ArgumentParser(description='')
parser.add_argument('--output_var', type=str, default='gene', help='Name of the output variable (default: gene)')
parser.add_argument('--model_name', type=str, default='CNN2D', help='Model Name (default: CNN2D) Options: CNN2D, CNN3D, ResNet50, VGG16')
args = parser.parse_args()
output_var= args.output_var
model_name = args.model_name


# In[9]:

xlDataPath = 'data/xlData.xlsx'

df = pd.read_excel(xlDataPath)

# Format patient ids as 2 digits
df['id'] = df['id'].apply(lambda x: '{:02d}'.format(x))

imgs_path = 'data/all_imgs'
patients_list = os.listdir(imgs_path)


# Clean dataset by removing patients without data or with missing or unspecified output variable
df = df[df['id'].isin(patients_list)].dropna(subset=[output_var]).drop(df[df[output_var] == 'NA'].index).drop(df[df[output_var] == 'Unspecified'].index).drop(df[df[output_var] == 'None'].index)


# Encode the target variable
le = LabelEncoder()
df[output_var] = le.fit_transform(df[output_var])


# Get weights of classes for balanced training
class_weights = torch.tensor(1/(df[output_var].value_counts(normalize=True))).to(device)

# Split the dataset into train, validation and test sets
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df[output_var], random_state=42)
train_df, val_df = train_test_split(train_df, test_size=0.25, stratify=train_df[output_var], random_state=42)



# Custom Torch Dataset
class AlportDataset(Dataset):
    def __init__(self, df, output_var, input_dir='data/all_imgs', transform=None):
        self.df = df
        self.output_var = output_var
        self.input_dir = input_dir
        self.imgs_list = self.getImgsList()
        self.transform = transform

    def getImgsList(self):
        imgs_list = []
        for patient in self.df['id'].values:
            imgs = [patient+'/'+img for img in os.listdir(os.path.join(self.input_dir, patient))]
            imgs_list.extend(imgs)
        return imgs_list
            
    def __len__(self):
        return len(self.imgs_list)

    def __getitem__(self, idx): 
        img_id= self.imgs_list[idx]
        img_path = os.path.join(self.input_dir, img_id)
        patient = img_id.split('/')[0]
        img = Image.open(img_path)
        img = img.convert('L')
        img = self.transform(img)
                
        label = self.df[self.df['id']==patient][self.output_var].values[0]

        return img,torch.tensor(label)

# Transformations to standardise inputs
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                     std=[0.229, 0.224, 0.225]),
])

batch_size = 64
trainDataset = AlportDataset(train_df,output_var, transform=transform)
train_loader = DataLoader(trainDataset, batch_size=batch_size, shuffle=True)

valDataset = AlportDataset(val_df, output_var,transform=transform)
val_loader = DataLoader(valDataset, batch_size=batch_size, shuffle=True)

testDataset = AlportDataset(test_df,output_var, transform=transform)
test_loader = DataLoader(testDataset, batch_size=batch_size, shuffle=True)


# Objective function for Optuna hyperparameter optimization
def objective(trial):
        
    num_epochs = 30
    
    # Change the output layer
    num_classes = len(class_weights)

    if model_name == 'CNN2D':

        
        out_channels_1 = trial.suggest_categorical("out_channels_1", [16,32])        
        out_channels_2 = trial.suggest_categorical("out_channels_2", [32,64])        
        out_channels_3 = trial.suggest_categorical("out_channels_3", [64,128])        
        
        kernel_sizes = [3, 5, 7]
        kernel_size_1 = trial.suggest_categorical("kernel_size_1", kernel_sizes)
        kernel_size_2 = trial.suggest_categorical("kernel_size_2", kernel_sizes)
        kernel_size_3 = trial.suggest_categorical("kernel_size_3", kernel_sizes)        

        stride_size_1 = trial.suggest_int("stride_size_1", 1, 2)
        stride_size_2 = trial.suggest_int("stride_size_2", 1, 2)
        stride_size_3 = trial.suggest_int("stride_size_3", 1, 2)

        dropout = trial.suggest_float("dropout", 0.0, 0.5)
        out_channels=[out_channels_1, out_channels_2, out_channels_3]
        kernel_sizes=[kernel_size_1, kernel_size_2, kernel_size_3]
        stride_sizes=[stride_size_1, stride_size_2, stride_size_3]

        model = getModel(model_name, num_classes, num_channels=3, out_channels=out_channels, kernel_sizes=kernel_sizes, stride_sizes=stride_sizes, dropout=dropout)
    
    else:

        model = getModel(model_name,num_classes=num_classes, num_channels=3)


    if model_name == 'ResNet50':
        
        # Freeze all layers
        for name, param in model.named_parameters():
                param.requires_grad = False

        freeze_layers = ["fc","layer4", "layer3"]
        all_sublists = []

        for i in range(len(freeze_layers)):
            for j in range(i + 1, len(freeze_layers) + 1):
                sublist = freeze_layers[i:j]
                
                all_sublists.append('_'.join(sublist))

        # Suggest which layers to unfreeze
        unfrozen_layers = trial.suggest_categorical("unfrozen_layers", all_sublists)
        
        # Unfreeze the suggested layers
        unfrozen_layers_list = unfrozen_layers.split('_')
        for name, param in model.named_parameters():
            for layer in unfrozen_layers_list:
                if layer in name:
                    param.requires_grad = True
                    break
        
    elif model_name == 'VGG16':
        # Freeze all layers except the classifier
        for name, param in model.named_parameters():
            if 'classifier' in name:
                param.requires_grad = True
            else:
                param.requires_grad = False
    

    model = model.to(device)
    
    
    # Define loss function and optimizer

    
    optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "SGD"])
    learning_rate = trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True)
    decay = trial.suggest_float("decay", 1e-5, 1e-4, log=True)

    optimizer = getattr(optim, optimizer_name)(model.parameters(), lr=learning_rate, weight_decay = decay)    
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    
    best_val_acc = 0.0
    new_best_val=0
    best_val_loss = float('inf')

    
    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")
        print('-' * 10)

        # Train phase
        model.train()
        running_loss = 0.0
        running_corrects = 0
        for images, labels in tqdm(train_loader):

            images, labels =images.float().to(device), labels.long().to(device)

            # Zero parameter gradients
            optimizer.zero_grad()

            # Forward pass, backward pass, and optimization
            outputs = model(images).to(float)
            _, preds = torch.max(outputs.data, 1)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            # Update statistics
            running_loss += loss.item() * images.size(0)
            running_corrects += torch.sum(preds == labels.data)

        # Validation phase
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        with torch.no_grad():
            for images, labels in tqdm(val_loader):

                images, labels = images.float().to(device), labels.long().to(device)

                outputs = model(images).to(float)

                _, preds = torch.max(outputs.data, 1)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                val_corrects += torch.sum(preds == labels.data)

        # Calculate epoch-level statistics
        train_loss = running_loss / len(train_loader.dataset)
        train_acc = running_corrects.double() / len(train_loader.dataset)
        val_loss = val_loss / len(val_loader.dataset)
        val_acc = val_corrects.double() / len(val_loader.dataset)



        print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
        print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")

        
        if val_acc > best_val_acc:
            new_best_val=0
            best_val_acc = val_acc
            torch.save(model.state_dict(),'data/{}/{}/best_model_acc_{}.pth'.format(output_var, model_name, trial.number))
        else:
            new_best_val+=1
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'data/{}/{}/best_model_loss_{}.pth'.format(output_var, model_name, trial.number))
        
        #Early stopping of training
        #check train acc to prevent overfitting
        if train_acc>0.99:
            new_best_val+=1
        if new_best_val>=5 and epoch>=num_epochs//2:
            print('stopped early')
            break
            
    
    return best_val_acc



study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=30)

print("Best trial:")
trial = study.best_trial

print("  Value: ", trial.value)

print("  Params: ")
for key, value in trial.params.items():
    print("    {}: {}".format(key, value))

