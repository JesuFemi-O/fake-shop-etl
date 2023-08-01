# fake-shop-etl

This repo demonstrates an end to end process for developing, testing and deploying google cloud functions using CI/CD pipelines setup with github actions.

The Fake shop etl is an etl pipeline for an imaginary e-commerce startup called fake shop. When a customer places an order for a fake shop product from it's 3rd party partner, they send a csv file to fake shop to process the order. The orders info are uploaded to a gsc bucket. Fake shop setup this pipeline to automatically surface the order in Bigquery. when the file gets uploaded the serverless pipeline is triggered and it loads the file into bigquery before moving the orders file to subfolder named `processed`.

To manage the pipeline, encourage collaboration, local development, testing and automated deployment. we have setup workflows to ensure that continuous Integration and deployment are enforced.

## Resources required

- A GCS bucket: this is where files will be uploaded to trigger the pipeline

- A Bigquery Dataset: We have to create two bigquery dataset where tables from the bucket will be created in production and development/ci.

- A CD service account: service account to be used by CD pipline with service account user and cloud function developer roles

- A CI service account: this service account requires storage object, storage and bigquery admin priviledges to be able to test the cloud function against s3 and bigquery

- A development service account: same priviledges as ci service account, to be used for local development and testing.

## CI flow

- when a PR is opened, the ci pipeline is triggered and merge button will be active only after the ci checks passes.


### misc [to be removed]

To get the CD workflow working I had to run:

```bash
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=serviceAccount:gcf-cd-service-account@<PROJECT_ID>.iam.gserviceaccount.com --role=roles/iam.serviceAccountUser
```

this was to to allow my CD service account the ability to be a service account caller/ a user of other service accounts in my project.

# how to set this up:

- create a storage bucket

- create 3 service accounts, one for Continous Integration, Continuous Deployment, local development. The CI service account should be able to access GCS and Biguqery. The CD service account should have the Cloud functions developer role and should have permission to use other service accounts. the development seervice account should have same priviledges as the CI service account.

- To be continued...lol