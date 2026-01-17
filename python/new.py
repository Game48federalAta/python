import numpy as np


# Nöronlar arasındaki bağlantıları ve ağırlıkları temsil eden sinir ağı
class NeuralNetwork:
    def __init__(self, num_inputs, num_neurons):
        # Başlangıçtaki ağırlıkları rastgele başlatıyoruz
        self.weights = np.random.rand(num_inputs, num_neurons)

    def forward(self, inputs):
        # Basit bir sinir ağı ileri besleme işlemi (z = W * X)
        return np.dot(inputs, self.weights)

    def get_weights(self):
        return self.weights


# Nöroplastisiteyi simüle eden sınıf
class Neuroplasticity:
    def __init__(self, learning_rate=0.1):
        self.learning_rate = learning_rate

    def apply(self, weights):
        # Ağırlıkların her birini belirli bir şekilde değiştiriyoruz (örneğin, küçük rastgele bir güncelleme)
        weight_changes = np.random.rand(*weights.shape) * self.learning_rate
        return weights + weight_changes


# Ağırlıkları simüle eden model
def simulate_neuroplasticity(num_inputs, num_neurons, num_iterations=10):
    # Sinir ağı modeli oluşturuluyor
    network = NeuralNetwork(num_inputs, num_neurons)
    # Nöroplastisiteyi uygulayan sınıf oluşturuluyor
    neuroplasticity = Neuroplasticity()

    print("Başlangıç Ağırlıkları:")
    print(network.get_weights())

    # Nöroplastisiteyi belirli adımlarda uyguluyoruz
    for _ in range(num_iterations):
        updated_weights = neuroplasticity.apply(network.get_weights())
        network.weights = updated_weights

    print("\nNöroplastisite Sonrası Ağırlıklar:")
    print(network.get_weights())


# Örnek çalıştırma (3 giriş, 4 nöron ve 5 tekrar)
simulate_neuroplasticity(3, 4, num_iterations=5)
