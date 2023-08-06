#!/bin/bash
#
# Calculates Video Quality Indicators (VQIs) on the file given as the argument 
# and stores the results in a CSV (Comma-Separated Values) file having the same
# name as the input video.
#
# author: Jakub Nawała (jakub.tadeusz.nawala@gmail.com)
# modified: 22 Nov 2021

# Define ANSI escapes codes for the colorful fonts
RED='\033[0;31m'
L_RED='\033[1;31m' # light red
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
L_GREEN='\033[1;32m' # light green
L_PURPLE='\033[1;35m'
NC='\033[0m' # No Color

# Define the variable storing the current script name
PROGNAME=$(basename "$0")

# Define the function for the error handling
function error_exit {
# ----------------------------------------------------------------
# Function for exit due to fatal program error
#   Accepts 1 argument:
#     string containing descriptive error message
# ----------------------------------------------------------------

	printf "\033[1;31m" # '\033[1;31m' sets the text color to light red
	printf "${PROGNAME}: ${1:-"Unknown Error"}\n" 1>&2 
	printf "\033[0m" # '\033[0m' resets the color back to normal
	exit 3
}

# Check if the bash version is compatible with this script (requires at least BASH ver.3)
if [ "${BASH_VERSINFO[0]}" -lt 3 ]; then
    printf "${RED}Your BASH version is too old (%s). Please use BASH ver. 3 or newer. Quitting.\n${NC}" "${BASH_VERSINFO[0]}"
    exit 1
fi

# Check for the input validity
if [[ -z "$1" || -z "$2" ]]; then
	printf "${L_RED}ERROR: Not enough parameters${NC}\n\n"
	printf "  ${YELLOW}Usage:\n"
	printf "\t$PROGNAME <path_to_video_clip> <path_to_vqi_binary> [<vqis_to_run>]\n\n${NC}"
	printf "NOTE: <path_to_video_clip> is a path to multimedia file that one wishes\n"
	printf "      \tto process using VQIs (Video Quality Indicators) calculating\n"
	printf "      \tbinary. Path to this binary is specified by \n"
	printf "      <path_to_vqi_binary> parameter.\n"
	printf "      <vqis_to_run> is an optional argument.\n"
	printf "      \tIt takes the form of a 16-bit positive integer. Each VQI belongs to a \n"
	printf "      \tgiven bit of the integer. For example, the Blockiness VQI corresponds \n"
	printf "      \tto the least significant bit of the 16-bit integer. The ordering of the\n"
	printf "      \trest of VQIs is as follows (values in parentheses identify decimal values\n"
	printf "      \tthat correspond to the one particular bit being set in the 16-bit positive\n"
	printf "      \tinteger): SA (2), Letterbox (4), Pillarbox (8), Blockloss (16), Blur (32),\n"
	printf "      \tTA (64), Blackout (128), Freezing (256), Exposure (512), Contrast (1024),\n"
	printf "      \tInterlace (2048), Noise (4096), Slice (8192) and Flickering (16384).\n"
	printf "      \tPlease note that you can provide a value for the <vqis_to_run> parameter\n"
	printf "      \tin the form of a hexadecimal number. For example, 0x7FFF means running all VQIs."
	printf "      \n\n"
	printf "      Output of the script will be stored in the folder created\n"
	printf "      according to the following syntax:\n\n"
	printf "      \tVQIs-results-<year>-<month>-<day>\n\n"
	printf "      Video or image file will have its respective *.csv file\n"
	printf "      with VQIs (Video Quality Indicators) results.\n\n"
	printf "SUPPORTED MULTIMEDIA FILES' EXTENSIONS: jpg, jpeg, png, ts, mpg, mp4,\n"
	printf "      mov, avi, mkv, gif, bmp.\n\n"
	printf "      Any new extensions may be added to this list by modification\n"
	printf "      of appropriate part of this script. Find the line that starts\n"
	printf "      with \"for EXT in\" and add new extensions to the list that\n"
	printf "      follows. Be aware that script will operate only with\n"
	printf "      extensions supported by the FFmpeg software.\n"
	printf "NOTE: This script works both with images and videos.\n\n"
	exit 1
fi

# Check whether all required apps are installed (for sure, check for FFmpeg)
command -v ffmpeg >/dev/null 2>&1 || error_exit \
  "$LINENO: FFmpeg is not in the PATH. I cannot continue without it. Aborting."
command -v ffprobe >/dev/null 2>&1 || error_exit \
  "$LINENO: ffprobe is not in the PATH. I cannot continue without it. Aborting."

# Read the input video's path and verify its correctness
VIDEOFILE="$1"
if [[ ! -e ${VIDEOFILE} ]]; then
 	error_exit "${LINENO}: Provided video file \"${VIDEOFILE}\" does not exist."
 fi 

