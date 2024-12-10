import numpy as np
import calculations_bolts
import thermal
from itertools import product

t2s = np.linspace(0.002, 0.01, 20) # at least 2 mm (immediately chosen)
t3s = np.linspace(0.005, 0.005, 1) # constant 5mm

widths = np.linspace(0.05, 0.05, 1) # constant 5 cm
lengths = np.linspace(0.05, 0.10, 9) # at least 5cm (immediately chosen)

lug_material = 2 ## 2 or 8
wall_material = 7
bolt_material = 1

Material_namessss = [
	"1 - AL6061-T6", 
	"2 - AL Alloy 7075-T6", 
	"3 - AL Alloy 2024-T3", 
	"4 - Stainless Steel 316", 
	"5 - Inconel 718", 
	"6 - Maraging Steel 18Ni(250)",
	"7 - Aluminium alloy AA 2024-T3",
	"8 -4130 Steel "  #material of the wall for whatever reason
]

Material_names = np.array([1,2,3,4,5,6,7,8])

normal_yield = np.array([240E6, 503E6, 324E6, 290E6, 1030E6, 1725E6,370E6,435E6])#Pa
shear_yield = normal_yield/np.sqrt(3)  # Shear yield strengths in MPa
E_moduli = np.array([69, 71.7, 73.1, 193, 205, 210,73,205])*10**9  # Young's Moduli in GPa
thermal_expansion = np.array([23.6, 23.5, 22.2, 16.0, 13.0, 10.8, 23,11.2])*10**-6  # Thermal expansion coefficients in 1/K
densities = np.array([2700, 2810, 2780, 8000, 8190, 8000,2780,7850])  # Density in kg/m^3

material_properties = np.vstack((Material_names, E_moduli, normal_yield, shear_yield,thermal_expansion,densities)).T

Force1 = np.array([442.2, 1400.25 + 280, 442.2])  # Force vector in 3D [Fx, Fy, Fz]
Moment1 = np.array([15.25, 0, 0])  # Moment vector in 3D [Mx, My, Mz] 280
r_force = [0,0.075, 0]
loadcase1 = np.vstack((Force1, Moment1, r_force)) 


Force2 = np.array([589.6, 442.2 + 88, 589.6])  # Force vector in 3D [Fx, Fy, Fz]
Moment2 = np.array([15.25, 0, 0])  # Moment vector in 3D [Mx, My, Mz] 88
r_force = [0,0.075, 0]
loadcase2 = np.vstack((Force2, Moment2,r_force))

loadcases = np.array([loadcase1, loadcase2])
#print(loadcases)

Diameters  = np.array([
	1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.7, 1.7, 1.8, 1.8, 1.8, 1.8,
	2, 2, 2, 2, 2.2, 2.2, 2.2, 2.2, 2.3, 2.3, 2.3, 2.3, 2.5, 2.5,
	2.5, 2.5, 2.6, 2.6, 3, 3, 3, 3, 3.5, 3.5, 3.5, 3.5, 4, 4, 4, 4,
	4.5, 4.5, 4.5, 4.5, 5, 5, 5, 5, 5.5, 5.5, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9,
	9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11,
	11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
	14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 16,
	16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17,
	18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18
])*10**(-3)
Diameters_minor = np.array([
	1.1385, 1.15, 1.207, 1.2155, 1.323, 1.332, 1.2385, 1.25, 1.3385,
	1.35, 1.523, 1.532, 1.478, 1.4905, 1.6605, 1.6705, 1.6165, 1.6295,
	1.8605, 1.8705, 1.7165, 1.7295, 1.778, 1.7905, 1.9165, 1.9295,
	2.0385, 2.05, 2.0165, 2.0295, 2.3555, 2.369, 2.5365, 2.549, 2.732,
	2.748, 3.0365, 3.049, 3.111, 3.128, 3.3555, 3.369, 3.5525, 3.5695,
	3.8555, 3.869, 3.9895, 4.007, 4.3555, 4.369, 4.848, 4.865, 4.7435,
	4.764, 4.997, 5.012, 5.0475, 5.066, 5.1085, 5.126, 5.3505, 5.3665,
	5.7435, 5.764, 6.0475, 6.066, 6.3505, 6.3665, 6.4455, 6.467, 6.7435,
	6.764, 6.984, 7.0035, 7.0475, 7.066, 7.3505, 7.3665, 7.4455, 7.467,
	7.7435, 7.764, 8.0475, 8.066, 8.3505, 8.3665, 8.141, 8.1645, 8.4455,
	8.467, 8.5995, 8.621, 8.7435, 8.764, 9.0475, 9.066, 9.3505, 9.3665,
	9.141, 9.1655, 9.7435, 9.764, 10.0475, 10.066, 10.3505, 10.3665,
	9.8365, 9.864, 10.137, 10.4385, 10.462, 10.7405, 10.762, 11.0445,
	11.064, 11.348, 11.3645, 11.534, 11.564, 12.137, 12.162, 12.4385,
	12.462, 12.7405, 12.7625, 13.0445, 13.064, 13.348, 13.3645, 13.137,
	13.162, 13.7405, 13.762, 13.534, 13.564, 14.037, 14.0565, 14.137,
	14.162, 14.4385, 14.462, 14.7405, 14.762, 15.0445, 15.064, 15.348,
	15.365, 15.137, 15.162, 15.7405, 15.762, 14.938, 14.97, 15.534,
	15.564, 16.137, 16.162, 16.4385, 16.462, 16.7405, 16.762, 17.0445,
	17.064, 17.348, 17.365
])*10**(-3)
d_head = Diameters * 1.5

