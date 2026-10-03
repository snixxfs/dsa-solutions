#!/bin/bash
# Usage: ./new.sh <codechef|leetcode> <ProblemName> [ext]
# Example: ./new.sh codechef START1 py
set -e
site=$1; name=$2; ext=${3:-py}
if [ -z "$site" ] || [ -z "$name" ]; then
  echo "Usage: ./new.sh <codechef|leetcode> <ProblemName> [ext]"; exit 1
fi
file="$site/$name.$ext"

case $ext in
  py) c="#" ;;
  *)  c="//" ;;
esac

if [ ! -f "$file" ]; then
  cat > "$file" << TEMPLATE
$c Problem: $name
$c Site: $site
$c Link:
$c Topic:
$c Difficulty:
$c Approach:
$c Complexity: O(?) time, O(?) space

TEMPLATE
fi

${EDITOR:-code} "$file"
read -p "Finished? Press Enter to commit and push (Ctrl+C to cancel)... "

python update_readme.py
git add "$file" README.md
git commit -m "solve $site/$name"
if [ -n "$(git remote)" ]; then git push; fi
