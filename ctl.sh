#!/bin/sh

# -e: exit on error
# -u: exit on unset variables
set -eu

preview() {
    docker run --rm -v ${pwd}:\workspace -w \workspace -itp 8080:8080 yarn node:lts-slim quartz build --serve
}

# For full help options, you can run npx quartz sync --help.
# 
# Most of these have sensible defaults but you can override them if you have a custom setup:
# 
# -d or --directory: the content folder. This is normally just content
# -v or --verbose: print out extra logging information
# --commit or --no-commit: whether to make a git commit for your changes
# --push or --no-push: whether to push updates to your GitHub fork of Quartz
# --pull or --no-pull: whether to try and pull in any updates from your GitHub fork (i.e. from other devices) before pushing
sync() {
    quartz sync $@
}

quartz() {
    docker run \
        --rm \
        -u 1000:1000 \
        -v $(pwd):/home/node/quartz -v ~/.ssh:/home/node/.ssh \
        -w /home/node/quartz \
        node:lts-bookworm \
        /bin/bash -c "su node; yarn quartz $@"
}

show_menu() {
    echo -e "\u001b[32;1m Setting up your env with dots2k...\u001b[0m"
    echo -e " \u001b[37;1m\u001b[4mSelect an option:\u001b[0m"
    echo -e "  \u001b[34;1m (0) Setup Everything \u001b[0m"
    echo -e "  \u001b[34;1m (1) Install Packages \u001b[0m"
    echo -e "  \u001b[34;1m (2) Install Languages \u001b[0m"
    echo -e "  \u001b[34;1m (3) Install Extras \u001b[0m"
    echo -e "  \u001b[34;1m (4) Backup Configs \u001b[0m"
    echo -e "  \u001b[34;1m (5) Setup Symlinks \u001b[0m"
    echo -e "  \u001b[31;1m (*) Anything else to exit \u001b[0m"
    echo -en "\u001b[32;1m ==> \u001b[0m"
}

main() {
    case "$1" in
    -m | --menu | m | menu | show_menu) show_menu ;;
    *) "$@";;
    esac
    exit 0
}

main "$@"
