git init
touch readme.md
touch gitignore
git add -A
git status
git commit -am "First commit of this project, still empty."
git remote add origin https://github.com/Freq95/ProiectLicenta.git
git push origin master
git pull origin master => update local repo with github changes
git push -f origin database_new_structure => push a local branch on GitHub
========================================================
git add -A stages All
git add . stages new and modified, without deleted
git add -u stages modified and deleted, without new

========================================================
git branch => list all branches

--new branch--
========================================================
git branch branch_name
git checkout branch_name

- changes to the current ver of project =>

git add --all   => this will add all the files to the new branch
git commit -am "text"  => commit the changes to the branch

git checkout master
