import numpy as np


### Ignore these functions for now -----------------------------------------------------------------
def get_MS_inplane_bearing_stress(inplane_stresses, Bearing_stress_lug, Bearing_stress_wall):
	return np.vstack((Bearing_stress_lug/inplane_stresses[0], Bearing_stress_wall/inplane_stresses[1]))

# Returns the safety Margin of 	Each of these thingies
def get_MS_shear_stress(shear_stresses, shear_yield_lug, shear_yield_wall):
	return np.vstack((shear_yield_lug/shear_stresses[0], shear_yield_wall/shear_stresses[1]))
### Ignore these functions for now -----------------------------------------------------------------


def getGrid(rows, cols, width, diameter, length, material):
	edgedist = 1.5*diameter # distance from the edge of the grid to center of closest fastener
	fastdist = 3 * diameter # assume material is metal as it is the only one explored


	# Create the grid
	if cols%2 == 0:
		x = np.linspace(- length/2 + edgedist, - length/2 + edgedist + cols/2 * fastdist, cols//2)
		if x[-1] > 0 - fastdist/2:
			#print("too many columns")
			return
		x  = np.concatenate((x,-x))
	else:
		x = np.linspace(- length/2 + edgedist, - length/2 + edgedist + cols/2 * fastdist, cols//2)
		#print("pre",x)		
		if x[-1] > 0 - fastdist:
			#print("too many columns")
			return
		x = np.concatenate((x, [0], -x))
	
	y = np.linspace(- width/2 + edgedist, width/2 - edgedist , rows)
	#print(y)
	#print(x)
	if y[1] - y[0] < fastdist:
		#print("too many rows")
		return
		
	xx,yy = np.meshgrid(x,y, indexing = 'ij')
	grid = np.column_stack((xx.flatten(),yy.flatten()))
	grid = np.insert(grid, 1, 0, axis=1)
	return grid

# d,w,l = 0.0016, 0.0128, 0.0128
# print(getGrid(3,3,w,d,l,"metal"))

# Calculates the center of gravity of the fasteners
def cg_position(positions, diameters):
	areas = np.pi * (diameters / 2) ** 2  # Area of each fastener
	total_area = areas.sum()
	cg = (positions.T @ areas) / total_area  # Weighted average
	return cg  # Return as [x, y, z]

#Returns the vector distances of the fasteners from the origin.
def get_vector_distances(positions):
	return positions  # [[x, y, z]]

# Returns the scalar distances (magnitudes) of vectors.
def get_scalars(distances):
	return np.linalg.norm(distances, axis=1)

# Calculates force in each fastener to counteract the applied forces and moments
def get_forces(positions, diameters, F, r_force, M):
	
	"""
	Parameters:
		fasteners: Array of fasteners, each in the form [[x, y, z], d].
		F: Applied force vector [Fx, Fy, Fz].
		r_force: Location vector of the applied force.
		M: Moment vector [Mx, My, Mz].
	
	Returns:
		Array of forces per fastener in the form [[Fx, Fy, Fz], ...].
	"""
	areas = np.pi * (diameters / 2) ** 2
	cg = cg_position(positions,diameters)

	rel_distances = positions - cg
	scalar_distances = get_scalars(rel_distances)

	# Reaction forces to counteract the applied force
	F_react_force_1 = (F * areas[:, None]) / areas.sum()

	# Moment due to the applied force
	r_force_rel_cg = np.array(r_force) - cg
	Moment = np.cross(r_force_rel_cg, F) + M  # Moment is now a 3D vector: Mx, My, Mz

	# Forces to counteract the moment in the plane(cool formula)
	F_in_Plane = (
		areas[:, None] 
		* np.cross(Moment*np.array([0,1,0]), rel_distances)  # Cross product with the position relative to CG	
	) / (areas * scalar_distances**2).sum()

	# Same thing but out of plane (in the y direction)
	I_xx = (areas * rel_distances[:, 0]**2).sum()
	I_zz = (areas * rel_distances[:, 2]**2).sum()
	I_xz = (areas * rel_distances[:, 0] * rel_distances[:, 2]).sum()


	Fy = areas/(I_xx*I_zz - I_xz**2) * ((Moment[2]*I_zz- -Moment[0]*I_xz)*rel_distances[:,0] + (-Moment[0]*I_xx - Moment[2]*I_xz)*rel_distances[:,2])




	F_react_force_M = F_in_Plane + np.array([np.zeros(len(Fy)), Fy, np.zeros(len(Fy))]).T

	#print("forces in y direction", Fy)

	#print("distances",rel_distances)
	#print("moments",[np.cross(dist, force) for dist,force in zip(rel_distances, F_react_force_M)])

	return F_react_force_1 + F_react_force_M

#Example usage
"""
positions = np.array([[-2.25, 0, -2.25],
	[-2.25, 0, 2.25],
	[2.25, 0, -2.25],
	[2.25, 0, 2.25]])
diameters = np.array([.004, .004, .004, .004])

F = np.array([1, 2, 3])  # Force vector in 3D [Fx, Fy, Fz]
r_force = [0, 1, 0]  # Applied force location
M = np.array([0,3,0])  # Moment vector [Mx, My, Mz]

print(get_forces(positions, diameters, F, r_force, M))

Returns the in-plane bearing stress on the lug and wall in array format [lug, wall][fastener1, fastener2, ...]

"""

def get_inplane_bearing_stress(forces,diameters, t2, t3):
	lug_stresses = get_scalars(forces[:,[0,2]])/(diameters*t2)
	wall_stresses = get_scalars(forces[:,[0,2]])/(diameters*t3)
	
	return np.vstack((lug_stresses, wall_stresses))

# Returns the safety Margin of 	Each of these thingies
	
# Returns the shear stress on the wall and the lug in array format [lug, wall][fastener1, fastener2, ...]
def get_shear_stress(forces, diameters, t2, t3):
	shearlug = forces[:,1]/(diameters*np.pi*t2)
	shearwall = forces[:,1]/(diameters*np.pi*t3)
	return np.vstack((shearlug, shearwall))





# # Example Usage
# fasteners = [
# 	[[-2.25, 0, -2.25], .004],
# 	[[-2.25, 0, 2.25], .004],
# 	[[2.25, 0, -2.25], .004],
# 	[[2.25, 0, 2.25], .004]
# 	# [[-9, 0, 1], 1],
# 	# [[1, 0, -5], 2]
# ]

# # F = np.array([1, 2, 3])  # Force vector in 3D [Fx, Fy, Fz]
# # r_force = [0, 1, 0]  # Applied force location
# # M = np.array([0,3,0])  # Moment vector [Mx, My, Mz]
# t2 = .2 # thickness of the lug at connection
# t3 = .2 # thickness of the wall

# # # set based on 2 materials
# E_wall = 70e9
# # Bearing_stress_wall = 70e6
# # Yield_shear_wall = 70e6
# E_lug = 70e9
# # Bearing_stress_lug = 70e6
# # Yield_shear_lug = 70e6

# E_bolt = E_nut = 70e9

# # # Moments and forces are in same direction as applied force (they represent the force the structure applies on the fasteners)
# # # For many forces, do superposition of this function (everything is nice and linear (i think))
# # #print(get_forces(fasteners, F, r_force, M))
# # forces = get_forces(fasteners, F, r_force, M)


# # inplane_normal_stresses = get_inplane_bearing_stress(forces, fasteners, t2,t3)
# # max_normal_stress_lug = np.max(inplane_normal_stresses[0])
# # max_normal_stress_wall = np.max(inplane_normal_stresses[1])


# # out_of_plane_shear_stresses = get_shear_stress(forces, fasteners, t2, t3)
# # max_shear_stress_lug = np.max(out_of_plane_shear_stresses[0])
# # max_shear_stress_wall = np.max(out_of_plane_shear_stresses[1])



# # print(forces)
# # print(inplane_normal_stresses)
# # print(out_of_plane_shear_stresses)

# # margin_inplane = get_MS_inplane_bearing_stress(inplane_normal_stresses, Bearing_stress_lug, Bearing_stress_wall)
# # margin_shear = get_MS_shear_stress(out_of_plane_shear_stresses, Yield_shear_lug, Yield_shear_wall)

# d_nom = fasteners[0][1]
# #print("d_nom",d_nom)
# d_minor = .8
# ht = "Hexagon"
# D_out = 1.2 * d_nom

# alphac1 = 1.2e-5

# alphac2 = 1.2e-5
# alphab = 2e-5


# PhiBolts = boltratios.force_ratio(d_nom, d_minor, E_bolt, E_nut, ht, t2, D_out, E_lug, t3, E_wall)
# print(fasteners[0][1])
# Thermal_stress = thermal.thermalforces2materials(PhiBolts, E_bolt, fasteners[0][1], alphac1,t2, alphac2,t3, alphab)


# print("PhiBolts", PhiBolts)
# print("Thermal Stress", Thermal_stress)
# 												###fr, E_b, d, alphac1, t_lug, alphac2, t_wall, alphab
# Thermal_stress = max(Thermal_stress)

# max_normal_stress_lug += Thermal_stress
# max_normal_stress_wall += Thermal_stress 


# print("Thermal Stress", Thermal_stress)