from manim import *
from manim_ml.neural_network import Convolutional2DLayer, FeedForwardLayer, NeuralNetwork
class ClientModel(Scene):
    def construct(self):
        # Make the neural network \
        # Convolutional2DLayer(num_feature_maps, feature_map_size, filter_size)
        nn = NeuralNetwork([
            Convolutional2DLayer(1,32,3),
            Convolutional2DLayer(32,64,3),
            FeedForwardLayer(num_nodes=128),

        ])
        self.add(nn)
        # Make the animation
        forward_pass_animation = nn.make_forward_pass_animation(run_time=10)
        # Play the animation
        self.play(forward_pass_animation)
