set r4010a [atomselect 1 "name GL0 and (x^2 + y^2 <= 4900)"]
set r4050a [atomselect 2 "name GL0 and (x^2 + y^2 <= 4900)"]
set r6010a [atomselect 3 "name GL0 and (x^2 + y^2 <= 8100)"]
set r6050a [atomselect 4 "name GL0 and (x^2 + y^2 <= 8100)"]
set r8510a [atomselect 5 "name GL0 and (x^2 + y^2 <= 11025)"]
set r8550a [atomselect 6 "name GL0 and (x^2 + y^2 <= 11025)"]

set r4010b [atomselect 1 "name GL0 and (x^2 + y^2 <= 4900) and (x^2 + y^2 >= 100)"]
set r4050b [atomselect 2 "name GL0 and (x^2 + y^2 <= 4900) and (x^2 + y^2 >= 100)"]
set r6010b [atomselect 3 "name GL0 and (x^2 + y^2 <= 8100) and (x^2 + y^2 >= 900)"]
set r6050b [atomselect 4 "name GL0 and (x^2 + y^2 <= 8100) and (x^2 + y^2 >= 900)"]
set r8510b [atomselect 5 "name GL0 and (x^2 + y^2 <= 11025) and (x^2 + y^2 >= 3025)"]
set r8550b [atomselect 6 "name GL0 and (x^2 + y^2 <= 11025) and (x^2 + y^2 >= 3025)"]

set resl4010a [$r4010a get resid]
set resl4050a [$r4050a get resid]
set resl6010a [$r6010a get resid]
set resl6050a [$r6050a get resid]
set resl8510a [$r8510a get resid]
set resl8550a [$r8550a get resid]

set resl4010b [$r4010b get resid]
set resl4050b [$r4050b get resid]
set resl6010b [$r6010b get resid]
set resl6050b [$r6050b get resid]
set resl8510b [$r8510b get resid]
set resl8550b [$r8550b get resid]

set numFrame4010 [molinfo 1 get numframes] 
set numFrame4050 [molinfo 2  get numframes] 
set numFrame6010 [molinfo 3  get numframes] 
set numFrame6050 [molinfo 4  get numframes] 
set numFrame8510 [molinfo 5  get numframes] 
set numFrame8550 [molinfo 6  get numframes] 


proc count {inputArray} {
	llength $inputArray
}

set reslLista [list $resl4010a $resl4050a $resl6010a $resl6050a $resl8510a $resl8550a]
set reslListb [list $resl4010b $resl4050b $resl6010b $resl6050b $resl8510b $resl8550b]

set flag 0 
while {$flag < 6} {
	puts " "
	set ca [count [lindex $reslLista $flag]]
	puts $ca
	set cb [count [lindex $reslListb $flag]]
	puts $cb	
	incr flag	
}


#set resl4010Input [$r4010 frame $numFrame4010]
#set resl4050Input [$r4050 frame $numFrame4050]
#set resl6010Input [$r6010 frame $numFrame6010]
#set resl6050Input [$r6050 frame $numFrame6050]
#set resl8510Input [$r8510 frame $numFrame8510]
#set resl8550Input [$r8550 frame $numFrame8550]
