import torch
import torch.nn as nn
import torch.optim as optim

class BrainAI(nn.Module):
    def __init__(self):
        super(BrainAI, self).__init__()
        # 2 girdi, 1 çıktı ile bir linear katman
        self.linear = nn.Linear(2, 1)

    def forward(self, x):
        # Modelin çıktısı
        return self.linear(x)


# Modeli oluştur
model = BrainAI()

# Kayıp fonksiyonu ve optimizasyon
criterion = nn.MSELoss()  # Mean Squared Error Loss
optimizer = optim.SGD(model.parameters(), lr=0.1)

x_train = torch.tensor([[1.0], [2.0], [3.0], [4.0]], dtype=torch.float32)
y_train = torch.tensor([[2.0], [4.0], [6.0], [8.0]], dtype=torch.float32)

# Eğitim döngüsü
for epoch in range(600):
    # Model tahminini al
    y_pred = model(x_train)

    # Kayıp hesapla
    loss = criterion(y_pred, y_train)

    # Geriye yayılım (backpropagation) ve optimizasyon
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}: Loss {loss.item()}")

# Test et
with torch.no_grad():
    test_val = torch.tensor([[5.0],[55.0],[11.0],[4555.0],[5.0]])
    for i in test_val:
        prediction = model(i)
        print(f"Prediction for input {i.item()}: {prediction.item()}")

