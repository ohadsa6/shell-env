
function print_build_variants()
{
cat << EOF

Available build variants:

1. make clean
2. make config
3. build kernel
4. create image
5. flash

EOF
}



function mk()
{
	if [ $# -gt 1 ]; then
		echo "Usage: mk [BUILD_VARIANT]"
		return
	elif [ $# -eq 1 ]; then
		BUILD_VARIANT=$1
	else
		print_build_variants
		read BUILD_VARIANT
	fi

	CUR_DIR=$PWD
	cd ${SHENV_PROJECT_ROOT}
	case ${BUILD_VARIANT} in
		1)
			echo "perform: make clean"
			make distclean=y
			;;
		2)
			echo "perform: make config"
			make config=y
			;;
		3)
			echo "perform: build kernel"
			make
			;;
		4)
			echo "perform: create image"
			make img
			;;
		5)
			echo "perform: flash"
			sudo make flash
			;;
		*)
			echo "Please choose valid environment variant, see below"
			print_env_variants
			return
			;;
	esac

	cd ${CUR_DIR}
}

echo "Loading environment for LG-V20 US996"
export SHENV_PROJECT_ROOT=${SHENV_DEV_ROOT}/lg-v20-us996
alias r='cd ${SHENV_PROJECT_ROOT}'
alias k='cd ${SHENV_PROJECT_ROOT}/android/kernel'
set-title "LG-V20"
