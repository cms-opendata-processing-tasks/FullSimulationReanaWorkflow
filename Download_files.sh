read -p "Enter workflow name: " workflow

for file in $(reana-client ls -w "$workflow" | \
              grep -v NAME | \
              awk '{print $1}' | \
              grep '^results/nano_.*\.root$')
do
    reana-client download -w "$workflow" "$file"
done