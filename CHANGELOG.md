# CHANGELOG

## v12 dated 23 aug
* Index (right)
    - Reformatted order by upon search results to account for numeric dosage within entry name
* Index (left)
    - Added 'Delete All' button to empty cart in one click
* static/js
    - Added AJAX script in cart.js to connect emptyall button click to app route
* App.py
    - Added emptyall app route

## v11 dated 20 aug
* Print-out
    - Added SHP tagline to bottom

## v10 dated 19 aug
* Index (right)
    - Added a 'Successful delete' popup on delete click
* static/css
    - Changed 'Added to PERMELIS' popup size to account for all phone sizes
* static/js
    - Added AJAX script in cart.js to connect empty button click to app route
* App.py
    - Changed empty app route to return jsonify instead of ('', 204) to account for iOS vulnerabilities that lead to a blank page being shown on 204 request

## v9 dated 13 aug
* Authentication
    - Changed image in login page to PERMELIS x SHP
* Index (left)
    - Changed color of modal Close button to darker shade for ease of use
    - Change modal heading from Drug Info to Medication Info
* Print-out
    - Swapped locations of PERMELIS and SHP logo
    - Changed icons used to indicate morning, afternoon and evening
* Admin
    - Changed Cost in add Modal and Edit page to text from number
    - Removed Cost paragraph block in add Modal and Edit page
    - Sorted admin datatable based on entry name in ascending order
* App.py
    - Added custom footer for printout via '--footer-html' in print function
    - To account for header vulnerabilities when using '--footer-html', created '--header-html' as well
    - Fixed bug in deleting of images on edit
* static/images files
    - Deleted unnecessary files
* mysql.dump
    - Updated format of Cost column in DrugInfo table

## v8 dated 12 aug
* Print-out
    - Extended name field
* Admin
    - Prevented typing in Cost field of modal and Edit page
* static/images
    - Included new images for new medications
* static/js files
    - Fixed bug in script for modals
* mysql.dump
    - Included new medications and updated image names for some

## v7 dated 06 aug
* README.md
    - Included relevant changes required if run in Windows
* Index page (left panel)
    - Edited search button in mobile view due to vulnerabilities of form-inline in width <578px
    - Edited 'Added to PERMELIS!' alert size to be independent of width and height of screen
    - Turned autocomplete off for search
    - Reformatted search result layout for mobile landscape view
    - Added css for modal in mobile landscape view
    - Fixed height of split screen columns
* Print-out
    - Added script in app.py for using wkhtmltopdf in Windows
* Login
    - Turned autocomplete off for admin login
* Admin
    - Added banner under modals to represent start of admin table
    - Added functionality for removal of admin users as well
    - Added preview for uploaded image on addition of new medication
    - Enabled modal form reset on modal close across all admin modals
    - Reformated datatable to now include display length dropdown and buttons on a new row
    - Resized webpage content to cover more width
    - Turned autocomplete off for all modals

## v6 dated 05 aug
* Index page (left panel)
    - Changed Search bar button to icon button at right end of search field 
    - Added minimum length limit of 2 to Search field
    - Changed 'Added to cart!' alert to 'Added to PERMELIS!'
* Print-out
    - Replaced “Img” with “Picture”, and “”Entry” with “Name”.
* Admin
    - Enabled preview of uploaded image during image edit to compare side-by-side against original input, along with the option to cancel or confirm the uploaded image.
    - Added second user with username 'shp2' and password 'password2' for access.
* App.py
    - Renamed 'printer' for print url as 'printing'.
    - Added bcrypt for password hashing in authentication, admin login, editing of authentication details and adding new admin user.
* static/js files
    - Removed an 'a href' based script that was preventing print
* requirements.txt
    - Added bcrypt 
* mysql.dump
    - Changed table information to account for bcrypt password hashing

## v5 dated 04 aug
* All pages
    - Set standard html zoom to 75% for optimal viewing across all platforms (Firefox, Edge, Chrome, Safari).
* Authentication page
    - Changed authentication field from text to password.
