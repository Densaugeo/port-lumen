install: downloads
	id agents || sudo useradd agents
	sudo usermod --append --groups agents $$USER
	echo '%agents ALL = (agents) NOPASSWD:/usr/bin/apptainer' | \
		sudo EDITOR='cp /dev/stdin' visudo -f /etc/sudoers.d/agents

downloads:
	mkdir $@ --mode 2775
	chgrp agents $@

apptainer: apptainers/port-lumen.sif
	sudo -u agents apptainer shell --containall \
		--bind $$(pwd):$$(pwd):rw \
		--cwd $$(pwd) apptainers/port-lumen.sif

# Apptainers are built using their restricted user. This recipe creates a
# temporary directory with the permissions to allow this
apptainers/%.sif: TMP = apptainers/$*-tmp
apptainers/%.sif: apptainers/%.Definitionfile
	mkdir -p $(TMP)
	sudo chgrp agents $(TMP)
	sudo chmod 2775 $(TMP)
	sudo -u agents apptainer build $(TMP)/image.sif $<
	sudo mv $(TMP)/image.sif $@
	sudo chown $$USER:$$USER $@
	sudo rm -rf $(TMP)

apptainers/python3.14.sif: apptainers/fedora.sif
apptainers/port-lumen.sif: apptainers/python3.14.sif
