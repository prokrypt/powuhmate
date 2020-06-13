#!/bin/bash  
addr="00:12:92:08:2E:31"
 
#LED values behavior:
# 00 to 7F: ?
# 80: completely off
# 81: completely on
# 82 to 9F: no change?
# A0: quick blink then low intensity
# A1 to BF: from low to high intensity
# C0 to FF: blinking at different speeds

ledon=A0
ledoff=80
mode="Media"

Global(){
	case $1 in
		77) echo Test;;
	esac
}
Scroll(){
	case $1 in
		68) echo CW; xdotool mousedown 4 mouseup 4;;
		67) echo CCW; xdotool mousedown 5 mouseup 5;;
		65) echo Press; xdotool key space; read -t 0.1 ;; #eat double-presses
		70) echo PCW; xdotool key XF86AudioRaiseVolume;;
		69) echo PCCW; xdotool key XF86AudioLowerVolume;;
		72) echo Hold 1.0s;;
		73) echo Hold 1.5s;;
		74) echo Hold 2.0s;;
		75) echo Hold 2.5s;;
		76) echo Hold 3.0s;;
		77) echo Hold 3.5s;;
		66) echo Release; read;;
		*) echo "Unknown value: $value"
	esac
}
Media(){
	case $1 in
		70) echo PCW; xdotool mousedown 4 mouseup 4;;
		69) echo PCCW; xdotool mousedown 5 mouseup 5;;
		65) echo Press; xdotool key space; read -t 0.1 ;; #eat double-presses
		68) echo CW; xdotool key XF86AudioRaiseVolume;;
		67) echo CCW; xdotool key XF86AudioLowerVolume;;
		72) echo Hold 1.0s;;
		73) echo Hold 1.5s;;
		74) echo Hold 2.0s;;
		75) echo Hold 2.5s;;
		76) echo Hold 3.0s;;
		77) echo Hold 3.5s;;
		66) echo Release; read;;
		*) echo "Unknown value: $value"
	esac
}

batt='xx'
while true; do
gatttool -b $addr --char-write-req -a 0x0029 -n $ledon > /dev/null && #set led
gatttool -b $addr -a 0x0026 --char-write-req --value 0000 > /dev/null && #battery monitor
gatttool -b $addr -a 0x002d --char-write-req --value 0100 --listen | { #event monitor
read -t1
echo "Connected"
while read -t300 _ _ _ handle _ value; do
#	echo handle: $handle, value: $value;
	case $handle in
		0x002c) echo -n "$batt%> ";
			$mode $value
			Global $value;;
		0x0025) batt=$((16#$value)); ;; #echo "Battery update: $batt%";;
		*) echo "Unknown handle: $handle with value: $value"
	esac
done
echo "Derp. Le reset"
killall gatttool
}
done
