#!/bin/sh

DIRNAME=libdrm
PACKAGENAME=${DIRNAME}-2.4.21

echo REF ${REF:+--reference $REF}
echo DIRNAME $DIRNAME
echo HEAD ${1:-HEAD}

if [ -d $DIRNAME ]
then
    pushd $DIRNAME
    git pull
    popd
else
    git clone ${REF:+--reference $REF} \
	git://proxy01.pd.intel.com:9419/git/mesa/drm $DIRNAME
fi

pushd $DIRNAME
tmp=$(git-show -s | grep '^commit' | cut -d " " -f 2)
commitid=$(echo ${tmp:0:10})
popd

GIT_DIR=$DIRNAME/.git git archive --format=tar --prefix=$PACKAGENAME~git$commitid/ ${1:-HEAD} \
	| bzip2 > $PACKAGENAME~git$commitid.tar.bz2

# rm -rf $DIRNAME
