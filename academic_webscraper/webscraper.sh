#!/bin/bash

echo "Fetching paper announcements from journal sites..."
echo "-----------------------------------------------------"
python3 1_scraper_A.py
echo "Journal 1 of 6 completed"
python3 2_scraper_B.py
echo "Journal 2 of 6 completed"
python3 3_scraper_C.py
echo "Journal 3 of 6 completed"
python3 4_scraper_D.py
echo "Journal 4 of 6 completed"
python3 5_scraper_E.py
echo "Journal 5 of 6 completed"
python3 6_scraper_F.py
echo "Journal 6 of 6 completed"
echo "-----------------------------------------------------"
echo "All done!"