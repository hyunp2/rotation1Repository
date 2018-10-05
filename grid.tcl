proc cylinder {length radius center density} {
 	set pi 3.1415926535897931
 	
	set delta_d [expr {sqrt(1.0 / $density)}]
	set delta_a [expr {$delta_d / $radius}]

	set points {}

	set Z_Min [expr {0 - $length / 2.0}]
	set Z_max [expr {0 + $length / 2.0}]

	set z $Z_Min

    while {$z < $Z_max} {
    	set theta 0 
    	while {$theta < [expr {2 * $pi}]} {
    		set x [expr {[lindex $center 0] + $radius * cos($theta)}]
    		set y [expr {[lindex $center 1] + $radius * sin($theta)}]
    		lappend points [list $x $y $z]
    		set theta [expr {$theta + $delta_a}]
    	    }
    	set z [expr {$z + $delta_d}]    	
    }

    return $points
 }
# convert points to DX file
proc makeDX {pointsList resolution outprefix} {

    set natoms [llength $pointsList]
    set molid [mol new atoms $natoms]
    animate dup $molid

    for {set i 0} {$i < $natoms} {incr i} {
        set sel [atomselect $molid "index $i"] 

        $sel set {x y z} [list [lindex $pointsList $i]]
        $sel delete
    }

    set sel [atomselect $molid all]
    $sel set name H
    $sel set element H
    $sel set radius 10.0
    mol reanalyze $molid

    mdff sim $sel -o ${outprefix}.dx -res $resolution
    mdff griddx -i ${outprefix}.dx -o ${outprefix}.dx

    $sel delete
    mol delete $molid
}


set cylinder_center  [list 0 0 0]
set density  0.1 
set radius  40
set length 162
set outfileprefix [format grid]


set CYLINDER [cylinder $length $radius $cylinder_center $density]

makeDX $CYLINDER 50.0 $outfileprefix

