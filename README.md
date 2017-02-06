A straightforward Python script, running on (free) Google App Engine.

Display:
- A sketch prompt every day, chosen at random from a list of 365. Strike the prompt once chosen.
- A media prompt (I need to learn to use something other than a 6B :pencil:).
- A gallery of links to tutorials on sketching/drawing.
- Prompts from previous days.

Run it yourself:
- Clone this repo.
- Follow the Google App Engine tutorials/instructions for Python development.
- Note that we're using the [AppEngine Google Cloud Storage client](https://github.com/GoogleCloudPlatform/appengine-gcs-client). Do the following in order to test using the local development server:
  - Download [appengine-gcs-client](https://github.com/GoogleCloudPlatform/appengine-gcs-client) `master.zip` and unzip.
  - Copy the`appengine-gcs-client/python/src/cloudstorage` directory into this repo.
  - TODO: Run `foo` to set up local Cloud Storage - otherwise, the local dev server will fail trying to contact the Google Cloud Storage servers.
