#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import opengate as gate
from opengate.sources.utility import __get_rad_beta_spectrum
from opengate.sources.utility import get_rad_yield
import pathlib
import pyvista
import SimpleITK as sitk
import sys
sys.path.append("/volatile/Gate10dev/opengate")
#from opengate.sources import utility
#from opengate.sources.utility import set_source_energy_spectrum
#from opengate.sources.utility import set_source_energy_spectrum

current_path = pathlib.Path(__file__).parent.resolve()
data_path = current_path / "data"
output_path = current_path / "outputMobyF18"
output_file = output_path / "dose.mhd"


def simulation(visu=True):
	# units
	m = gate.g4_units.m
	mm = gate.g4_units.mm
	um = gate.g4_units.um
	Bq = gate.g4_units.Bq
	sec = gate.g4_units.s

	# create the simulation
	sim = gate.Simulation()

	sim.progress_bar = True

	# main options
	ui = sim.user_info
	ui.g4_verbose = False
	ui.g4_verbose_level = 1
	#ui.visu = visu
	#ui.visu_type = "vrml_file_only"
	#ui.visu_filename = str(output_path / f"visu_{n}.wrl")
	ui.random_seed = "auto"
	ui.number_of_threads = 6

	# materials
	sim.volume_manager.add_material_database("/volatile/Gate10dev/opengate/opengate/tests/data/GateMaterials.db")

	# change world size
	world = sim.world
	world.size = [1 * m, 1 * m, 1 * m]

	# patient CT
	moby_ct = sim.add_volume("Image", "moby_ct")
	moby_ct.image = str(current_path / "F_LR_30g_atn_1_water.mhd")
	moby_ct.voxel_materials = [[1, 1, "Water"], [0, 0, "Air"]]
	moby_ct.translation = [0 * mm, 0 * mm, 0 * mm]

	moby_ct_info = gate.image.read_image_info(moby_ct.image)
	moby_ct.dump_label_image = output_path / "irt_label.mhd"

	print(f"CT image origin and size: {moby_ct_info.origin}, {moby_ct_info.size}, {moby_ct_info.spacing}")

	# physics
	sim.physics_manager.physics_list_name = "QGSP_BIC_EMZ"
	sim.physics_manager.set_production_cut("world", "gamma", 10 * m)
	sim.physics_manager.set_production_cut("world", "electron", 10 * m)
	sim.physics_manager.set_production_cut("world", "positron", 10 * m)
	sim.physics_manager.set_production_cut(moby_ct.name, "gamma", 100 * um)
	sim.physics_manager.set_production_cut(moby_ct.name, "electron", 100 * um)
	sim.physics_manager.set_production_cut(moby_ct.name, "positron", 100 * um)

	# Activity map from SPECT imaging
	source = sim.add_source("VoxelSource", "source")
	source.attached_to = moby_ct.name
	# source.particle = "ion 71 177"
	source.particle = "e+"
	#source.image = str(current_path / "F_LR_30g_act_1_brain.mhd")
	source.image = str("F_LR_30g_act_1_brain.mhd")

	source.direction.type = "iso"
	source.energy.type = "F18"
	#set_source_energy_spectrum(source, "Lu177")  # After defining the particle!!
	#source.energy.spectrum_histogram_interpolation = interpolation
	#source.energy.type = "spectrum_histogram"
	#source.energy.spectrum_energy_bin_edges = spectrum.energy_bin_edges
	#source.energy.spectrum_weights = spectrum.weights
	# compute the translation to align the source with CT
	# (considering they are in the same physical space)
	source.position.translation = gate.image.get_translation_between_images_center(moby_ct.image, source.image)
	source_info = gate.image.read_image_info(source.image)
	activity =  178 * 1e6 * Bq / ui.number_of_threads
	total_yield = get_rad_yield("F18")
	print(f"{total_yield=}")
	source.activity = activity * total_yield
	#source.n = n / ui.number_of_threads

	total_yield = get_rad_yield("F18")
	print(f"{total_yield=}")
	print("Yield for F18 (nb of e+ per decay) : ", total_yield)

	print(f"Source image origin and size: {source_info.origin}, {source_info.size}, {source_info.spacing}")

	# dose actor
	dose = sim.add_actor("DoseActor", "dose")
	dose.attached_to = moby_ct
	dose.output_filename = output_file
	dose.size = moby_ct_info.size
	dose.spacing = moby_ct_info.spacing
	dose.hit_type = "random"
	dose.output_coordinate_system = "attached_to_image"
	dose.dose.active = True
	dose.dose_uncertainty.active = True

	# add stat actor
	stats = sim.add_actor("SimulationStatisticsActor", "Stats")
	stats.track_types_flag = True

	# start simulation
	sim.run()

	# print results at the end
	print(stats)


def load(mhd: str):
	img = sitk.ReadImage(mhd)
	data = np.array(sitk.GetArrayFromImage(img))
	data = np.swapaxes(data, 0, 2)
	data = np.rot90(data, 3)
	return img, data


#def analysis():
#	dose_img, dose = load(str(output_file).replace(".mhd", "_dose.mhd"))
#	ct_img, ct = load(str(current_path / "F_LR_30g_atn_1_water.mhd"))
#	mcSlice = dose[:, :, 300]
#	ctSlice = ct[:, :, 300]
#	fig, ax = plt.subplots()
	# cbar = plt.figure().colorbar(plt.imshow(mcSlice,label='Dose'))
#	ax.imshow(ctSlice)
#	im_dose = ax.imshow(mcSlice, label='Dose', alpha=.7)
#	fig.colorbar(im_dose)

#	plt.xlabel('pixel')
#	plt.ylabel('pixel')
#	plt.set_cmap('jet')
#	plt.tight_layout()
#	plt.title('Dose slice')
#	plt.show()


#def visualisation(n: int):
#	pl = pyvista.Plotter()
#	pl.import_vrml(str(output_path / f"visu_{n}.wrl"))
#	pl.add_axes(line_width=5, color="white")
#	pl.background_color = "black"
#	for actor in pl.renderer.GetActors():
#		actor.GetProperty().SetOpacity(.7)
#	pl.show()


def main():
	#n = 139
	enable_visu = False

	simulation(visu=enable_visu)

	#analysis()

	if enable_visu:
		visualisation(n)


if __name__ == "__main__":
	main()
