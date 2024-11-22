curl --location 'http://localhost:15959/' \
--header 'Content-Type: application/json' \
--data '{
    "text": "def foo(i, j): return i +i"
}
'
