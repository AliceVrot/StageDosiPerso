#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import opengate as gate
from opengate.sources.utility import __get_rad_beta_spectrum 
from opengate.sources.utility import __get_rad_gamma_spectrum
from opengate.sources.utility import get_rad_yield
import pathlib
import pyvista
import SimpleITK as sitk
import sys
import argparse
from pathlib import Path
import random
sys.path.append("/volatile/Gate10dev/opengate")
#from opengate.sources import utility
#from opengate.sources.utility import set_source_energy_spectrum
#from opengate.sources.utility import set_source_energy_spectrum

#current_path = pathlib.Path(__file__).parent.resolve()
#data_path = current_path / "data"
#output_path = current_path / "outputMobyF18verifnoneau"
#output_file = output_path / "dose.mhd"


def simulation(ct_image_path, activity_image_path, activity_value, output_doss, threads, visu=True):

	current_path = pathlib.Path(__file__).parent.resolve()
	data_path = current_path / "data"
	output_path = current_path / output_doss
	output_file = output_path / "dose.mhd"
	
	#moby_ct.image = str(ct_image_path)
	#source.image = str(activity_image_path)
	#activity = activity_value * Bq / threads
	
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
	ui.random_seed = "auto" ##Je peux changer ça??
	#ui.number_of_threads = 6

	# materials
	#sim.volume_manager.add_material_database("/volatile/Gate10dev/opengate/opengate/tests/data/GateMaterials.db")
	sim.volume_manager.add_material_database("/home/verot/Projet/GateMaterials.db")

	##CA JE PEUX LE CHANGER AUSSI


	# change world size
	world = sim.world
	world.size = [1 * m, 1 * m, 1 * m]

	# patient CT
	moby_ct = sim.add_volume("Image", "moby_ct")
	#moby_ct.image = str(current_path / "F_LR_30g_atn_1.mhd")
	moby_ct.image = str(ct_image_path)
	moby_ct.voxel_materials = [[1, 1, "Water"], [0, 0, "Air"]]
	#moby_ct.voxel_materials = [[1, 1.9, "Water"], [0, 0.9, "Air"],[2,2.9, "Body"],[3, 3.9, "Brain"], [4, 4.9, "Heart"], [5, 5.9, "Lung"], [6, 6.9, "Liver"], [7, 7.9, "Intestine"], [8, 8.9, "Spleen"], [9, 9.9, "Kidney"], [10, 10.9, "Intestine"]] #Intestin au lieu de Stomach et Bladder car je n'ai pas trouvé dans la database de Gate 
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
	#spectrum = __get_rad_beta_spectrum("Lu177")
	#source = sim.add_source("VoxelSource", "source")
	#source.attached_to = moby_ct.name
	# source.particle = "ion 71 177"
	#source.particle = "e-"
	#source.image = str(current_path / "F_LR_30g_act_1_brain.mhd")
	#source.image = str (activity_image_path)	
	#source.direction.type = "iso"
	#source.energy.type = "spectrum_histogram"
	#source.energy.spectrum_energy_bin_edges = spectrum.energy_bin_edges
	#source.energy.spectrum_weights = spectrum.weights

	spectrumgamma = __get_rad_gamma_spectrum("Lu177")
	
	sourcegamma = sim.add_source("VoxelSource", "sourcegamma")
	sourcegamma.attached_to = moby_ct.name
	sourcegamma.particle = "gamma"
	sourcegamma.image = str (activity_image_path)	
	sourcegamma.direction.type = "iso"
	sourcegamma.energy.type = "spectrum_discrete"
	sourcegamma.energy.spectrum_energies = spectrumgamma.energies
	sourcegamma.energy.spectrum_weights = spectrumgamma.weights

	sourcegamma.position.translation = gate.image.get_translation_between_images_center(moby_ct.image, sourcegamma.image)
	#source_info = gate.image.read_image_info(sourcegamma.image)
	#sourcegamma.attached_to = moby_ct.name
	
	# source.particle = "ion 71 177"
	#source.particle = "e-"
	#source.image = str(current_path / "F_LR_30g_act_1_brain.mhd")
	#source.image = str (activity_image_path)	
	#source.direction.type = "iso"
	#source.energy.type = "spectrum_histogram"
	#source.energy.spectrum_energy_bin_edges = spectrumgamma.energy_bin_edges
	#source.energy.spectrum_weights = spectrumgamma.weights


	#set_source_energy_spectrum(source, "Lu177")  # After defining the particle!!
	#source.energy.spectrum_histogram_interpolation = interpolation
	#source.energy.type = "spectrum_histogram"
	#source.energy.spectrum_energy_bin_edges = spectrum.energy_bin_edges
	#source.energy.spectrum_weights = spectrum.weights
	# compute the translation to align the source with CT
	# (considering they are in the same physical space)
	#source.position.translation = gate.image.get_translation_between_images_center(moby_ct.image, source.image)
	#source_info = gate.image.read_image_info(source.image)
	#source.n = n / ui.number_of_threads
	total_yield = get_rad_yield("Lu177")
	print(f"{total_yield=}")
	#source.activity = activity_value * 1e6 * Bq * total_yield

	#total_yieldgamma = get_rad_yield("Lu177", particle="gamma")
	sourcegamma.activity = activity_value * 1e6 * Bq * 0.16
	#print(f"Source image origin and size: {source_info.origin}, {source_info.size}, {source_info.spacing}")

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
	# dose.counts.active = True

	# add stat actor
	stats = sim.add_actor("SimulationStatisticsActor", "Stats")
	stats.track_types_flag = True
		# print results at the end
	print(stats)
	
	output_doss = Path(output_doss)
	stats.output_filename = output_doss / "simulation_stats.txt"
	#stats.output_filename = "simulation_stats.txt"

	# start simulation
	sim.run()

	# print results at the end
	#print(stats)
	#stats.output_filename = output_doss / "simulation_stats.txt"
	#stats.output_filename = "simulation_stats.txt"



def load(mhd: str):
	img = sitk.ReadImage(mhd)
	data = np.array(sitk.GetArrayFromImage(img))
	data = np.swapaxes(data, 0, 2)
	data = np.rot90(data, 3)
	return img, data


#def analysis():s
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
	parser = argparse.ArgumentParser(description="Simulation with input phantom and activity.")
	parser.add_argument("--ct", type=str, required=True, help="Path to the CT image (.mhd)")
	parser.add_argument("--activity", type=str, required=True, help="Path to the activity image (.mhd)")
	parser.add_argument("--activity_value", type=float, default=44, help="Activity EN MBQ scaling factor (default=44)")
	parser.add_argument("--output_doss", type=str, default="outputMobyF18verifnoneau", help="Output directory for dose (default=outputMobyF18verifnoneau)")
	parser.add_argument("--threads", type=float, default="6", help="number of threads")
	parser.add_argument("--visu", action='store_true', help="Enable visualization")


	args = parser.parse_args()
	#n = 139
	enable_visu = False

	simulation(
        ct_image_path=args.ct,
        activity_image_path=args.activity,
        activity_value=args.activity_value,
        output_doss=args.output_doss,
		threads = args.threads,
        visu=args.visu
    )

	#simulation(visu=enable_visu)

	#analysis()

	#if enable_visu:
	#	visualisation(n)


if __name__ == "__main__":
	main()
