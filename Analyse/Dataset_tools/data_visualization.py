import matplotlib.pyplot as plt
import os

class Dataset:
	def __init__(self, dataset_path):
		self.dataset = dataset_path

	def get_data_from_id(self, id):
		files = [f for r, d, f in os.walk(self.dataset)][0]
		data_for_id = []; data_dict = {}
		for file in files:
			with open(f"{self.dataset}/{file}", "r") as _f:
				data = _f.readlines()
			for d in data:
				if d.startswith(id):
					data_for_id.append(d)

		for d in data_for_id:
			spl = d.split(';')
			time = spl[1].split('T')[1].split('.')[0]
			data_dict[time] = [spl[2], spl[3], spl[4].replace('\n', '')]

		return data_dict


class Visualization:
	def __init__(self, id):
		self.dataset = Dataset('bf_dataset').get_data_from_id(id)
		self.id = id

	def plot_data(self):
		x = list(self.dataset.keys())

		fig, ax = plt.subplots(2, 1)
		ax[0].plot(x, [float(self.dataset.get(_)[1])/float(self.dataset.get(_)[2]) for _ in x])
		ax[0].set_title("Concentration (veh/km)")

		ax[1].plot(x, [float(self.dataset.get(_)[2]) for _ in x])
		ax[1].set_title("Speed (km/h)")
		plt.show()


Visualization("MM713.N1").plot_data()