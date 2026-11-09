# CVS Evening Loss-Prevention Navigator

## Vision
The Regional Loss Prevention Manager at CVS Health in Los Angeles must decide each quarter which five LAPD reporting districts need an extra evening security guard (18:00–24:00). This app provides a data-backed shortlist to justify the budget allocation.

## Live App Link
**You can access the live app here:** 
https://cvs-loss-prevention-app-team1.streamlit.app/

## Demo Video
**Watch our demo walkthrough here:**
https://youtu.be/Kml-suydCWU

## Data Used
This app uses the **LAPD NIBRS Offenses** dataset. To ensure fast loading and avoid exceeding GitHub/Streamlit memory limits, we use a pre-processed, column-filtered version of the data stored in `data/processed/`. The app reads this processed file directly. We excluded the Victims table since the tool focuses on offense counts.

## How to Run Locally
If you want to run this app on your own machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/christiancabello-usc/dso576-project-M1.git
   cd dso576-project-M1
