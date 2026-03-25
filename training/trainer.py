import torch
import torch.nn as nn
from tqdm import tqdm
import os

class Trainer:
    def __init__(self, model, train_loader, val_loader, criterion, optimizer, scheduler, device, save_dir='checkpoints'):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        self.save_dir = save_dir
        self.best_acc = 0.0

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def train_epoch(self, epoch):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc=f"Epoch {epoch} [Train]")
        for images, labels in pbar:
            images, labels = images.to(self.device), labels.to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix(loss=f"{loss.item():.4f}", acc=f"{100.*correct/total:.2f}%")
        
        return running_loss / len(self.train_loader), 100. * correct / total

    def validate(self, epoch):
        self.model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            pbar = tqdm(self.val_loader, desc=f"Epoch {epoch} [Val]")
            for images, labels in pbar:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
                
                pbar.set_postfix(loss=f"{loss.item():.4f}", acc=f"{100.*correct/total:.2f}%")
        
        acc = 100. * correct / total
        avg_loss = val_loss / len(self.val_loader)
        
        if acc > self.best_acc:
            self.best_acc = acc
            self.save_checkpoint(epoch, acc, is_best=True)
            
        return avg_loss, acc

    def save_checkpoint(self, epoch, acc, is_best=False):
        state = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'acc': acc,
        }
        
        filename = os.path.join(self.save_dir, 'last_checkpoint.pth')
        torch.save(state, filename)
        
        if is_best:
            torch.save(state, os.path.join(self.save_dir, 'best_model.pth'))
            print(f"⭐ Best Model Saved (Acc: {acc:.2f}%)")

    def fit(self, epochs):
        for epoch in range(1, epochs + 1):
            train_loss, train_acc = self.train_epoch(epoch)
            val_loss, val_acc = self.validate(epoch)
            
            print(f"\n📊 Summary Epoch {epoch}:")
            print(f"   Train Loss: {train_loss:.4f} | Acc: {train_acc:.2f}%")
            print(f"   Val   Loss: {val_loss:.4f} | Acc: {val_acc:.2f}%\n")
            
            self.scheduler.step(val_loss)
