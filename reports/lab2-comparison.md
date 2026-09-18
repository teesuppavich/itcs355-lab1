# Lab 2 — Remote Hyperparameter Comparison

**Trials:** 12  
**Total estimated tuning cost:** 1.0558 THB  
**Instance:** e2-standard-4  
**Spot:** Yes

## Trial results

| trial | run_id | job_id | n_estimators | max_depth | min_samples_leaf | seed | instance | spot | duration_s | cost_thb | val_roc_auc | val_pr_auc | test_roc_auc | test_pr_auc | data_fingerprint | image_digest |
|---:|:---|:---|---:|---:|---:|---:|:---|:---|---:|---:|---:|---:|---:|---:|:---|:---|
| 1 | b8787b9ce32b4252ba057f850dd77a07 | projects/581504912225/locations/asia-southeast1/customJobs/6771063908338761728 | 100 | 4 | 5 | 20260101 | e2-standard-4 | True | 254.8530 | 0.1359 | 0.8426 | 0.3932 | 0.8533 | 0.4965 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 0 | bd33de7d808a441a90e4eadbbeceada5 | projects/581504912225/locations/asia-southeast1/customJobs/763473111659053056 | 100 | 4 | 1 | 20260101 | e2-standard-4 | True | 30.0000 | 0.0160 | 0.8424 | 0.3938 | 0.8518 | 0.4942 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 7 | 5ef9270dd5ea49588f3321949346bba3 | projects/581504912225/locations/asia-southeast1/customJobs/3805443553715290112 | 300 | 4 | 5 | 20260101 | e2-standard-4 | True | 181.6090 | 0.0969 | 0.8411 | 0.3887 | 0.8545 | 0.5038 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 6 | f7a28578aac24d2bac8b47de9230c657 | projects/581504912225/locations/asia-southeast1/customJobs/2976992328511651840 | 300 | 4 | 1 | 20260101 | e2-standard-4 | True | 201.7570 | 0.1076 | 0.8404 | 0.3901 | 0.8537 | 0.5062 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 3 | ea35baeefd01481d91cf8d93501bc0f1 | projects/581504912225/locations/asia-southeast1/customJobs/4636568791197679616 | 100 | 8 | 5 | 20260101 | e2-standard-4 | True | 186.3340 | 0.0994 | 0.8397 | 0.4063 | 0.8466 | 0.4675 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 9 | 58836fcf61d54c45a0b77bb12a135be0 | projects/581504912225/locations/asia-southeast1/customJobs/7358994765943144448 | 300 | 8 | 5 | 20260101 | e2-standard-4 | True | 42.5400 | 0.0227 | 0.8377 | 0.3954 | 0.8491 | 0.4780 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 11 | 1b8f6b88ab44480198dbd36d168ddcfe | projects/581504912225/locations/asia-southeast1/customJobs/382918943146246144 | 300 | 12 | 5 | 20260101 | e2-standard-4 | True | 162.1270 | 0.0865 | 0.8354 | 0.3791 | 0.8431 | 0.4707 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 8 | c4c57f3c0aae4ecea9a2851fe3eb788e | projects/581504912225/locations/asia-southeast1/customJobs/7511906047041208320 | 300 | 8 | 1 | 20260101 | e2-standard-4 | True | 178.1940 | 0.0950 | 0.8338 | 0.3876 | 0.8478 | 0.4699 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 5 | 968c34a6a29246819e60f9fe5906f33a | projects/581504912225/locations/asia-southeast1/customJobs/1499600544501596160 | 100 | 12 | 5 | 20260101 | e2-standard-4 | True | 161.5830 | 0.0862 | 0.8322 | 0.3794 | 0.8417 | 0.4711 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 2 | 081efb5da4074c1b8151092598585e47 | projects/581504912225/locations/asia-southeast1/customJobs/234300155443019776 | 100 | 8 | 1 | 20260101 | e2-standard-4 | True | 233.6640 | 0.1246 | 0.8312 | 0.3830 | 0.8488 | 0.4705 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 4 | daa9d923a6ed45a8987f8ed7ff4e0435 | projects/581504912225/locations/asia-southeast1/customJobs/8579259158728015872 | 100 | 12 | 1 | 20260101 | e2-standard-4 | True | 169.9370 | 0.0906 | 0.8268 | 0.3898 | 0.8415 | 0.4572 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |
| 10 | bad682f44f5c4b2cbb272808d6df10e6 | projects/581504912225/locations/asia-southeast1/customJobs/5125209350767378432 | 300 | 12 | 1 | 20260101 | e2-standard-4 | True | 176.9940 | 0.0944 | 0.8265 | 0.3857 | 0.8374 | 0.4560 | 422cccb9136e8140 | sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47 |

## Selected configuration

Selected configuration: Trial 1 (`n_estimators=100`, `max_depth=4`, `min_samples_leaf=5`).

- Validation ROC-AUC: 0.8426
- Test ROC-AUC: 0.8533
- Training cost: 0.1359 THB

## Selection justification

The selected configuration had the highest validation ROC-AUC at 0.8426, but the margin over Trial 0 was only 0.00016, so the difference is very small and may be within normal variation. The selected model cost 0.1359 THB per training run, and monthly retraining at the same estimated Spot rate and duration would cost approximately 0.1359 THB. All trials used the same seed (20260101), so seed variance was not measured in this study. The choice could be wrong if the validation split does not represent future production data or if another seed produces a different ranking. A future evaluation using multiple seeds and newer data could therefore select a different configuration.

## Registered Model Lineage

The tuning selection came from Trial 1. The selected configuration was then rerun remotely with an artifact-producing image before registration. The following lineage belongs to the registered model:

- Data fingerprint: `422cccb9136e8140`
- Image digest: `sha256:0b54b73ddb9f6bd5206e85dd5a4696cad1c1874808ddc59860249b32b34a8296`
- MLflow run ID: `4f6a4bd74e64430893d63d035691dce9`
- Training job ID: `projects/581504912225/locations/asia-southeast1/customJobs/6825318210099740672`
- Seed: `20260101`
- Validation ROC-AUC: `0.84259989736441`
- Test ROC-AUC: `0.8532857870606215`
- Vertex AI Model ID: `97210022034931712`
- Vertex AI Model Version: `1`
- Vertex AI Alias: `staging`
