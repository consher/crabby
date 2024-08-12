#set -x


#flags
while getopts "hd:s:" opt; do
 case $opt in
        h) #display help
          echo ""
          echo "Voltage to Filterbank converter for I-LOFAR observations. Made by Sai & ammended by Conor"
          echo "(Note that the .fil is written to the same directory of the script - ensure you have at least x4 the size o
f the .zst files for space)"
          echo "Options:"
          echo "-h              Display this help message"
          echo "-d DIRECTORY    Searches given directory for volatges in *.zst format"
          echo "-s SRCS         Input name,DM,no. polarizations on the source to be processed in the form 'NAME DM POLS'"
          echo "                Default is crab pulsar 'B0531+21 56.7712 4'"
          echo ""
          exit 1
        ;;
        d)
          search="$OPTARG"
        ;;
        s) #SRC input
          srcs=("$OPTARG")
        ;;
        \?)
          echo "Invalid option: -$OPTARG"
          exit 1
        ;;
        :)
          echo "Option -$OPTARG requires an argument."
          exit 1
        ;;
 esac
done

#lastDir="$(find ${search} -maxdepth 1 -type d -name "20*" | sort | tail -n 1)"
#inputDir="${1:-${lastDir}}"/
inputDir="${search}"

echo "Searching for files in ${inputDir}"

srcs=("B0531+21 56.7712 4")

prefix="udp_1613%d.ucc1."
checkPort="16130"
splitText="udp_16130.ucc1."
suffix=".zst"

for ((i = 0; i < ${#srcs[@]}; i++)); do
        src=( ${srcs[$i]} )
        name="${src[0]}"
        backupdm=$(psrcat -c dm -x $name | awk '{print $1}')
        dm="${src[1]:-$backupdm}"
        dsfact="${src[2]:-4}"
        if [ "$dm" == "WARNING:" ]; then
                echo "Unable to find DM for $name, exiting.";
                print "\n\n\n";
                exit;
        fi;

        paths=($(ls --directory -1a ${inputDir} 2>/dev/null))
        echo "${src}" "${dm}" "${dsfact}" "${paths}"
        if [ ! -z "${paths}" ]; then
                echo "Searching ${paths}"
                for path in "${paths[@]}"; do
                        echo "Observation at ${path}"
                        filename=$(ls -1a ${path}/${splitText}*${suffix} | sort | head -n 1)
                        if [ ! -f "${filename}" ]; then
                                echo "Input file not found at ${filename} (${path}), continuing."
                                continue
                        fi
                        lastModified=$(stat -c %Z "${filename}")
                        timestr=$(echo "${filename}" | awk -F'/' '{print $NF}' | sed "s/${splitText}//g" | sed "s/${suffix}
//g")
                        touch output_"${src}"_"${timestr}".log
                        let currTime=$(date +%s)-10
                        if [ ${currTime} -lt ${lastModified} ]; then
                                echo "$src at $path is still being modified, not processing yet.";
                                continue;
                        fi;
                        if [ -f "${src}_${timestr}.fil" ]; then
                                echo "${src} at ${path} has already been processed, continuing.";
                                continue
                        fi;
                        #echo "procrun ${prefix} ${timestr} ${name} ${dm} ${dsfact}"
                        echo bash combined_cmd "${prefix}" "${timestr}" "${name}" "${dm}" "${dsfact}" "${inputDir}"
                        bash combined_cmd "${prefix}" "${timestr}" "${name}" "${dm}" "${dsfact}" "${inputDir}"
                done;
        fi;
done

find . -type f -empty | while read fil; do mv ${fil} ${fil}_empty; done

while pgrep -x "digifil" >/dev/null; do
        echo "It is currently $(date). There are still $(pgrep -x "digifil" | wc -l) processes running."
        sleep 300;
done;

#sleep 1200

chown -R 1000:1000 .