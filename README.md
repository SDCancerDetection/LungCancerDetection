
# Lung Cancer Diagnostic System
This repository hosts a four person Michigan Technological University undergraduate senior design team developing an application prototype for a user friendly lung cancer detection software with machine learning capability for CT scans. The User Interface provides a level of abstraction so that the user does not need to know the inter-working of the machine learning algorithm, but can still benefit from it's analysis. 

### Application Structure

The application structure was chosen to have a HTML/CSS/JS front end to allow for an appealing and flexible UI and Python 3.6 backend for the data processing and machine learning algorithms. Tensor Flow was the machine learning library used to create the CNN algorithm. ElectronJS was the chosen framework to package the app to use as a local application.
**![](https://lh3.googleusercontent.com/hkAYdXg_TmwadS44Ll0yUP6Ss1LzXF5bTmv_TEsGefN1QdDGxZNPSzQ_hOrxsNES89ynRT9PW-Kl9wQW1DRZoQ1Nr6NHP72Be_zNv6JW6ge5P58K9Vfku7NZq5sg0vCUY4KcJYtg)**

### Project Summary
This project was split into four parts for our four members: 

- Machine Learning: Creating, training, and predicting for the CT scans of patients
- Data Processing: Preparing scans during the training and predicting (normalizing and augmentation)
-  Front End Design: Included interviews with doctors for interface analysis to know what is important
- Backend Communication: Set up data communication lines from front end to python and back

These parts were combined in the end of the project to create a working application.

### Current State
The current application allows users to upload a scan in RAW/MHD by selecting a file path. The path is passed to the python script to do some preprocessing (1 pixel = 1 mm x 1 mm spacing and Hounsfield Unit normalization) and then the trained CNN predicts on patches that are 64 x 64 pixels. A CSV is created to contain all patches that are likely to be cancerous and saved in a temporary folder. Images (.jpg) of all slices in each axes are also save to this folder. All of this data is used to display the results to the user on the front end. A heat map is created using the CSV and the user can view a nodule from all perspectives using the 3 axes of the scan. Image manipulation tools are also included to allow the user to magnify an area, measure a nodule, and change the contrast of the scan (measurement and contrast are not yet functioning). Below is a screen shot of the front end from the current working application.

**![](https://lh6.googleusercontent.com/lwDsSnw8yiJsUof_hJAIsDczmrKpL4NfYKgTn17HqfigT_8D2B_r0elyi5tcBNV_W5umi4911wn58aht0gw85SAPP_uZqkPNCA0iiaZyXEmUCJoOxd9Suk-Ys2Hl_eTYqrqOeWALhoY)**

### Future Improvement Suggestions
Although we met the project requirements in the project definition for the application prototype, there are many parts of this project that can be improved upon to make it a better and more useful application. Below is a list of improvements that could be made in the future:
-   Train, predict, and view scans in 3D space
--  Might allow for better predictions and representation of nodules
-   Employ lung segmentation
--   Only allow nodules to be found within the lungs
-   Improve machine learning algorithm
-   Optimize training patch size and CNN - currently using 64 pixel patches, but this might not be best
-   Distribution software & a program installer/updater to allow for future improvements to reach all users
-- Allow users in the field to help train ML algorithm when analyzing results
-   Load and compare multiple scans
-- Clinicians need to be able to compare scans from the same patient taken over time to see growth of nodules
-   Allow clinicians to record medical notes for patient scans and save them for viewing next time that scan is opened

## Start Developing

You'll need to download the following:

<a href="https://git-scm.com/downloads">GitHub Command Line</a>
<a href="https://nodejs.org/en/">Node.js</a>
<a href="https://yarnpkg.com/en/docs/install#windows-stable">Yarn</a>

Clone the project

Run Git CMD, in the window find a good location (using cd & dir) for the repository (eg C:/User/Name/Documents)
Run the following command inside the quotes "git clone https://github.com/SDCancerDetection/LungCancerDetection/"
This will create a new folder called LungCancerDetection

Download Packages

Using Git CMD type "npm install", this will install the dependencies to run the project.

Create a new branch.

Enter the folder with Git CMD, and type "git checkout -b Initials-Develop" (eg "git checkout -b JL-Develop")

Edit the code

Using any IDE you want edit the code you want to change

Run Program

Using Git CMD type "yarn build" in the correct directory (LungCancerDetection)
This will create a folder called dist, using windows File Explorer go into that folder and run the SDCancerDetectionXXXXXX.exe file.
You should now be running the program.

Push New Code

Using Git CMD type "git push origin Initals-Develop" (eg "git push origin JL-Develop")
You may be prompted for user and password
This will push your branch to the online repository

Merge Code

Go to the online reposity --> select branches --> select your (should be a pull request) --> click merge pull request