diameterscondensed = np.vstack((Diameters, Diameters_minor, d_head)).T
#actually too many diameters. lets take an 8th of them
diameterscondensed = diameterscondensed[::16]
print("diameterslength",len(diameterscondensed))




def GetWeight(diameters, density_lug, density_wall, density_bolt, w, l,t2):
	weight = density_lug * w* l * t2  + density_bolt * np.pi / 4* diameters[0]**2 * t2 * len(diameters) * 1.1
	return weight


counter = 0
minweight = 100000
for w in widths:
	print("sth happened")
	for l in lengths:
		for diametercondensed in diameterscondensed[:]:
			for loadcase in [loadcases[1]]:
				for t2 in t2s:
					for t3 in t3s:
						for material_bolt in [material_properties[bolt_material-1]]:
							for material_lug in [material_properties[lug_material-1]]:
								for material_wall in [material_properties[wall_material-1]]:

									name_material_lug = material_lug[0]
									E_lug = material_lug[1]
									normal_yield_lug = material_lug[2]
									shear_yield_lug = material_lug[3]
									alpha_lug = material_lug[4]
									density_lug = material_lug[5]

									name_material_wall = material_wall[0]
									E_wall = material_wall[1]
									normal_yield_wall = material_wall[2] 
									shear_yield_wall = material_wall[3]
									alpha_wall = material_wall[4]
									density_wall = material_wall[5]

									name_material_bolt = material_bolt[0]
									E_bolt = material_bolt[1]
									normal_yield_bolt = material_bolt[2]
									shear_yield_bolt = material_bolt[3]
									alpha_bolt = material_bolt[4]
									density_bolt = material_bolt[5]

									F = loadcase[0]
									M = loadcase[1]
									r_force = loadcase[2]

									d_nom = diametercondensed[0]
									diameters_minor = diametercondensed[1]
									d_head = diametercondensed[2]


									positioncases =[]
									for i in range(1):
										for j in range(1):
											tempgrid = calculations_bolts.getGrid(i+2,j+2, w, d_nom, l, "metal")
											if tempgrid is not None:
												positioncases.append(tempgrid)
									
									for positions in positioncases:
										counter += 1
										diameters = np.full(positions.shape[0], d_nom)
										# calculating everything
										forces = calculations_bolts.get_forces(positions, diameters, F, r_force, M)

										fr = thermal.force_ratio(d_nom, diameters_minor, E_bolt, E_bolt, "Hexagon", t2, d_head, E_lug, t3, E_wall)

										thermal_force = thermal.thermalforces2materials(fr, E_bolt, d_nom, alpha_lug, t2, alpha_wall, t3, alpha_bolt)

										forces += np.array([0,thermal_force,0])

										inplane_normal_stresses = calculations_bolts.get_inplane_bearing_stress(forces, diameters, t2, t3)
										max_normal_stress_lug = np.max(inplane_normal_stresses[0])
										max_normal_stress_wall = np.max(inplane_normal_stresses[1])

										out_of_plane_shear_stresses = calculations_bolts.get_shear_stress(forces, diameters, t2, t3)
										max_shear_stress_lug = np.max(out_of_plane_shear_stresses[0])
										max_shear_stress_wall = np.max(out_of_plane_shear_stresses[1])

										inplane_safety = min(normal_yield_lug/max_normal_stress_lug, normal_yield_wall/max_normal_stress_wall)
										shear_safety = min(shear_yield_lug/max_shear_stress_lug, shear_yield_wall/max_shear_stress_wall)

										total_safety = min(inplane_safety, shear_safety)
										# if counter == 1:
										# 	print("forces",forces)
										# 	print("max shear",max_shear_stress_lug)
										# 	print("shear yield",shear_yield_lug)
										# 	print("ms", max_shear_stress_lug/shear_yield_lug)

										if total_safety > 1:
											weight = GetWeight(diameters, density_lug, density_wall, density_bolt, w, l, t2)
											if weight < minweight:

												minweight = weight
												
												print("weight", weight)
												print("safety", total_safety)
												print("t2", t2)
												print("t3", t3)
												print("w", w)
												print("l", l)
												print("diameter nom", d_nom)
												print("diameter minor", diameters_minor)
												print("diameter head", d_head)
												print("position matrix:")
												print(positions)
												print("material_lug", Material_namessss[int(name_material_lug)-1])
												print("material_wall", Material_namessss[int(name_material_wall)-1])
												print("name_material_bolt", Material_namessss[int(name_material_bolt)-1])
												print("----------------------------------------------")						


												# print("counter",counter)
												# print("weight", weight)
												# print("safety", total_safety)
												# print("forces",forces)
												# print("thermalforce",thermal_force)
												# print(positions.shape)
												# print(positions)
												# print(diameters[0], w, l)
												# print("name_material_lug, name_material_wall, name_material_bolt, loadcase, t2, t3, diametercondensed, w, l")
												# print(name_material_lug, name_material_wall, name_material_bolt, loadcase, t2, t3, diametercondensed, w, l)