# Read the binary file and verify its correctness
EXECUTABLE="$2"
if [[ ! -e ${EXECUTABLE} || ! -x ${EXECUTABLE} ]]; then
	error_exit "${LINENO}: Provided path for VQIs calculating binary: \
\"${EXECUTABLE}\" does not exist or is not executable."
fi

# Read the 16-bit integer specifying which VQIs to run (if provided)
VQIS_TO_RUN=0x7FFF
if [[ $# -eq 3 ]]; then  # three positional arguments present
  VQIS_TO_RUN=${3}
fi
printf "You asked to run the following VQIs: %s\n" "${VQIS_TO_RUN}"

# Prepare an array of supported multimedia files types
declare -A EXT_MAP
for EXT in jpg jpeg png ts mp4 mov avi mkv gif bmp; do 	# populate array with supported extensions (modify to add more)
	EXT_MAP["${EXT}"]=1	# set value '1' for key "${EXT}"
done

# Prepare an array of photo multimedia files types
declare -A PHOTO_EXT_MAP
for PHOTO_EXT in png PNG jpg JPG jpeg JPEG bmp BMP; do # populate array with photos' extensions
	PHOTO_EXT_MAP["${PHOTO_EXT}"]=1
done

# Extract the sole filename (w/o the path and extension)
FILENAME=$(basename "${VIDEOFILE}")
FILENAME=${FILENAME%.*}
# printf "${LINENO}: Variable FILENAME is now set to: ${FILENAME}\n"	# debug print

# Check if file given is a proper multimedia file
if [[ ! ${EXT_MAP["${VIDEOFILE##*.}"]} && ! ${PHOTO_EXT_MAP["${VIDEOFILE##*.}"]} ]]; then	# if file's extension is not supported, skip the file
	error_exit "${LINENO}: Provided file \"${VIDEOFILE}\" is not a supported multimedia file."
fi

# Make the directory for the output files
DIR="VQIs-results-$(date +%Y-%m-%d)"
# printf "${LINENO}: Variable DIR is now set to: ${DIR}\n"  # debug print
printf "${YELLOW}Creating the ${DIR} directory or using the exitent one...${NC}\n"
mkdir -p $DIR || error_exit "${LINENO}: Failed creating \"${DIR}\" directory."
printf "${YELLOW}All results will be stored in ${DIR} directory${NC}\n"

# Read the dimensions of the video frame and the FPS
eval $(ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries \
	stream=height,width "${VIDEOFILE}")
WIDTH=${streams_stream_0_width}
HEIGHT=${streams_stream_0_height}

# If file is the photo, ommit the FPS calculus
if [[ ${PHOTO_EXT_MAP["${VIDEOFILE##*.}"]} ]]; then	# ${VIDEOFILE##*.} returns VIDEOFILE's extension
	FPS=1
else
	eval $(ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries \
		stream=avg_frame_rate "${VIDEOFILE}")
	FPS=${streams_stream_0_avg_frame_rate}
	FPS=$(echo "scale=2; $FPS" | bc) # reduce the FPS to 2 digits after dot precision
	# Make sure that there is only one FPS read
	set -- $FPS
	FPS=$1
fi
printf "${YELLOW}Parameters of the video stream:\n"
printf "\tName:\t${FILENAME}\n"
printf "\tWidth:\t$WIDTH\n"
printf "\tHeight:\t$HEIGHT\n"
printf "\tFPS:\t$FPS\n\n${NC}"

# Convert file to the yuv format and save the ffmpeg output to the log file
printf "${YELLOW}Uncompressing using the ffmpeg...${NC}\n"
YUV="$FILENAME.yuv"
LOGFILE="ffmpeglog-${FILENAME}-$(date +%Y-%m-%d-%H-%M-%S).txt"
ffmpeg -nostdin -v info -i "${VIDEOFILE}" -pix_fmt yuv420p "${YUV}" > "${LOGFILE}" 2>&1 \
	|| error_exit "${LINENO}: Failed during uncompression of \"${VIDEOFILE}\" file."
printf "Output of the ffmpeg stored in the ${LOGFILE}\n\n"

# Calculate the metrics on the file and save the output in the results.txt
RESULTS="results-${FILENAME}.csv"
printf "${YELLOW}Calculating VQIs on uncompressed video...${NC}\n"
"${EXECUTABLE}" "${YUV}" ${WIDTH} ${HEIGHT} "${VQIS_TO_RUN}" ${FPS} > /dev/null
mv metricsResultsCSV.csv "${RESULTS}"
printf "${L_GREEN}Results saved in the ${L_PURPLE}${RESULTS} \
${L_GREEN}file\n\n${NC}"

# Move the results and logfiles to one common folder
mv "${RESULTS}" "${DIR}"
mv "${LOGFILE}" "${DIR}"
# Remove the uncompressed file
printf "${YELLOW}All computations done.${NC}\n"
printf "${YELLOW}Removing the ${YUV} file...${NC}\n\n"
rm $YUV

printf "Exiting the script...\n"
exit 0
