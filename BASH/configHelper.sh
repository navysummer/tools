#!/usr/bin/bash
getLine(){
    file=$1
    section=$2
    option=$3
    tl=$(cat $file | wc -l)
    lines=$(sed -n -e "/$section/=" $file)
    tn=0
    lindedata=''
    for i in $lines
    do
        nlines=$(cat $file | awk -v i=$i '/^\[.*\]$/ {if(NR>i)print NR}')
        nline=$(echo $nlines | awk '{print $1}')
        if [ -n $nline ]
        then
            sl=$((i+1))
            el=$((nline-1))
            if [ $el -eq -1 ]
            then
                el=$tl
            fi
            #echo $tl $nline
            if [ $((tl-nline)) -ge 0 ]
            then
                rs=$(cat $file | head -n $el | tail -n "+"$sl | grep -n '^'$option | tail -n 1)
                #echo $rs
                flag=$(awk -v a="$rs" -v b=":" 'BEGIN{print index(a,b)}')
                if [ $flag -ne 0 ]
                then
                    px=$(echo $rs | awk -F ':' '{print $1}')
                    tn=$((i+px))
                fi
            fi
        fi
    done
    return $tn

}
getConfig(){
    file=$1
    section=$2
    option=$3
    getLine $file $section $option
    line=$?
    #echo $line
    content=$(cat $file | awk '{if(NR=="'$line'"){print}}')
    #echo $content
    value=$(echo $content | awk -F '=' '{print $2}')
    #echo $value

}

alterConfig(){
    file=$1
    section=$2
    option=$3
    rvalue=$4
    getConfig $file $section $option
    str=$line's/'$value'/'$rvalue'/'
    sed -i "$str" $file
}
getConfig test.conf comon files
echo $line $value 
alterConfig test.conf comon files best
#echo $line $value
getConfig test.conf comon files
echo $line $value
