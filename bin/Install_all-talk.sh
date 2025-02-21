#!/usr/bin/bash
# Install_all-talk.sh
#

export APP_HOME="/home/$(whoami)/all-talk"
export APP_PYTHON="/home/$(whoami)/.local/bin/python3.11"
export DEBUG="True"

# Debugging support
if [ "${DEBUG}" = "True" ]
then
	# enable shell debug mode
	set -x
fi

cd ${APP_HOME}

if [ -d "${APP_HOME}/dist" ]
then
	rm -rf "${APP_HOME}/dist"
fi

${APP_PYTHON} -m pip uninstall -y all-talk

${APP_PYTHON} -m build .
ls -l dist/*.whl
${APP_PYTHON} -m pip install dist/*.whl

${APP_PYTHON} -m all_talk.all_listen &
${APP_PYTHON} -m all_talk.all_talk
