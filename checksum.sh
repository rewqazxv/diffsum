SUM='sha1sum'
LOC=${1:-.}

exec find $LOC -type f ! -name "*.$SUM" -print0 | xargs -0 $SUM > `date +%Y%m%d%H%M%S`.$SUM
