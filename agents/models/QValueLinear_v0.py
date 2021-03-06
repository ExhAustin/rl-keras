import numpy as np
import math

class QValueModel:
	def __init__(self, state_dim, action_dim,
			lr,
			epsilon=1e-3
	):
		self.lr = lr
		self.state_dim = state_dim
		self.action_dim = action_dim

		# create the model
		self.M = epsilon * np.random.rand(state_dim, action_dim)
		self.b = epsilon * np.random.rand(1,1)

	def action_gradients(self, states, actions):
		return np.matmul(self.M.T, states)

	def train_on_grads(self, inputs, q_grads):
		states = inputs[0]
		actions = inputs[1]
		#batchsize = states.shape[1]

		for i in range(self.state_dim):
			for j in range(self.action_dim):
				Mw_grads = np.multiply(states[i,:], actions[j,:])
				self.M[i,j] += self.lr * np.mean(np.multiply(Mw_grads.reshape([1,-1]), q_grads))

		self.b += self.lr * np.mean(q_grads)

	def train(self, inputs, q_targets):
		delta = q_targets - self.predict(inputs)
		self.train_on_grads(inputs, delta)

		return np.mean(np.absolute(delta))

	def predict(self, inputs):
		state = inputs[0]
		action = inputs[1]
		q = np.sum(np.multiply(np.matmul(state.T, self.M).T ,action), axis=0) + self.b
		return q
