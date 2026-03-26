import torch
import torch.nn as nn
from tqdm import tqdm
import os
from torch.cuda.amp import autocast, GradScaler

class Trainer:
    def __init__(self, model, train_loader, test_loader, criterion, optimizer, scheduler, device, save_dir='checkpoints'):
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        self.save_dir = save_dir
        self.scaler = GradScaler() if device == 'cuda' else None
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def train(self, epochs, start_epoch=0):
        for epoch in range(start_epoch, epochs):
            self.model.train()
            running_loss = 0.0
            correct = 0
            total = 0
            
            pbar = tqdm(self.train_loader, desc=f"Epoch {epoch+1}/{epochs}")
            for images, labels in pbar:
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
                pbar.set_postfix(loss=f"{loss.item():.4f}", acc=f"{100.*correct/total:.2f}%")
            
            train_acc = 100. * correct / total
            val_loss, val_acc = self.evaluate()
            
            print(f"📊 Ep {epoch+1}: T-Loss {running_loss/len(self.train_loader):.3f} T-Acc {train_acc:.2f}% | V-Loss {val_loss:.3f} V-Acc {val_acc:.2f}%")
            
            self.scheduler.step(val_loss)
            self.save_checkpoint(epoch + 1, val_acc)

    def evaluate(self):
        self.model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in self.test_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        return val_loss / len(self.test_loader), 100. * correct / total

    def save_checkpoint(self, epoch, acc, filename="Checkpoint.pth.tar"):
        state = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'acc': acc,
        }
        torch.save(state, os.path.join(self.save_dir, filename))
        if epoch % 5 == 0:
            torch.save(state, os.path.join(self.save_dir, f"checkpoint_epoch_{epoch}.pth.tar"))

    def load_checkpoint(self, filename="Checkpoint.pth.tar"):
        path = os.path.join(self.save_dir, filename)
        if os.path.exists(path):
            checkpoint = torch.load(path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
            print(f"✅ Loaded checkpoint from {path} (Epoch {checkpoint['epoch']})")
            return checkpoint['epoch']
        return 0
