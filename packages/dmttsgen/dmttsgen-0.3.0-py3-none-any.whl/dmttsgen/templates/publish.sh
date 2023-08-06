set -e
npm install --unsafe-perm
npm run build


if [ -z "$PUBLISH_LIB" ]
then
    echo "PUBLISH_LIB environment not set"
    exit 1
fi

if $PUBLISH_LIB; then
    npm publish --tag=beta
    echo "Library published"
else
    echo "Library not published"
fi
