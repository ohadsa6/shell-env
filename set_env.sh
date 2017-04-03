
function print_env_variants()
{
cat << EOF

Available environment variants:

1. LG-G5 H850
1. LG-V20 US996

EOF
}

function set_env()
{
	if [ $# -gt 1 ]; then
		echo "Usage: set_env [ENV_VARIANT]"
		return
	elif [ $# -eq 1 ]; then
		ENV_VARIANT=$1
	else
		print_env_variants
		read ENV_VARIANT
	fi

	case ${ENV_VARIANT} in
		1)
			PROJECT="g5"
			;;
		2)
			PROJECT="lg-v20-us996"
			;;
		*)
			echo "Please choose valid environment variant, see below"
			print_env_variants
			return
			;;
	esac

	source ${SHENV_DEV_ENV}/project/${PROJECT}/set_project_env.sh
	cd ${SHENV_PROJECT_ROOT}
}