* Index page (left panel)
    - Rectified location of modal dialog to prevent body of screen from scrolling upwards and prevent modal from sticking to bottom of screen.
    - Isolated vertical layout of modal in mobile to prevent changes to layout of cart in right panel of Index page.
    - Edited Search result to remain there until new search is entered.
    - Added additional instructions when Search is presented on accessing medication information.
    - Added 'Added to cart!' alert in mobile view since cart is at bottom of screen.
    - Added 'Added to cart!' alert in desktop view as well
* Index page (right panel)
    - Replaced “Img” with “Picture”, and “”Entry” with “Name”.
    - Fixed bug in Delete loop during duplicate additions
    - Edited Cart result so that when cart is empty, earlier instructions are present again.
* Print-out
    - Fixed spacing in title
    - Changed footer to appear in every printed page
    - Added page numbers (e.g. Page 1 of 2) to top right hand corner of every page
* Admin
    - Added comment on optimal image size for upload
* App.py
    - Removed print functions for debugging
    - Turned off app debug

## v4 dated 03 aug
* Index page
    - Removed admin button when in mobile viewport
* Index page (left panel)
    - Improved mobile responsiveness of medication info modal 
        * Information is displayed in vertical format but horizontal in desktop.
        * Removed vertical scroll within modal dialog
    - Added comment in case of no search results
    - Optimised cards to display images of all sizes
* Admin 
    - Optimised to display images of all sizes
* Print-out
    - Changed title from "Personalized Medication List" to "My Personalized Medication List".

## v3 dated 03 aug
* Index page
    - Changed title (of HTML page) to same as the index page "PERMELIS - Personalized Medication List Made Easy" (from "PERMELIS - Index")
    - Moved "Admin" button to top-right (from top-left)
* Index page (left panel)
    - Removed the "Search result for" label
    - To make it more mobile friendly:
        * For search results, made it one card per row when viewport is small/mobile
        * For the top of the page, changed it such that when viewport is small/mobile, the Permelis logo is on the left and Admin button on the right on the same line, with Permelis logo enlarged.
* Index page (right panel)
    - Removed "Clear List" button and replaced it with individual delete buttons next to each medication. 
* Print-out
    - Edited Permelis logo so it would be in-line with SHP logo.
    - Change title from "Personalised Medication List" to "Personalized Medication List".
* Admin
    - Created an export function to export the medication database (exclude images) as both csv and xlsx files. File name "PERMELIS Database - YYYYMMDD HH_MM_SS"

## v2 dated 02 aug
* Authentication page
    - Amended the page title (in HTML) to "PERMELIS - Personalized Medication List Made Easy"
* Index page
    - For the h1 text - changed to "Personalized Medication List Made Easy" instead of "Personalised Medication List", made bold.
    - Below the h1 text, added "1. Search 2. Add 3. Print". Numbers are in colored circles, with blue, green and red corresponding to 1,2 and 3.
    - Created a blue search button in replacement of live data search, with color matching the circle above.
    - Changed the print button to red color, matching the circle above.
    - Edited search result formatting to prevent need to scroll left and right within panel. 
    - For mobile responsiveness, changed layout to right panel going below left panel when the view port is mobile size
* Index page (left panel)
    - Changed "Enter Medication Name" to "Search Medication"
    - In search box, changed "Search all fields e.g. Glimperide" to "Enter medication name e.g. metformin"
    - Enabled pop-up window with medication info when clicking medication images.
* Index page (right panel)
    - Changed "Empty Cart" to "Clear List"
    - Changed "Your personal medication list." to "Your PERMELIS"
    - Change "Img" to "Image"
    - Change "Entry" to "Name"
* Print out
    - Moved permelis logo to the top-right. Kept SHP logo top-left.
    - Added a footer "Made with the PERMELIS app (permelis.com) (C) 2021"
    - Changed file name of print-out to "PERMELIS - (append with timestamp YYYYMMDD HH_MM_SS)"

## v1 dated 30 jul