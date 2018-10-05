# 16 April 2018, Moeen Meigooni
# usage: 
# if using structures straight from charmmgui:
#     copy charmm-gui folder into dir
#     set from_charmmgui to True
#     python make_cg_lipid.py
# if using other structures i.e. building out of patches from charmmgui:
#     mkdir 00-system
#     name custom structure lipid.pdb, lipid.psf and place in 00-system
#     set from_charmmgui to False
#     python make_cg_lipid.py
#########################################################################

import os

# user defined var
sys = 'het_CDL1_20'
from_charmmgui = True      # is structure file coming straight from charmm-gui?
solvent_x_dir = 0          # plus or minus solvation direction
solvent_y_dir = 0
solvent_z_dir = 50
spdb = '/Scr/meigoon2/curve/cg/files/02-solvate-ionize/cg-waterbox/cgwaterbox-90W-10WAF-100A-QQQ.pdb'
spsf = '/Scr/meigoon2/curve/cg/files/02-solvate-ionize/cg-waterbox/cgwaterbox-90W-10WAF-100A-QQQ.psf'
stop = '/Scr/meigoon2/curve/cg/files/04-cgc-top-par-files/martini-top/martini-water.top'
params = ['martini_v2.2.namd.prm',
			'martini_CDL1.par',
			'martini_DOPC.par']
prod1_run = 10000000 # 200 ns


os.system('mkdir 00-system 01-solvate-ionize 02-mineq 03-prod')

# 00
if from_charmmgui:
	os.system('cp charmm-gui/step4_lipid.pdb 00-system/lipid.pdb')
	os.system('cp charmm-gui/step4_lipid.psf 00-system/lipid.psf')

# 01
os.chdir('01-solvate-ionize')
os.system('cp /Scr/meigoon2/curve/cg/files/04-cgc-top-par-files/martini-top/martini-ions.top .')
with open('solvate-ionize.tcl', 'w') as f:
	f.write('source /Scr/meigoon2/curve/cg/files/05-scripts/solvate.tcl \n')
	if solvent_x_dir == 0 and solvent_y_dir == 0:
		f.write('solvate ../00-system/lipid.psf ../00-system/lipid.pdb -o lipid_water -s W -b 5 -z %i +z %i -spsf %s -spdb %s -stop %s -ks "name W WAF" -ws 100 \n'%(solvent_z_dir, solvent_z_dir, spsf, spdb, stop))
	elif solvent_x_dir != 0 and solvent_y_dir == 0:
		f.write('solvate ../00-system/lipid.psf ../00-system/lipid.pdb -o lipid_water -s W -b 5 -x %i -z %i +x %i +z %i -spsf %s -spdb %s -stop %s -ks "name W WAF" -ws 100 \n'%(solvent_x_dir, solvent_z_dir, solvent_x_dir, solvent_z_dir, spsf, spdb, stop))
	else:
		f.write('solvate ../00-system/lipid.psf ../00-system/lipid.pdb -o lipid_water -s W -b 5 -x %i -y %i -z %i +x %i +y %i +z %i -spsf %s -spdb %s -stop %s -ks "name W WAF" -ws 100 \n'%(solvent_x_dir, solvent_y_dir, solvent_z_dir, solvent_x_dir, solvent_y_dir, solvent_z_dir, spsf, spdb, stop))
	f.write('\n')
	f.write('source /Scr/meigoon2/curve/cg/files/05-scripts/cg-ionize.tcl \n')
	f.write('autoionize -psf lipid_water.psf -pdb lipid_water.pdb -sc 0.15 -o lipid_water_ions \n')
	f.write('\n')
	f.write('set all [atomselect top all] \n')
	f.write('set minmax [measure minmax $all] \n')
	f.write('puts "cellBasisVector1 [expr {[lindex [lindex $minmax 1] 0] - [lindex [lindex $minmax 0] 0]}] 0 0" \n')
	f.write('puts "cellBasisVector2 0 [expr {[lindex [lindex $minmax 1] 1] - [lindex [lindex $minmax 0] 1]}] 0" \n')
	f.write('puts "cellBasisVector3 0 0 [expr {[lindex [lindex $minmax 1] 2] - [lindex [lindex $minmax 0] 2]}]" \n')
	f.write('puts "cellOrigin [measure center $all weight none]" \n')
	f.write('exit \n')
	f.write('\n')
with open('run.sh', 'w') as f:
	f.write('vmd -dispdev text -e solvate-ionize.tcl > solvate-ionize.log & \n')
	f.write('wait \n')
os.system('chmod +x run.sh')
os.system('./run.sh')
os.chdir('..')

# 02
os.chdir('02-mineq')
os.system('mkdir output')
pbcs = []
with open('../01-solvate-ionize/solvate-ionize.log', 'r') as f:
	w = f.readlines()
for wi in w:
	if wi[0:4] == 'cell':
		pbcs.append(wi)
