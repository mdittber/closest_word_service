#!/bin/sh

curl	--header "Content-Type: application/json" \
			--request POST \
			--data '{"word":"orange","N":15}' \
			http://localhost:5050/ClosestWord
