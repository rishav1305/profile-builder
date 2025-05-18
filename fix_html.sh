#!/bin/bash

# Fix the JavaScript in the index.html file
sed -i '' 's/                    alert(.An error occurred while extracting portfolio data..);//g' /Users/rishavchatterjee/Desktop/Projects/profile-builder/templates/index.html
sed -i '' 's/                })//g' /Users/rishavchatterjee/Desktop/Projects/profile-builder/templates/index.html
sed -i '' 's/                .finally(() => {//g' /Users/rishavchatterjee/Desktop/Projects/profile-builder/templates/index.html
sed -i '' 's/                    extractBtn.disabled = false;//g' /Users/rishavchatterjee/Desktop/Projects/profile-builder/templates/index.html
sed -i '' 's/                    extractBtn.textContent = .Extract Data.;//g' /Users/rishavchatterjee/Desktop/Projects/profile-builder/templates/index.html
sed -i '' 's/                });//g' /Users/rishavchatterjee/Desktop/Projects/profile-builder/templates/index.html

echo "HTML file has been fixed to remove duplicate code"
