
#!/bin/sh

set -e
#################
#   TEST        #
#################

if [ 0 -eq 1 ]
then
DIALOG_SIZE="15 50"
BACKTITLE="Welcome to Pengrix Desktop installation!"
TEMP="/tmp/pengrix-install.tmp"
SUBTITLE="Pengrix Desktop Configuration"
MESSAGE=""
INPUT=""
STRING=""
LIST=""

unitCalculate() {
    size=$1
    NEGATIVE=1

    # byte to Kb / Mb/ Gb 
    div=1000
    if [ ${size} -lt 0 ]       # negative
    then
	NEGATIVE=0
	size=-${size}
    fi

    if [ ${size} -eq 0 ]
    then
	trans=${size}
    else 
	if [ `expr ${size} / ${div}` -lt 1 ]
	then
	    trans="${size}bytes"
	elif [ `expr ${size} / \( ${div} \* ${div} \)` -lt 1 ]
	then
	    trans="`expr ${size} / ${div}`KB"
	elif [ `expr ${size} / \( ${div} \* ${div} \* ${div} \)` -lt 1 ]
	then
	    trans="`expr ${size} / \( ${div} \* ${div} \)`MB"
	elif [ `expr ${size} / \( ${div} \* ${div} \* ${div} \* ${div} \)` -lt 1 ]
	then
	    trans="`expr ${size} / \( ${div} \* ${div} \* ${div} \)`GB"
	elif [ `expr ${size} / \( ${div} \* ${div} \* ${div} \* ${div} \* ${div} \)` -lt 1 ]
	then
	    trans="`expr ${size} / \( ${div} \* ${div} \* ${div} \)`TB"
	else
	    trans="${size}byte"
	fi
    fi

    if [ ${NEGATIVE} -eq 0 ]
    then
	trans=-${trans}
    fi

}

strstr() {
    [ "${1#*$2*}" = "$1" ] && return 1
    return 0
}

LIST=""
DEV_TEMP=""
PART_TOTAL=0
while read line 
do
    if strstr "${line}" "sd" 
    then
	GET_DEV=`echo ${line} |awk '{print $4}'`
	echo ${GET_DEV}
	if [ `expr length ${GET_DEV}` -eq 3 ]
	then
	    if [ "${DEV_TEMP}" = "" ]
	    then
		DEV_TEMP=${GET_DEV}
		DEV_SIZE=`echo ${line} |awk '{print $3}'`
	    else
		echo 1111111111
		DEV="/dev/${DEV_TEMP}(Free/Total)"
		if [ ${PART_TOTAL} -eq 0 ]
		then
		   USED_BYTES=0 
		else
		    USED_BYTES=`expr ${PART_TOTAL} \* 1024`
		fi
		TOTAL_BYTES=`expr ${DEV_SIZE} \* 1024`
		FREE_BYTES=`expr ${TOTAL_BYTES} - ${USED_BYTES}`

		unitCalculate ${FREE_BYTES}
		FREE_SIZE=${trans}
		unitCalculate ${TOTAL_BYTES}
		TOTAL_SIZE=${trans}
		LINE="${DEV} ${FREE_SIZE}/${TOTAL_SIZE} off"
		LIST="${LIST} ${LINE}"

		DEV_TEMP=${GET_DEV}
		DEV_SIZE=`echo ${line} |awk '{print $3}'`
		PART_TOTAL=0
	    fi
	else
	    PART_TEMP=${GET_DEV}
	    PART_SIZE=`echo ${line} |awk '{print $3}'`
	    PART_TOTAL=`expr ${PART_TOTAL} + ${PART_SIZE}`

	    PART="/dev/${PART_TEMP}"
	    BYTES=`expr ${PART_SIZE} \* 1024`
	    unitCalculate ${BYTES}
	    SIZE=${trans}
	    LINE="${PART} ${SIZE} off"
	    LIST="${LIST} ${LINE}"
	fi
	echo ${LIST}
    fi
done < /proc/partitions

echo ${LIST}

DEV="/dev/${DEV_TEMP}(Free/Total)"
if [ ${PART_TOTAL} -eq 0 ]
then
    USED_BYTES=0 
else
    USED_BYTES=`expr ${PART_TOTAL} \* 1024`
fi
TOTAL_BYTES=`expr ${DEV_SIZE} \* 1024`
FREE_BYTES=`expr ${TOTAL_BYTES} - ${USED_BYTES}`

unitCalculate ${FREE_BYTES}
FREE_SIZE=${trans}
unitCalculate ${TOTAL_BYTES}
TOTAL_SIZE=${trans}
LINE="${DEV} ${FREE_SIZE}/${TOTAL_SIZE} off"
LIST="${LIST} ${LINE}"

echo ${LIST}

whiptail --title "${SUBTITLE}" --backtitle "${BACKTITLE}" --checklist "${MESSAGE}" ${DIALOG_SIZE} 10 ${LIST} 2>${TEMP}
EXIT=`echo $?`
if [ ${EXIT} -eq 1 ]
then
    exit
else
    INPUT=`cat ${TEMP}`
    rm -f ${TEMP}
fi

echo ${INPUT}


LIST=""

while read line 
do
    if strstr "${line}" "sd" 
    then
	TEMP_DEV=`echo ${line} |awk '{print $4}'`
	TEMP_SIZE=`echo ${line} |awk '{print $3}'`
	DEV="/dev/${TEMP_DEV}"
	BYTES=`expr ${TEMP_SIZE} \* 1024`
	unitCalculate ${BYTES}
	SIZE=${trans}
	LINE="${DEV} ${SIZE} off"
	LIST="${LIST} ${LINE}"
    fi
done < /proc/partitions

echo ${LIST}
    
whiptail --title "${SUBTITLE}" --backtitle "${BACKTITLE}" --checklist "${MESSAGE}" ${DIALOG_SIZE} 10 ${LIST} 2>${TEMP}
EXIT=`echo $?`
if [ ${EXIT} -eq 1 ]
then
    exit
else
    INPUT=`cat ${TEMP}`
    rm -f ${TEMP}
fi

echo ${INPUT}

fi
