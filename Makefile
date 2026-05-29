install:
	id agents || sudo useradd agents
	sudo usermod --append --groups agents $$USER
	echo '%agents ALL = (agents) NOPASSWD:/usr/bin/apptainer' | \
		sudo EDITOR='cp /dev/stdin' visudo -f /etc/sudoers.d/agents

test-apptainer: apptainers/test.sif
	@printf '\n$(ORANGE)Session history is broken again but session can be '
	@printf 'resumed with $(BOLD)$(AQUA)opencode -s '
	@printf 'ses_???$(RESET)\n\n'
	
	@# Changing cwd breaks Opencode session history, so I'm waiting to move
	@# it
	sudo -u agents apptainer shell --containall \
		--bind .:/repo:rw \
		--bind "/projects/Port Lumen download for testing 2:/projects/Port Lumen download for testing 2:ro" \
		--bind "/projects/Port Lumen download for testing:/projects/Port Lumen download for testing:ro" \
		--cwd /repo apptainers/test.sif

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

apptainers/opencode.sif: apptainers/fedora.sif
apptainers/python3.14.sif: apptainers/opencode.sif
apptainers/test.sif: apptainers/python3.14.sif
