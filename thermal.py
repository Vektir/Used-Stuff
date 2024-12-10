import numpy as np

def compliancE_bolt(d_nom, d_minor, E_bolt, E_nut,ht,t_2,t_3):
	#d_nom - nominal diameter of the fastener (from the standard specs)
	#d_minor - minor diameter of the fastener (from the standard specs)
	#t1 - thickness of the lug (from previous design steps)
	#t2 - thickness of the spacecraft wall (from prevoius work packedges*)
	#E_bolt, E_nut - youngs modulus of the bolt and nut
	#ht - head type (Hexagon or cylindrical)
	#st - shank type (nut tightened or threaded hole)

	if ht=="Hexagon":
		Lh=0.5*d_nom
	else:
		Lh=0.4*d_nom


	Ls=0.4*d_nom

	Ls=0.33*d_nom

	Ln=0.4*d_nom
	A_nom=np.pi*d_nom**2/4
	A_min=np.pi*d_minor**2/4


	com_b=(Lh/A_nom+Ls/A_min+(t_2+t_3)/A_nom)/E_bolt+Ln/E_nut/A_nom

	return com_b

def compliance_a(t,D_Head,D_in,E_a):
	#t thickness of the plate
	#D_Head diameter of the head
	#D_in diameter of the shank
	#E_a young modulus of the attached part (lug plate or the s/c wall)
	com_a=4*t/(E_a*np.pi*(D_Head**2-D_in**2))

	return com_a

def force_ratio(d_nom, d_minor, E_bolt, E_nut,ht,t_2,D_Head,E_lug,t_3,E_wall):
	# t_2 - thickness of the lug (from previous design steps)
	# t_3 - thickness of the spacecraft wall (from prevoius work packedges*)
	# E_lug - young modulus of the plate
	# E_wall - young modulus of the wall

	fr=(compliance_a(t_2,D_Head,d_nom,E_lug)+compliance_a(t_3,D_Head,d_nom,E_wall))/(compliance_a(t_2,D_Head,d_nom,E_lug)+compliance_a(t_3,D_Head,d_nom,E_wall)+compliancE_bolt(d_nom,d_minor, E_bolt, E_nut,ht,t_2,t_3))

	return fr



def thermalforces2materials(fr, E_bolt, d, alpha_lug, t_lug, alpha_wall, t_wall, alpha_bolt):
	Tmin = -90
	Tmax = 76.1
	Tref = 15
	DeltaTmin = Tmin - Tref
	DeltaTmax = Tmax - Tref
	alpha_lug_wall = (alpha_lug*t_lug + alpha_wall*t_wall)/(t_lug + t_wall)
	# alpha c - coefficient of wall, lug  somewhat accurate
	# alpha b - coefficient of Bolt, nut

	#d#diameter of the shank
	A = np.pi / 4 * d**2 #stiffness area of the fastener

	FdTmax = (alpha_lug_wall - alpha_bolt) * DeltaTmax * E_bolt * A * (1 - fr)
	FdTmin = (alpha_lug_wall - alpha_bolt) * DeltaTmin * E_bolt * A * (1 - fr)

	maxFT = max(FdTmax, FdTmin)
	return maxFT



#fr = force_ratio(d_nom=.008, d_minor=.0062, E_bolt=200e9, E_nut=70e9,ht="Hexagon",t_2=.0001,D_Head=.010,E_lug=70e9,t_3=.0001,E_wall=70e9)
#thermalforce = thermalforces2materials(fr, E_bolt=200e9, d=.008, alpha_lug=23e-6, t_lug=.0001, alpha_wall=23e-6, t_wall=.0001, alpha_bolt=11e-6)

#print("force", thermalforce)