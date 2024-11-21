curl --location 'http://localhost:15959/' \
--header 'Content-Type: application/json' \
--data '{
    "document_type": "FUNCTION",
    "text": "def foo(i, j): return i +i"
}
'
