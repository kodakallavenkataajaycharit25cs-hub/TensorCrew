import torch
import torch.nn as nn
import os
from torch.cuda.amp import autocast, GradScaler

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
        self.scaler = GradScaler() if device == 'cuda' else None
        self.best_acc = 0.0
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def fit(self, epochs, start_epoch=0):
        for epoch in range(start_epoch, epochs):
            self.model.train()
            running_loss = 0.0
            correct = 0
            total = 0
            
            for images, labels in self.train_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                
                if self.scaler:
                    with autocast():
                        outputs = self.model(images)
                        loss = self.criterion(outputs, labels)
                    self.scaler.scale(loss).backward()
                    self.scaler.step(self.optimizer)
                    self.scaler.update()
                else:
                    outputs = self.model(images)
                    loss = self.criterion(outputs, labels)
                    loss.backward()
                    self.optimizer.step()
                
                running_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
            
            train_loss = running_loss / len(self.train_loader)
            train_acc = 100. * correct / total
            val_loss, val_acc = self.evaluate()
            
            print(f"Epoch [{epoch+1}/{epochs}]")
            print(f"   Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
            print(f"   Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.2f}%")
            
            if val_acc > self.best_acc:
                self.best_acc = val_acc
                self.save_checkpoint(epoch + 1, val_acc, filename="best_model.pth")
                print(f"   New Best Model Saved! (Acc: {val_acc:.2f}%)")
            
            if (epoch + 1) % 5 == 0:
                self.save_checkpoint(epoch + 1, val_acc, filename=f"checkpoint_epoch_{epoch+1}.pth")
                print(f"   Periodic Checkpoint Saved: checkpoint_epoch_{epoch+1}.pth")

            print("-" * 30)
            self.scheduler.step(val_loss)

    def evaluate(self):
        self.model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in self.val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        return val_loss / len(self.val_loader), 100. * correct / total

    def save_checkpoint(self, epoch, acc, filename):
        state = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'acc': acc,
            'best_acc': self.best_acc
        }
        torch.save(state, os.path.join(self.save_dir, filename))

    def load_latest_checkpoint(self):
        if not os.path.exists(self.save_dir): return 0
        
        checkpoints = [f for f in os.listdir(self.save_dir) if f.startswith('checkpoint_epoch_')]
        if not checkpoints: return 0
        
        checkpoints.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
        latest = checkpoints[-1]
        path = os.path.join(self.save_dir, latest)
        
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.best_acc = checkpoint.get('best_acc', checkpoint['acc'])
        
        print(f"Resumed from checkpoint: {latest} (Epoch {checkpoint['epoch']}, Prev Acc: {checkpoint['acc']:.2f}%)")
        return checkpoint['epoch']
