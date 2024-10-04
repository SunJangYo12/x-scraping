file="kusolink/link.txt"

line_number=0
line_total=$(wc -l < "$file")

while IFS= read -r line; do

    filename=$(echo "$line" | tr '/:' '_' | sed 's/[^a-zA-Z0-9._-]//g')

    echo
    echo
    echo "[+] [$line_number/$line_total] $filename"
    echo
    echo

    curl -s "$line" > "original/$filename"

    ((line_number++))
done < $file
