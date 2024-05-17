#!/bin/bash

# -e: exit on error
# -u: exit on unset variables
set -eu

NODE_VERSION=lts-bookworm

preview() {
    docker run --rm -v $(pwd):/workspace -w /workspace -itp 8080:8080 node:$NODE_VERSION yarn quartz build --serve
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
        node:$NODE_VERSION \
        yarn quartz $@
}

show_menu() {
    echo -e "\u001b[32;1m QUARTZ CTL MENU \u001b[0m"
    echo -e " \u001b[37;1m\u001b[4m Options:\u001b[0m"
    echo -e "  \u001b[34;1m (0) perview | p => perview blog before publich \u001b[0m"
    echo -e "  \u001b[34;1m (1) sync => sync blog to remote repository, or update quartz \u001b[0m"
    echo -e "  \u001b[34;1m (2) sync --no-pull | sop => sync blog to remote repository but not update quartz \u001b[0m"
    echo -e "  \u001b[34;1m (3) quartz | q => run any quartz support sub commands \u001b[0m"
}

main() {
    case "$1" in
    -m | --menu | m | menu | show_menu) show_menu ;;
    p) preview;;
    sop) sync --no-pull;;
    *) "$@";;
    esac
    exit 0
}

main "$@"
