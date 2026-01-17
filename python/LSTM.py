import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

# 1. Veri oluştur (sinüs fonksiyonu)
data = np.sin(np.linspace(0, 100, 1000))
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data.reshape(-1, 1))


# 2. Dataset oluşturma fonksiyonu
def create_dataset(data, time_step=5):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i : (i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)


time_step = 5
X, Y = create_dataset(scaled_data, time_step)

# Veriyi tensorlara çevir ve reshape et
X = torch.from_numpy(X).float().reshape(-1, time_step, 1)
Y = torch.from_numpy(Y).float().reshape(-1, 1)


# 3. LSTM modelini tanımla
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
        super(LSTMModel, self).__init__()
        self.hidden_layer_size = hidden_layer_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        self.hidden_cell = (
            torch.zeros(1, 1, self.hidden_layer_size),
            torch.zeros(1, 1, self.hidden_layer_size),
        )

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq, self.hidden_cell)
        predictions = self.linear(lstm_out[-1])
        return predictions


# Modeli oluştur
model = LSTMModel()

# 4. Loss fonksiyonu ve optimizer tanımla
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 5. Modeli eğit
epochs = 150
for i in range(epochs):
    for seq, labels in zip(X, Y):
        optimizer.zero_grad()
        batch_size = seq.shape[0]  # Batch size'ı kontrol et

        # hidden_cell'i batch size'a göre ayarla
        model.hidden_cell = (
            torch.zeros(1, batch_size, model.hidden_layer_size),
            torch.zeros(1, batch_size, model.hidden_layer_size),
        )

        y_pred = model(seq.unsqueeze(0))

        single_loss = loss_function(y_pred, labels)
        single_loss.backward()
        optimizer.step()

    if i % 25 == 0:
        print(f"Epoch {i} loss: {single_loss.item()}")

# 6. Modeli kaydet
torch.save(model.state_dict(), "lstm_model.pth")
joblib.dump(scaler, "scaler.save")

# 1. Modeli yükle
model = LSTMModel()
model.load_state_dict(torch.load("lstm_model.pth"))
model.eval()

# 2. Scaler'ı yükle
scaler = joblib.load("scaler.save")

# 3. Test verisi oluştur (yeni sinüs verisi)
test_data = np.sin(np.linspace(100, 105, 6))  # Sinüs dalgasının devamı
scaled_test_data = scaler.transform(test_data.reshape(-1, 1))

# 4. Test verisini modele uygun hale getir
X_test = torch.from_numpy(scaled_test_data[:5].reshape(1, 5, 1)).float()

# 5. Model ile tahmin yap
with torch.no_grad():
    model.hidden_cell = (
        torch.zeros(1, 1, model.hidden_layer_size),
        torch.zeros(1, 1, model.hidden_layer_size),
    )
    predicted = model(X_test)

# 6. Tahmini geri ölçekle
predicted_value = scaler.inverse_transform(predicted.detach().numpy())

# 7. Tahmini yazdır
print(f"Tahmin edilen değer: {predicted_value[0][0]}")