with open('mineq.namd', 'w') as f:
	f.write("""#############################################################
## JOB DESCRIPTION                                         ##
#############################################################
#
# Initial minimization and equilibration of the coarse-grained system.
#
#############################################################
## ADJUSTABLE PARAMETERS                                   ##
#############################################################
set outputname  output/mineq
set restart 0
set temperature    310
cosAngles          on

structure        ../01-solvate-ionize/lipid_water_ions.psf
coordinates      ../01-solvate-ionize/lipid_water_ions.pdb

temperature      $temperature

firsttimestep   0

#############################################################
## SIMULATION PARAMETERS                                   ##
#############################################################

# Input
paraTypeCharmm      on
""")
	for param in params:
		f.write('parameters             ../toppar/%s \n'%param)
	f.write("""
# Force-Field Parameters
exclude             1-2
1-4scaling          1.0
cutoff              12.0
martiniSwitching    on
switching           on
PME                 off
switchdist          9.0
pairlistdist        14.0
dielectric          15.0

# Integrator Parameters
timestep            20.0
nonbondedFreq       1
stepspercycle       10

# Constant Temperature Control
langevin            yes    ;# do langevin dynamics
langevinDamping     1      ;# damping coefficient (gamma) of 1/ps
langevinTemp        $temperature
langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

# Periodic Boundary Conditions
if {$restart == 0} {
""")
	for pbc in pbcs:
		f.write(pbc)
	f.write("""}
wrapAll             on

# Constant Pressure Control (variable volume)
useGroupPressure      no
useFlexibleCell       yes
useConstantArea       no
useConstantRatio      yes

langevinPiston        yes
langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
langevinPistonPeriod  2000.  #usually 2000 for RBCG system
langevinPistonDecay   1000.  #usually 1000 for RBCG system
langevinPistonTemp    $temperature

# Output
outputName          $outputname
restartfreq          1000
dcdfreq              1000
xstFreq              1000
outputEnergies       1000
outputPressure       1000

#############################################################
## EXECUTION SCRIPT                                        ##
#############################################################

if {$restart == 0} {
minimize             5000
reinitvels          $temperature
}

run 50000

""")
os.chdir('..')


# 03
os.chdir('03-prod')
os.system('mkdir output')
with open('prod1.namd', 'w') as f:
	f.write("""proc get_first_ts { xscfile } {
  set fd [open $xscfile r]
  gets $fd
  gets $fd
  gets $fd line
  set ts [lindex $line 0]
  close $fd
  return $ts
}

#############################################################
## JOB DESCRIPTION                                         ##
#############################################################
#
# Production simulation of the coarse-grained system.
#
#############################################################
## ADJUSTABLE PARAMETERS                                   ##
#############################################################
set outputname  output/prod1
set restart 1
set temperature    310
cosAngles          on

structure        ../01-solvate-ionize/lipid_water_ions.psf
coordinates      ../01-solvate-ionize/lipid_water_ions.pdb

if {$restart == 1} {
set inputname      ../02-mineq/output/mineq
binCoordinates     $inputname.restart.coor
binVelocities      $inputname.restart.vel  ;# remove the "temperature" entry if you use this!
extendedSystem     $inputname.restart.xsc
} else {
temperature $temperature
}

set firsttime [get_first_ts $inputname.restart.xsc]
firsttimestep      $firsttime

#############################################################
## SIMULATION PARAMETERS                                   ##
#############################################################

# Input
paraTypeCharmm      on
""")
	for param in params:
		f.write('parameters             ../toppar/%s \n'%param)
	f.write("""
# Force-Field Parameters
exclude             1-2
1-4scaling          1.0
cutoff              12.0
martiniSwitching    on
switching           on
PME                 off
switchdist          9.0
pairlistdist        14.0
dielectric          15.0

# Integrator Parameters
timestep            20.0
nonbondedFreq       1
stepspercycle       10

# Constant Temperature Control
langevin            yes    ;# do langevin dynamics
langevinDamping     1      ;# damping coefficient (gamma) of 1/ps
langevinTemp        $temperature
langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

# Periodic Boundary Conditions
if {$restart == 0} {
cellBasisVector1   279.00  0        0
cellBasisVector2   0       271.76   0
cellBasisVector3   0       0        163.22
cellOrigin         -0.2923417091 1.4583858251 -0.1471934169
}
wrapAll             on

# Constant Pressure Control (variable volume)
useGroupPressure      no
useFlexibleCell       yes
useConstantArea       yes
useConstantRatio      no

langevinPiston        yes
langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
langevinPistonPeriod  2000.  #usually 2000 for RBCG system
langevinPistonDecay   1000.  #usually 1000 for RBCG system
langevinPistonTemp    $temperature

# Output
outputName          $outputname
restartfreq          1000
dcdfreq              1000
xstFreq              1000
outputEnergies       1000
outputPressure       1000

#############################################################
## EXECUTION SCRIPT                                        ##
#############################################################

if {$restart == 0} {
minimize             5000
reinitvels          $temperature
}

run %i

"""%prod1_run)
os.chdir('..')


print('\nFinished!')

