# fake-shop-etl

To get the CD workflow working I had to run:

```bash
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=serviceAccount:gcf-cd-service-account@<PROJECT_ID>.iam.gserviceaccount.com --role=roles/iam.serviceAccountUser
```

this was to to allow my CD service account the ability to be a service account caller/ a user of other service accounts in my project.

# how to set this up:

- create a storage bucket

- create 3 service accounts, one for Continous Integration, Continuous Deployment, local development. The CI service account should be able to access GCS and Biguqery. The CD service account should have the Cloud functions developer role and should have permission to use other service accounts. the development seervice account should have same priviledges as the CI service account.

- To be continued...lol