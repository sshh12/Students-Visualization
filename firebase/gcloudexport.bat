@echo off
:: Set Project
gcloud config set project cfisd-api
:: Export Firestore -> Buckets
gcloud beta firestore export gs://cfisd-data --collection-ids=users,grades,profile,transcript
:: Import Bucket as tables (for each datakind) into CFISD_DATA BigQuery Dataset
:: <cmd here>
:: Export table to Bucket /exports/tablename
:: <cmd here>
:: Download as JSON from Google Console
:: <cmd here>